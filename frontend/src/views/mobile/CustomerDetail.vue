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
            :accept="uploaderAccept"
            :capture="uploaderCapture"
          />

          <!-- 选择的文件（未上传）预览入口 -->
          <div v-if="fileList.length" class="selected-files">
            <div
              v-for="(item, idx) in fileList"
              :key="idx"
              class="selected-file-row"
              style="display:flex;justify-content:space-between;align-items:center;margin-top:8px;gap:8px;"
            >
              <div style="flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:#646566;font-size:12px;">
                {{ item.file?.name || '未命名文件' }}
              </div>
              <van-button size="mini" type="primary" @click="previewSelected(item)">预览</van-button>
            </div>
          </div>


          <van-button
            type="primary"
            block
            round
            :loading="uploadLoading"
            :disabled="!uploadForm.documentType || fileList.length === 0 || !canUpload"
            @click="handleUpload"
            style="margin-top: 16px;"
          >
            上传
          </van-button>
          <div v-if="uploadForm.documentType && currentDocumentType" style="margin-top: 8px; font-size: 12px; color: #909399; text-align: center;">
            <div v-if="currentDocumentType.max_file_count === 0">无限制</div>
            <div v-else>
              已上传 {{ uploadedCount }} / 最多 {{ currentDocumentType.max_file_count }} 个文件
              <div v-if="!canUpload" style="color: #f56c6c; margin-top: 4px;">已达到最大文件数限制</div>
            </div>
          </div>
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

    <!-- 文件预览 -->
    <MobilePreviewDialog
      v-model="previewVisible"
      :file-url="previewUrl"
      :file-name="previewFileName"
      :file-type="previewFileType"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getCustomer, getCustomerCompleteness } from '@/api/customer'
import { getDocumentTypes, getDocuments, uploadDocument, deleteDocument } from '@/api/document'
import { formatFileSize } from '@/utils/image'
import { getFileType, getFileTypeName, getFileSizeLimit, formatFileSizeLimit, getFileTypeFromFile } from '@/utils/fileType'
import { showToast, showConfirmDialog } from 'vant'
import MobilePreviewDialog from '@/components/FilePreview/MobilePreviewDialog.vue'

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
const previewUrl = ref('')
const previewFileName = ref('')
const previewFileType = ref('image')

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

// 当前选中的资料类型信息
const currentDocumentType = computed(() => {
  if (!uploadForm.documentType) return null
  return documentTypes.value.find(dt => dt.id === uploadForm.documentType)
})

// 当前资料类型已上传的文件数
const uploadedCount = computed(() => {
  if (!uploadForm.documentType) return 0
  return documents.value.filter(doc => doc.document_type === uploadForm.documentType).length
})

// 是否可以上传（检查文件数量限制）
const canUpload = computed(() => {
  if (!uploadForm.documentType) return false
  const docType = currentDocumentType.value
  if (!docType) return false

  // 如果没有设置最大文件数限制（0 表示不限制），则可以上传
  if (docType.max_file_count === 0) return true

  // 否则检查是否已达到限制
  return uploadedCount.value < docType.max_file_count
})

// 动态生成 accept 属性（根据资料类型允许的文件类型）
const uploaderAccept = computed(() => {
  const docType = currentDocumentType.value
  if (!docType || !docType.allowed_file_types || docType.allowed_file_types.length === 0) {
    // 如果没有设置限制，允许所有文件类型
    return 'image/*,video/*,.pdf,.doc,.docx,.xls,.xlsx'
  }

  const accepts = []
  if (docType.allowed_file_types.includes('image')) {
    accepts.push('image/*')
  }
  if (docType.allowed_file_types.includes('video')) {
    accepts.push('video/*')
  }
  if (docType.allowed_file_types.includes('pdf')) {
    accepts.push('.pdf')
  }
  if (docType.allowed_file_types.includes('document')) {
    accepts.push('.doc', '.docx', '.txt', '.rtf')
  }
  if (docType.allowed_file_types.includes('spreadsheet')) {
    accepts.push('.xls', '.xlsx', '.csv')
  }

  return accepts.join(',')
})

// 动态生成 capture 属性（根据资料类型设置摄像头模式）
const uploaderCapture = computed(() => {
  const docType = currentDocumentType.value
  if (!docType || !docType.allowed_file_types) {
    return 'environment' // 默认使用后置摄像头
  }

  // 如果只允许视频，使用视频录制
  if (docType.allowed_file_types.length === 1 && docType.allowed_file_types[0] === 'video') {
    return 'camcorder' // 视频录制
  }

  // 如果允许图片，使用相机拍照
  if (docType.allowed_file_types.includes('image')) {
    return 'environment' // 后置摄像头
  }

  // 其他情况不使用 capture（允许从文件管理器选择）
  return undefined
})

const statusMap = {
  pending: { text: '收集中', type: 'default' },
  complete: { text: '已齐全', type: 'success' },
  completed: { text: '已齐全', type: 'success' }, // 兼容数据库中的 completed
  reviewing: { text: '审核中', type: 'warning' },
  in_progress: { text: '审核中', type: 'warning' }, // 兼容数据库中的 in_progress
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
  // 统一为数组处理，兼容多选/单选
  const items = Array.isArray(file) ? file : [file]

  for (const item of items) {
    // 验证是否选择了资料类型
    if (!uploadForm.documentType) {
      showToast('请先选择资料类型')
      // 移除该文件
      fileList.value = fileList.value.filter(x => x !== item)
      continue
    }

    const docType = currentDocumentType.value
    if (!docType) {
      showToast('资料类型不存在')
      fileList.value = fileList.value.filter(x => x !== item)
      continue
    }

    // 获取文件类型：优先文件名，其次 MIME（兼容相机拍摄视频/某些浏览器无扩展名的情况）
    let fileType = getFileTypeFromFile(item.file)
    if (!fileType) {
      showToast(`不支持的文件类型: ${item.file?.name || '未知文件'}`)
      fileList.value = fileList.value.filter(x => x !== item)
      continue
    }

    // 检查文件类型是否被允许
    if (docType.allowed_file_types && docType.allowed_file_types.length > 0) {
      if (!docType.allowed_file_types.includes(fileType)) {
        showToast(`不支持上传 ${getFileTypeName(fileType)} 文件`)
        fileList.value = fileList.value.filter(x => x !== item)


        continue
      }
    }

    // 检查文件大小
    const sizeLimit = getFileSizeLimit(fileType)
    if (item.file.size > sizeLimit) {
      showToast(`${item.file.name} 文件大小超过限制 (最大 ${formatFileSizeLimit(fileType)})`)
      fileList.value = fileList.value.filter(x => x !== item)
      continue
    }

    console.log('文件验证通过:', item.file.name, '类型:', fileType)
  }
}

const beforeDelete = (item) => {
  try {
    if (item && item.previewUrl && typeof item.previewUrl === 'string' && item.previewUrl.startsWith('blob:')) {
      URL.revokeObjectURL(item.previewUrl)
    }
  } catch (e) {
    // noop
  }
  return true
}

// 统一构建本地预览元数据（未上传前）
const ensurePreviewMeta = (item) => {
  try {
    if (!item) return
    if (!item.previewUrl) {
      if (item.content) {
        // Vant Uploader base64 预览
        item.previewUrl = item.content
      } else if (item.file instanceof File) {
        item.previewUrl = URL.createObjectURL(item.file)
      }
    }
    if (!item.previewType) {
      item.previewType = getFileTypeFromFile(item.file) || 'image'
    }
  } catch (e) {
    console.warn('ensurePreviewMeta failed:', e)
  }
}

// 点击“未上传文件”的预览
const previewSelected = (item) => {
  ensurePreviewMeta(item)
  if (!item.previewUrl) {
    showToast('无法预览该文件')
    return
  }
  previewUrl.value = item.previewUrl
  previewFileName.value = item.file?.name || '未命名文件'
  previewFileType.value = item.previewType || 'image'
  previewVisible.value = true
}

// 监听 fileList，自动为新选择的文件生成预览 URL，避免内存泄漏
watch(fileList, (list) => {
  try {
    (list || []).forEach(it => ensurePreviewMeta(it))
  } catch (e) {}
}, { deep: true })


const handleUpload = async () => {
  if (!uploadForm.documentType) {
    showToast('请选择资料类型')
    return
  }

  if (fileList.value.length === 0) {
    showToast('请选择要上传的文件')
    return
  }

  // 检查文件数量限制
  if (!canUpload.value) {
    showToast('已达到最大文件数限制')
    return
  }

  // 上传前再次验证所有文件
  const docType = currentDocumentType.value
  for (const item of fileList.value) {
    const fileType = getFileTypeFromFile(item.file)
    if (!fileType) {
      showToast(`不支持的文件类型: ${item.file?.name || '未知文件'}`)
      return
    }

    // 检查文件类型是否被允许
    if (docType.allowed_file_types && docType.allowed_file_types.length > 0) {
      if (!docType.allowed_file_types.includes(fileType)) {
        showToast(`${item.file.name} 文件类型不符合要求`)
        return
      }
    }

    // 检查文件大小
    const sizeLimit = getFileSizeLimit(fileType)
    if (item.file.size > sizeLimit) {
      showToast(`${item.file.name} 文件大小超过限制 (最大 ${formatFileSizeLimit(fileType)})`)
      return
    }
  }

  uploadLoading.value = true

  try {
    // 上传每个文件
    for (const item of fileList.value) {
      const formData = new FormData()

      formData.append('customer', route.params.id)
      formData.append('document_type', uploadForm.documentType)
      formData.append('file', item.file)

      await uploadDocument(formData)
    }

    showToast({ message: '上传成功', type: 'success' })
    // 清理本地 blob URL，避免内存泄漏
    try {
      fileList.value.forEach(it => {
        if (it && typeof it.previewUrl === 'string' && it.previewUrl.startsWith('blob:')) {
          URL.revokeObjectURL(it.previewUrl)
        }
      })
    } catch (e) {}
    fileList.value = []
    uploadForm.documentType = null

    // 刷新数据
    fetchDocuments()
    fetchCompleteness()
  } catch (error) {
    // 检查是否是后端返回的验证错误
    if (error.response?.data?.error) {
      showToast(error.response.data.error)
    } else if (error.message) {
      showToast('上传失败: ' + error.message)
    } else {
      showToast('上传失败')
    }
    console.error('上传错误:', error)
  } finally {
    uploadLoading.value = false
  }
}

const handlePreview = (doc) => {
  previewUrl.value = doc.file_url
  previewFileName.value = doc.file_name

  // 更稳健地解析文件类型：仅当后端提供的类型可靠时采用，否则从文件名推断
  const knownTypes = ['image', 'video', 'pdf', 'document', 'spreadsheet']
  let resolvedType = doc.file_type
  if (!resolvedType || !knownTypes.includes(resolvedType)) {
    resolvedType = getFileType(doc.file_name) || 'image'
  }
  previewFileType.value = resolvedType

  previewVisible.value = true

  console.log('预览文件:', {
    url: doc.file_url,
    name: doc.file_name,
    type: previewFileType.value,
    rawType: doc.file_type
  })
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

