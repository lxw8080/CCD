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
            :before-read="beforeRead"
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
            @click="handleUpload($event)"
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
import { ref, reactive, computed, onMounted, onBeforeUnmount, watch } from 'vue'
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

const getDisplayFileName = (file) => file?.name || '未命名文件'


const uploaderLogPrefix = '[MobileUploader]'
const isIOSDevice = typeof window !== 'undefined' && /iP(ad|hone|od)/i.test((window.navigator?.userAgent) || '')
const isSafari = typeof window !== 'undefined' ? /^((?!chrome|android).)*safari/i.test(window.navigator?.userAgent || '') : false
let globalErrorToastTimer = null


const logDebug = (...args) => {
  if (typeof console !== 'undefined' && console.log) {
    console.log(uploaderLogPrefix, ...args)
  }
}

const logError = (...args) => {
  if (typeof console !== 'undefined' && console.error) {
    console.error(uploaderLogPrefix, ...args)
  }
}

const cleanupCallbacks = []

const getFileSnapshot = (file) => {
  if (!file) return null
  return {
    name: file.name,
    size: file.size,
    type: file.type,
    lastModified: file.lastModified,
    constructor: file.constructor?.name
  }
}

const formatUploadErrorMessage = (error, fallback = '上传失败') => {
  try {
    if (!error) return fallback

    const status = error.response?.status
    const statusText = error.response?.statusText
    const backendMessage = error.response?.data?.error || error.response?.data?.detail
    const networkMessage = error.message

    if (backendMessage) {
      return `${fallback}：${backendMessage}`
    }

    if (status) {
      return `${fallback}（HTTP ${status}${statusText ? ` ${statusText}` : ''}）`
    }

    if (networkMessage) {
      return `${fallback}：${networkMessage}`
    }
  } catch (formatError) {
    logError('formatUploadErrorMessage failed', formatError)
  }

  return fallback
}

const unwrapRawFile = (item) => {
  if (!item) return null
  if (item instanceof File) return item
  if (item.file instanceof File) return item.file
  return item.file || null
}

const detectFileType = (file) => {
  if (!file) return null
  try {
    const snapshot = getFileSnapshot(file)
    logDebug('detectFileType invoked', { snapshot })
    const detected = getFileTypeFromFile(file) || getFileType(file.name)
    logDebug('detectFileType result', { detected, snapshot })
    return detected
  } catch (error) {
    logError('detectFileType failed', error)
    try {
      return getFileType(file.name)
    } catch (fallbackError) {
      logError('detectFileType fallback failed', fallbackError)
      return null
    }
  }
}

const formatAllowedTypeNames = (types = []) => {
  if (!Array.isArray(types) || types.length === 0) {
    return ''
  }
  return types.map(type => getFileTypeName(type) || type).join('、')
}

const getFileValidationError = (rawFile, docType) => {
  if (!rawFile) {
    return '无法读取所选文件，请重新选择'
  }

  const fileType = detectFileType(rawFile)
  if (!fileType) {
    return `不支持的文件类型：${getDisplayFileName(rawFile)}`
  }

  const allowed = docType?.allowed_file_types
  if (Array.isArray(allowed) && allowed.length > 0 && !allowed.includes(fileType)) {
    const allowedText = formatAllowedTypeNames(allowed)
    return `${getDisplayFileName(rawFile)} 类型不符合要求（需上传 ${allowedText}）`
  }

  const sizeLimit = getFileSizeLimit(fileType)
  if (Number.isFinite(sizeLimit) && rawFile.size > sizeLimit) {
    return `${getDisplayFileName(rawFile)} 文件大小超过限制（最大 ${formatFileSizeLimit(fileType)}）`
  }

  return null
}

const removePendingItemWithDelay = async (target) => {
  try {
    await new Promise(resolve => setTimeout(resolve, 0))
    const beforeLength = fileList.value.length
    fileList.value = fileList.value.filter(item => item !== target)
    logDebug('removePendingItemWithDelay', { beforeLength, afterLength: fileList.value.length })
  } catch (error) {
    logError('removePendingItemWithDelay failed', error)
  }
}

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
    return 'image/*,.pdf,.doc,.docx,.xls,.xlsx,.txt,.rtf,.csv,.mp4,.mov,.avi,.wmv,.flv,.mkv,.m4v,.3gp,.3gpp,.webm,.ts,.mpg,.mpeg,.ogg'
  }

  const accepts = []
  if (docType.allowed_file_types.includes('image')) {
    accepts.push('image/*')
  }
  if (docType.allowed_file_types.includes('video')) {
    accepts.push('.mp4', '.mov', '.avi', '.wmv', '.flv', '.mkv', '.m4v', '.3gp', '.3gpp', '.webm', '.ts', '.mpg', '.mpeg', '.ogg')
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

const uploaderCapture = computed(() => {
  const docType = currentDocumentType.value
  const allowed = docType?.allowed_file_types

  if (!Array.isArray(allowed) || allowed.length === 0) {
    logDebug('uploaderCapture fallback: unrestricted types', { isiOS: isIOSDevice })
    return undefined
  }

  const onlyImages = allowed.every(type => type === 'image')
  if (onlyImages) {
    const captureMode = isIOSDevice ? 'environment' : 'environment'
    logDebug('uploaderCapture image only', { captureMode, isiOS: isIOSDevice })
    return captureMode
  }

  const onlyVideo = allowed.length > 0 && allowed.every(type => type === 'video')
  if (onlyVideo) {
    logDebug('uploaderCapture disabled for video only types', { allowed, isiOS: isIOSDevice })
    return undefined
  }

  const imageAndVideo = allowed.every(type => type === 'image' || type === 'video')
  if (imageAndVideo) {
    logDebug('uploaderCapture disabled for image & video combo', { allowed, isiOS: isIOSDevice })
    return undefined
  }

  logDebug('uploaderCapture disabled for unsupported mix', { allowed })
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

const beforeRead = (file) => {
  logDebug('beforeRead triggered', { isiOS: isIOSDevice })
  try {
    const items = Array.isArray(file) ? file : [file]
    logDebug('beforeRead received items', { count: items.length, fileSnapshots: items.map(it => getFileSnapshot(unwrapRawFile(it) || it.file)) })

    if (!uploadForm.documentType) {
      showToast("请选择资料类型后再上传")
      return false
    }

    const docType = currentDocumentType.value
    if (!docType) {
      showToast("资料类型不存在或已被删除")
      return false
    }

    if (!canUpload.value) {
      showToast("已达到最大文件数限制")
      return false
    }

    const pendingCount = fileList.value.length
    const maxCount = docType.max_file_count || 0
    if (maxCount > 0) {
      const remaining = maxCount - uploadedCount.value - pendingCount
      if (remaining <= 0) {
        showToast("已达到最大文件数限制")
        return false
      }
      if (items.length > remaining) {
        showToast(`最多还能选择 ${remaining} 个文件`)
        return false
      }
    }

    for (const item of items) {
      const rawFile = unwrapRawFile(item)
      const errorMessage = getFileValidationError(rawFile, docType)
      if (errorMessage) {
        logDebug('beforeRead validation failed', { errorMessage, snapshot: getFileSnapshot(rawFile) })
        showToast(errorMessage)
        return false
      }
    }

    logDebug('beforeRead validation passed')
    return true
  } catch (error) {
    logError('beforeRead encountered error', error)
    showToast(`处理文件选择时出错：${error?.message || error}`)
    return false
  }
}

const afterRead = async (file) => {
  logDebug('afterRead invoked', { isiOS: isIOSDevice })
  const items = Array.isArray(file) ? file : [file]
  logDebug('afterRead received items', { count: items.length, fileSnapshots: items.map(it => getFileSnapshot(unwrapRawFile(it) || it.file)) })

  try {
    if (!uploadForm.documentType) {
      showToast("请选择资料类型后再上传")
      await Promise.all(items.map(item => removePendingItemWithDelay(item)))
      return
    }

    const docType = currentDocumentType.value
    if (!docType) {
      showToast("资料类型不存在或已被删除")
      await Promise.all(items.map(item => removePendingItemWithDelay(item)))
      return
    }

    if (!canUpload.value) {
      showToast("已达到最大文件数限制")
      await Promise.all(items.map(item => removePendingItemWithDelay(item)))
      return
    }

    for (const item of items) {
      try {
        const rawFile = unwrapRawFile(item)
        const errorMessage = getFileValidationError(rawFile, docType)
        if (errorMessage) {
          logDebug('afterRead validation failed', { errorMessage, snapshot: getFileSnapshot(rawFile) })
          showToast(errorMessage)
          await removePendingItemWithDelay(item)
          continue
        }

        ensurePreviewMeta(item)
        logDebug('afterRead preview metadata ensured', { snapshot: getFileSnapshot(rawFile) })
      } catch (innerError) {
        logError('afterRead inner loop error', innerError)
        showToast(`处理文件时出错：${innerError?.message || innerError}`)
      }
    }
  } catch (error) {
    logError('afterRead top-level error', error)
    showToast(`处理文件时出错：${error?.message || error}`)
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
    const rawFile = unwrapRawFile(item) || item.file
    logDebug('ensurePreviewMeta start', { hasPreviewUrl: !!item.previewUrl, snapshot: getFileSnapshot(rawFile) })
    if (!item.previewUrl) {
      if (item.content) {
        // Vant Uploader base64 预览
        item.previewUrl = item.content
      } else if (item.file instanceof File) {
        item.previewUrl = URL.createObjectURL(item.file)
      } else if (rawFile instanceof File) {
        item.previewUrl = URL.createObjectURL(rawFile)
      }
    }
    if (!item.previewType) {
      item.previewType = getFileTypeFromFile(item.file) || getFileTypeFromFile(rawFile) || 'image'
    }
    logDebug('ensurePreviewMeta success', { hasPreviewUrl: !!item.previewUrl, previewType: item.previewType })
  } catch (e) {
    logError('ensurePreviewMeta failed', e)
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
    const snapshots = (list || []).map(it => getFileSnapshot(unwrapRawFile(it) || it.file))
    logDebug('fileList watcher triggered', { count: list?.length || 0, snapshots })
    ;(list || []).forEach(it => ensurePreviewMeta(it))
  } catch (e) {
    logError('fileList watcher error', e)
  }
}, { deep: true })


const handleUpload = async (event) => {
  try {
    event?.preventDefault?.()
    event?.stopPropagation?.()
  } catch (eventError) {
    logError('handleUpload event normalization failed', eventError)
  }

  logDebug('handleUpload triggered', {
    isiOS: isIOSDevice,
    fileCount: fileList.value.length,
    documentType: uploadForm.documentType
  })

  if (!uploadForm.documentType) {
    showToast("请选择资料类型")
    return
  }

  if (fileList.value.length === 0) {
    showToast("请选择要上传的文件")
    return
  }

  if (!canUpload.value) {
    showToast("已达到最大文件数限制")
    return
  }

  const docType = currentDocumentType.value
  if (!docType) {
    showToast("资料类型不存在或已被删除")
    return
  }

  const pendingUploads = []
  for (const item of fileList.value) {
    const rawFile = unwrapRawFile(item) || item.file
    const snapshot = getFileSnapshot(rawFile)
    try {
      const errorMessage = getFileValidationError(rawFile, docType)
      if (errorMessage) {
        logDebug('handleUpload validation failed', { errorMessage, snapshot })
        showToast(errorMessage)
        return
      }
      pendingUploads.push(rawFile)
    } catch (validationError) {
      logError('handleUpload validation error', validationError, { snapshot })
      showToast("校验文件时出错，请重试")
      return
    }
  }

  uploadLoading.value = true

  try {
    for (const rawFile of pendingUploads) {
      const snapshot = getFileSnapshot(rawFile)
      logDebug('handleUpload uploading file', { snapshot })
      const formData = new FormData()

      formData.append('customer', route.params.id)
      formData.append('document_type', uploadForm.documentType)
      formData.append('file', rawFile)

      await uploadDocument(formData)
    }

    showToast({ message: '上传成功', type: 'success' })
    try {
      fileList.value.forEach(it => {
        if (it && typeof it.previewUrl === 'string' && it.previewUrl.startsWith('blob:')) {
          URL.revokeObjectURL(it.previewUrl)
        }
      })
    } catch (e) {
      logError('handleUpload revokeObjectURL error', e)
    }
    fileList.value = []
    uploadForm.documentType = null

    fetchDocuments()
    fetchCompleteness()
  } catch (error) {
    logError('handleUpload failed', error)
    const message = formatUploadErrorMessage(error, '上传失败')
    showToast(message)
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
  logDebug('MobileCustomerDetail mounted', { isiOS: isIOSDevice, isSafari })
  if (typeof window !== 'undefined') {
    const errorHandler = (event) => {
      logError('Global window error', {
        message: event?.message,
        filename: event?.filename,
        lineno: event?.lineno,
        colno: event?.colno,
        error: event?.error
      })
      if (!globalErrorToastTimer) {
        showToast(`页面发生错误：${event?.message || '未知错误'}`)
        globalErrorToastTimer = setTimeout(() => {
          globalErrorToastTimer = null
        }, 2000)
      }
    }

    const rejectionHandler = (event) => {
      logError('Unhandled promise rejection', {
        reason: event?.reason
      })
      if (!globalErrorToastTimer) {
        const message = typeof event?.reason?.message === 'string' ? event.reason.message : (event?.reason || '未知错误')
        showToast(`请求处理异常：${message}`)
        globalErrorToastTimer = setTimeout(() => {
          globalErrorToastTimer = null
        }, 2000)
      }
    }

    window.addEventListener('error', errorHandler)
    window.addEventListener('unhandledrejection', rejectionHandler)

    cleanupCallbacks.push(() => {
      window.removeEventListener('error', errorHandler)
      window.removeEventListener('unhandledrejection', rejectionHandler)
      if (globalErrorToastTimer) {
        clearTimeout(globalErrorToastTimer)
        globalErrorToastTimer = null
      }
    })
  }
  fetchCustomerDetail()
  fetchCompleteness()
  fetchDocumentTypes()
  fetchDocuments()
})

onBeforeUnmount(() => {
  cleanupCallbacks.forEach(cb => {
    try {
      cb()
    } catch (error) {
      logError('cleanup callback failed', error)
    }
  })
  cleanupCallbacks.length = 0
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
