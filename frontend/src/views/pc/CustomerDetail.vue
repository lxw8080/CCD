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
                    accept="image/*"
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
                    :disabled="!uploadForm.documentType || fileList.length === 0"
                    @click="handleUpload"
                  >
                    上传
                  </el-button>
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
                <el-table-column prop="file_name" label="文件名" />
                <el-table-column prop="file_size" label="文件大小" width="120">
                  <template #default="{ row }">
                    {{ formatFileSize(row.file_size) }}
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
                <el-table-column label="操作" width="150" fixed="right">
                  <template #default="{ row }">
                    <el-button type="primary" size="small" @click="handlePreview(row)">
                      查看
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
    
    <!-- 图片预览对话框 -->
    <el-dialog v-model="previewVisible" title="图片预览" width="80%">
      <img :src="previewUrl" style="width: 100%" />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getCustomer, getCustomerCompleteness } from '@/api/customer'
import { getDocumentTypes, getDocuments, uploadDocument, deleteDocument } from '@/api/document'
import { compressImage, formatFileSize } from '@/utils/image'
import { ElMessage, ElMessageBox } from 'element-plus'

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

const uploadForm = reactive({
  documentType: null
})

const statusMap = {
  pending: { text: '资料收集中', type: 'info' },
  complete: { text: '资料已齐全', type: 'success' },
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
const getStatusType = (status) => statusMap[status]?.type || 'info'
const getDocStatusText = (status) => docStatusMap[status]?.text || status
const getDocStatusType = (status) => docStatusMap[status]?.type || 'info'

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
  
  uploadLoading.value = true
  
  try {
    // 上传每个文件
    for (const file of fileList.value) {
      const formData = new FormData()
      
      // 压缩图片
      const compressedFile = await compressImage(file.raw)
      
      formData.append('customer', route.params.id)
      formData.append('document_type', uploadForm.documentType)
      formData.append('file', compressedFile)
      
      await uploadDocument(formData)
    }
    
    ElMessage.success('上传成功')
    fileList.value = []
    uploadForm.documentType = null
    
    // 刷新数据
    fetchDocuments()
    fetchCompleteness()
  } catch (error) {
    ElMessage.error('上传失败')
  } finally {
    uploadLoading.value = false
  }
}

const handlePreview = (doc) => {
  previewUrl.value = doc.file_url
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

