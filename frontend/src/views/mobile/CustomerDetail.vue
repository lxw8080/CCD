<template>
  <div class="mobile-customer-detail">
    <van-nav-bar
      title="客户详情"
      left-arrow
      fixed
      @click-left="handleBack"
    >
      <template #right>
        <van-button type="primary" size="small" @click="handleEdit">
          编辑
        </van-button>
      </template>
    </van-nav-bar>
    
    <div class="content">
      <!-- 基本信息 -->
      <van-cell-group title="基本信息" inset>
        <van-cell title="姓名" :value="customer?.name" />
        <van-cell title="身份证号" :value="customer?.id_card" />
        <van-cell title="手机号" :value="customer?.phone" />
        <van-cell title="状态">
          <template #value>
            <van-tag :type="getStatusType(customer?.status)">
              {{ getStatusText(customer?.status) }}
            </van-tag>
          </template>
        </van-cell>
        <van-cell title="地址" :value="customer?.address || '-'" />
        <van-cell title="创建人" :value="customer?.created_by_info?.username || '-'" />
        <van-cell title="创建时间" :value="customer?.created_at" />
        <van-cell v-if="customer?.remarks" title="备注" :value="customer.remarks" />
      </van-cell-group>
      
      <!-- 资料完整性 -->
      <van-cell-group title="资料完整性" inset>
        <div style="padding: 16px;">
          <div v-if="completeness">
            <div style="margin-bottom: 16px;">
              <van-progress
                :percentage="completeness.completion_rate"
                :color="getProgressColor(completeness.completion_rate)"
                stroke-width="8"
              />
              <div style="margin-top: 8px; text-align: center; color: #646566;">
                已上传 {{ completeness.uploaded_required }}/{{ completeness.total_required }} 项必需资料
              </div>
            </div>
            
            <van-notice-bar
              v-if="completeness.missing_count > 0"
              left-icon="warning-o"
              :text="`还缺少 ${completeness.missing_count} 项必需资料`"
            />
            
            <div style="margin-top: 16px;">
              <van-cell
                v-for="doc in completeness.documents"
                :key="doc.type_id"
                :title="doc.type_name"
                :label="doc.is_required ? '必需' : '可选'"
              >
                <template #right-icon>
                  <van-tag :type="doc.is_uploaded ? 'success' : 'warning'">
                    {{ doc.is_uploaded ? '已上传' : '未上传' }}
                  </van-tag>
                </template>
              </van-cell>
            </div>
          </div>
        </div>
      </van-cell-group>
      
      <!-- 上传资料 -->
      <van-cell-group title="上传资料" inset>
        <div style="padding: 16px;">
          <van-field
            v-model="selectedTypeName"
            label="资料类型"
            placeholder="请选择资料类型"
            readonly
            is-link
            @click="showTypePicker = true"
          />
          
          <van-uploader
            v-model="fileList"
            :max-count="10"
            multiple
            :after-read="afterRead"
            :before-delete="beforeDelete"
            accept="image/*"
            capture="camera"
          />
          
          <van-button
            type="primary"
            block
            round
            :loading="uploadLoading"
            :disabled="!uploadForm.documentType || fileList.length === 0"
            @click="handleUpload"
            style="margin-top: 16px;"
          >
            上传
          </van-button>
        </div>
      </van-cell-group>
      
      <!-- 已上传资料 -->
      <van-cell-group title="已上传资料" inset>
        <van-list
          v-model:loading="documentsLoading"
          :finished="true"
        >
          <van-cell
            v-for="doc in documents"
            :key="doc.id"
            :title="doc.document_type_name"
            :label="`${doc.file_name} | ${formatFileSize(doc.file_size)}`"
            is-link
            @click="handlePreview(doc)"
          >
            <template #right-icon>
              <div style="display: flex; align-items: center; gap: 8px;">
                <van-tag :type="getDocStatusType(doc.status)">
                  {{ getDocStatusText(doc.status) }}
                </van-tag>
                <van-icon name="delete-o" @click.stop="handleDeleteDoc(doc.id)" />
              </div>
            </template>
          </van-cell>
        </van-list>
        
        <van-empty v-if="documents.length === 0" description="暂无资料" />
      </van-cell-group>
    </div>
    
    <!-- 资料类型选择器 -->
    <van-popup v-model:show="showTypePicker" position="bottom">
      <van-picker
        :columns="typeColumns"
        @confirm="onTypeConfirm"
        @cancel="showTypePicker = false"
      />
    </van-popup>
    
    <!-- 图片预览 -->
    <van-image-preview
      v-model:show="previewVisible"
      :images="previewImages"
      :start-position="previewIndex"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getCustomer, getCustomerCompleteness } from '@/api/customer'
import { getDocumentTypes, getDocuments, uploadDocument, deleteDocument } from '@/api/document'
import { compressImage, formatFileSize } from '@/utils/image'
import { showToast, showConfirmDialog } from 'vant'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const completenessLoading = ref(false)
const documentsLoading = ref(false)
const uploadLoading = ref(false)
const customer = ref(null)
const completeness = ref(null)
const documentTypes = ref([])
const documents = ref([])
const fileList = ref([])
const showTypePicker = ref(false)
const previewVisible = ref(false)
const previewImages = ref([])
const previewIndex = ref(0)

const uploadForm = reactive({
  documentType: null
})

const typeColumns = computed(() => {
  return documentTypes.value.map(type => ({
    text: type.name,
    value: type.id
  }))
})

const selectedTypeName = computed(() => {
  const type = documentTypes.value.find(t => t.id === uploadForm.documentType)
  return type?.name || ''
})

const statusMap = {
  pending: { text: '收集中', type: 'default' },
  complete: { text: '已齐全', type: 'success' },
  reviewing: { text: '审核中', type: 'warning' },
  approved: { text: '已通过', type: 'success' },
  rejected: { text: '已拒绝', type: 'danger' }
}

const docStatusMap = {
  pending: { text: '待审核', type: 'warning' },
  approved: { text: '已通过', type: 'success' },
  rejected: { text: '已拒绝', type: 'danger' }
}

const getStatusText = (status) => statusMap[status]?.text || status
const getStatusType = (status) => statusMap[status]?.type || 'default'
const getDocStatusText = (status) => docStatusMap[status]?.text || status
const getDocStatusType = (status) => docStatusMap[status]?.type || 'default'

const getProgressColor = (percentage) => {
  if (percentage < 50) return '#ee0a24'
  if (percentage < 100) return '#ff976a'
  return '#07c160'
}

const fetchCustomerDetail = async () => {
  loading.value = true
  try {
    customer.value = await getCustomer(route.params.id)
  } catch (error) {
    showToast('获取客户信息失败')
  } finally {
    loading.value = false
  }
}

const fetchCompleteness = async () => {
  completenessLoading.value = true
  try {
    completeness.value = await getCustomerCompleteness(route.params.id)
  } catch (error) {
    showToast('获取资料完整性失败')
  } finally {
    completenessLoading.value = false
  }
}

const fetchDocumentTypes = async () => {
  try {
    const response = await getDocumentTypes()
    // API 返回的是数组（已禁用分页）
    documentTypes.value = Array.isArray(response) ? response : []
    console.log('资料类型数据:', documentTypes.value)
  } catch (error) {
    console.error('获取资料类型失败:', error)
    showToast('获取资料类型失败')
  }
}

const fetchDocuments = async () => {
  documentsLoading.value = true
  try {
    const response = await getDocuments({ customer_id: route.params.id })
    documents.value = response.results || []
  } catch (error) {
    showToast('获取资料列表失败')
  } finally {
    documentsLoading.value = false
  }
}

const onTypeConfirm = ({ selectedOptions }) => {
  uploadForm.documentType = selectedOptions[0].value
  showTypePicker.value = false
}

const afterRead = (file) => {
  console.log('文件选择:', file)
}

const beforeDelete = () => {
  return true
}

const handleUpload = async () => {
  if (!uploadForm.documentType) {
    showToast('请选择资料类型')
    return
  }
  
  if (fileList.value.length === 0) {
    showToast('请选择要上传的文件')
    return
  }
  
  uploadLoading.value = true
  
  try {
    // 上传每个文件
    for (const item of fileList.value) {
      const formData = new FormData()
      
      // 压缩图片
      const compressedFile = await compressImage(item.file)
      
      formData.append('customer', route.params.id)
      formData.append('document_type', uploadForm.documentType)
      formData.append('file', compressedFile)
      
      await uploadDocument(formData)
    }
    
    showToast({ message: '上传成功', type: 'success' })
    fileList.value = []
    uploadForm.documentType = null
    
    // 刷新数据
    fetchDocuments()
    fetchCompleteness()
  } catch (error) {
    showToast('上传失败')
  } finally {
    uploadLoading.value = false
  }
}

const handlePreview = (doc) => {
  previewImages.value = [doc.file_url]
  previewIndex.value = 0
  previewVisible.value = true
}

const handleDeleteDoc = async (id) => {
  try {
    await showConfirmDialog({
      title: '提示',
      message: '确定要删除这个资料吗？'
    })
    
    await deleteDocument(id)
    showToast({ message: '删除成功', type: 'success' })
    fetchDocuments()
    fetchCompleteness()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
    }
  }
}

const handleEdit = () => {
  router.push(`/customers/${route.params.id}/edit`)
}

const handleBack = () => {
  router.push('/customers')
}

onMounted(() => {
  fetchCustomerDetail()
  fetchCompleteness()
  fetchDocumentTypes()
  fetchDocuments()
})
</script>

<style scoped>
.mobile-customer-detail {
  min-height: 100vh;
  background: #f7f8fa;
  padding-bottom: 20px;
}

.content {
  padding-top: 46px;
}

.van-cell-group {
  margin-top: 12px;
}
</style>

