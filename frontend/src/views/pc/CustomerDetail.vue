<template>
  <div class="customer-detail-container">
    <el-container>
      <el-header class="header">
        <div class="header-content">
          <h2>客户详情</h2>
          <el-button @click="handleBack">返回</el-button>
        </div>
      </el-header>
      
      <el-main>
        <el-row :gutter="20">
          <!-- 客户基本信息 -->
          <el-col :span="24">
            <el-card v-loading="loading">
              <template #header>
                <div class="card-header">
                  <span>基本信息</span>
                  <el-button type="primary" size="small" @click="handleEdit">
                    编辑
                  </el-button>
                </div>
              </template>
              
              <el-descriptions v-if="customer" :column="2" border>
                <el-descriptions-item label="姓名">{{ customer.name }}</el-descriptions-item>
                <el-descriptions-item label="身份证号">{{ customer.id_card }}</el-descriptions-item>
                <el-descriptions-item label="手机号">{{ customer.phone }}</el-descriptions-item>
                <el-descriptions-item label="状态">
                  <el-tag :type="getStatusType(customer.status)">
                    {{ getStatusText(customer.status) }}
                  </el-tag>
                </el-descriptions-item>
                <el-descriptions-item label="地址" :span="2">
                  {{ customer.address || '-' }}
                </el-descriptions-item>
                <el-descriptions-item label="创建人">
                  {{ customer.created_by_info?.username || '-' }}
                </el-descriptions-item>
                <el-descriptions-item label="创建时间">
                  {{ customer.created_at }}
                </el-descriptions-item>
                <el-descriptions-item label="备注" :span="2">
                  {{ customer.remarks || '-' }}
                </el-descriptions-item>
              </el-descriptions>
            </el-card>
          </el-col>
          
          <!-- 资料完整性 -->
          <el-col :span="24" style="margin-top: 20px">
            <el-card v-loading="completenessLoading">
              <template #header>
                <span>资料完整性</span>
              </template>
              
              <div v-if="completeness">
                <el-progress
                  :percentage="completeness.completion_rate"
                  :color="getProgressColor(completeness.completion_rate)"
                  :stroke-width="20"
                  style="margin-bottom: 20px"
                />
                
                <el-alert
                  v-if="completeness.missing_count > 0"
                  :title="`还缺少 ${completeness.missing_count} 项必需资料`"
                  type="warning"
                  :closable="false"
                  style="margin-bottom: 20px"
                />
                
                <el-table :data="completeness.documents" border>
                  <el-table-column prop="type_name" label="资料类型" />
                  <el-table-column prop="is_required" label="是否必需" width="100">
                    <template #default="{ row }">
                      <el-tag :type="row.is_required ? 'danger' : 'info'" size="small">
                        {{ row.is_required ? '必需' : '可选' }}
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column prop="is_uploaded" label="上传状态" width="100">
                    <template #default="{ row }">
                      <el-tag :type="row.is_uploaded ? 'success' : 'warning'" size="small">
                        {{ row.is_uploaded ? '已上传' : '未上传' }}
                      </el-tag>
                    </template>
                  </el-table-column>
                </el-table>
              </div>
            </el-card>
          </el-col>
          
          <!-- 资料上传 -->
          <el-col :span="24" style="margin-top: 20px">
            <el-card>
              <template #header>
                <span>上传资料</span>
              </template>
              
              <el-form :inline="true">
                <el-form-item label="资料类型">
                  <el-select v-model="uploadForm.documentType" placeholder="请选择资料类型" style="width: 200px">
                    <el-option
                      v-for="type in documentTypes"
                      :key="type.id"
                      :label="type.name"
                      :value="type.id"
                    />
                  </el-select>
                </el-form-item>

                <el-form-item>
                  <el-upload
                    ref="uploadRef"
                    :auto-upload="false"
                    :on-change="handleFileChange"
                    :file-list="fileList"
                    :limit="10"
                    :accept="acceptAttribute"
                    multiple
                    list-type="picture-card"
                  >
                    <el-icon><Plus /></el-icon>
                  </el-upload>
                </el-form-item>

                <el-form-item>
                  <el-button
                    type="primary"
                    :loading="uploadLoading"
                    :disabled="!uploadForm.documentType || fileList.length === 0 || !canUpload"
                    @click="handleUpload"
                  >
                    上传
                  </el-button>
                  <span v-if="uploadForm.documentType" style="margin-left: 10px; color: #909399; font-size: 12px">
                    {{ uploadHintText }}
                  </span>
                  <span v-if="uploadForm.documentType && !canUpload" style="margin-left: 10px; color: #f56c6c; font-size: 12px">
                    已达到最大文件数限制
                  </span>
                </el-form-item>
              </el-form>
            </el-card>
          </el-col>
          
          <!-- 已上传资料列表 -->
          <el-col :span="24" style="margin-top: 20px">
            <el-card v-loading="documentsLoading">
              <template #header>
                <div class="card-header">
                  <span>已上传资料</span>
                  <el-button type="primary" size="small" @click="fetchDocuments">
                    刷新
                  </el-button>
                </div>
              </template>
              
              <el-table :data="documents" border>
                <el-table-column prop="document_type_name" label="资料类型" width="150" />
                <el-table-column label="文件名" width="200">
                  <template #default="{ row }">
                    <div style="display: flex; align-items: center; gap: 8px">
                      <el-icon :size="20">
                        <component :is="getFileTypeIconComponent(row.file_type)" />
                      </el-icon>
                      <span>{{ row.file_name }}</span>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column prop="file_size" label="文件大小" width="120">
                  <template #default="{ row }">
                    {{ formatFileSize(row.file_size) }}
                  </template>
                </el-table-column>
                <el-table-column prop="file_type" label="文件类型" width="100">
                  <template #default="{ row }">
                    {{ getFileTypeName(row.file_type) }}
                  </template>
                </el-table-column>
                <el-table-column prop="status" label="状态" width="100">
                  <template #default="{ row }">
                    <el-tag :type="getDocStatusType(row.status)" size="small">
                      {{ getDocStatusText(row.status) }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="uploaded_by_info.username" label="上传人" width="100" />
                <el-table-column prop="uploaded_at" label="上传时间" width="180" />
                <el-table-column label="操作" width="180" fixed="right">
                  <template #default="{ row }">
                    <el-button type="primary" size="small" @click="handlePreview(row)">
                      预览
                    </el-button>
                    <el-button type="danger" size="small" @click="handleDeleteDoc(row.id)">
                      删除
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
    
    <!-- 文件预览对话框 -->
    <PreviewDialog
      v-model="previewVisible"
      :file-url="previewUrl"
      :file-name="previewFileName"
      :file-type="previewFileType"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getCustomer, getCustomerCompleteness } from '@/api/customer'
import { getDocumentTypes, getDocuments, uploadDocument, deleteDocument } from '@/api/document'
import { compressImage, formatFileSize } from '@/utils/image'
import { getFileType, getFileTypeName, getAcceptAttribute, isImage } from '@/utils/fileType'
import { PreviewDialog } from '@/components/FilePreview'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

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
const previewVisible = ref(false)
const previewUrl = ref('')
const previewFileName = ref('')
const previewFileType = ref('image')

const uploadForm = reactive({
  documentType: null
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

// 上传提示信息
const uploadHintText = computed(() => {
  if (!uploadForm.documentType) return ''
  const docType = currentDocumentType.value
  if (!docType) return ''

  if (docType.max_file_count === 0) {
    return '无限制'
  }

  return `已上传 ${uploadedCount.value} / 最多 ${docType.max_file_count} 个文件`
})

// 动态生成 accept 属性
const acceptAttribute = computed(() => {
  const docType = currentDocumentType.value
  if (!docType || !docType.allowed_file_types || docType.allowed_file_types.length === 0) {
    // 如果没有设置限制，允许所有文件类型
    return getAcceptAttribute()
  }

  // 根据允许的文件类型生成 accept 字符串
  const FILE_TYPES = {
    image: { extensions: ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'], mimeTypes: ['image/*'] },
    video: { extensions: ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv'], mimeTypes: ['video/*'] },
    pdf: { extensions: ['.pdf'], mimeTypes: ['application/pdf'] },
    document: { extensions: ['.doc', '.docx', '.txt', '.rtf'], mimeTypes: ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain', 'application/rtf'] },
    spreadsheet: { extensions: ['.xls', '.xlsx', '.csv'], mimeTypes: ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'text/csv'] }
  }

  const acceptTypes = docType.allowed_file_types
    .map(type => FILE_TYPES[type]?.extensions?.join(',') || '')
    .filter(ext => ext)
    .join(',')

  return acceptTypes || getAcceptAttribute()
})

const statusMap = {
  pending: { text: '资料收集中', type: 'info' },
  complete: { text: '资料已齐全', type: 'success' },
  completed: { text: '资料已齐全', type: 'success' }, // 兼容数据库中的 completed
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
const getStatusType = (status) => statusMap[status]?.type || 'info'
const getDocStatusText = (status) => docStatusMap[status]?.text || status
const getDocStatusType = (status) => docStatusMap[status]?.type || 'info'

// 文件类型图标映射（用于 Element Plus 图标组件）
const getFileTypeIconComponent = (fileType) => {
  const iconMap = {
    image: 'Picture',
    video: 'VideoPlay',
    pdf: 'DocumentCopy',
    document: 'Document',
    spreadsheet: 'Document'
  }
  return iconMap[fileType] || 'Document'
}

const getProgressColor = (percentage) => {
  if (percentage < 50) return '#f56c6c'
  if (percentage < 100) return '#e6a23c'
  return '#67c23a'
}

const fetchCustomerDetail = async () => {
  loading.value = true
  try {
    customer.value = await getCustomer(route.params.id)
  } catch (error) {
    ElMessage.error('获取客户信息失败')
  } finally {
    loading.value = false
  }
}

const fetchCompleteness = async () => {
  completenessLoading.value = true
  try {
    completeness.value = await getCustomerCompleteness(route.params.id)
  } catch (error) {
    ElMessage.error('获取资料完整性失败')
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
    ElMessage.error('获取资料类型失败')
  }
}

const fetchDocuments = async () => {
  documentsLoading.value = true
  try {
    const response = await getDocuments({ customer_id: route.params.id })
    documents.value = response.results || []
  } catch (error) {
    ElMessage.error('获取资料列表失败')
  } finally {
    documentsLoading.value = false
  }
}

const handleFileChange = (file, files) => {
  fileList.value = files
}

const handleUpload = async () => {
  if (!uploadForm.documentType) {
    ElMessage.warning('请选择资料类型')
    return
  }

  if (fileList.value.length === 0) {
    ElMessage.warning('请选择要上传的文件')
    return
  }

  // 检查文件数量限制
  if (!canUpload.value) {
    ElMessage.error('已达到最大文件数限制')
    return
  }

  // 验证文件类型
  const docType = currentDocumentType.value
  if (docType && docType.allowed_file_types && docType.allowed_file_types.length > 0) {
    for (const file of fileList.value) {
      const fileType = getFileType(file.name)
      if (!docType.allowed_file_types.includes(fileType)) {
        ElMessage.error(`文件 ${file.name} 的类型不符合要求。允许的类型: ${docType.allowed_file_types.join(', ')}`)
        return
      }
    }
  }

  uploadLoading.value = true

  try {
    // 上传每个文件
    for (const file of fileList.value) {
      const formData = new FormData()

      // 获取文件类型
      const fileType = getFileType(file.name)

      // 如果是图片，进行压缩
      let uploadFile = file.raw
      if (isImage(fileType)) {
        uploadFile = await compressImage(file.raw)
      }

      formData.append('customer', route.params.id)
      formData.append('document_type', uploadForm.documentType)
      formData.append('file', uploadFile)

      await uploadDocument(formData)
    }

    ElMessage.success('上传成功')
    fileList.value = []
    uploadForm.documentType = null

    // 刷新数据
    fetchDocuments()
    fetchCompleteness()
  } catch (error) {
    // 检查是否是后端返回的验证错误
    if (error.response?.data?.error) {
      ElMessage.error(error.response.data.error)
    } else {
      ElMessage.error('上传失败')
    }
  } finally {
    uploadLoading.value = false
  }
}

const handlePreview = (doc) => {
  previewUrl.value = doc.file_url
  previewFileName.value = doc.file_name
  previewFileType.value = doc.file_type || 'image'
  previewVisible.value = true
}

const handleDeleteDoc = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除这个资料吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await deleteDocument(id)
    ElMessage.success('删除成功')
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
.customer-detail-container {
  min-height: 100vh;
  background: #f0f2f5;
}

.header {
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.header-content h2 {
  margin: 0;
  color: #333;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>

