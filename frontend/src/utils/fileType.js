/**
 * 文件类型判断工具
 */

// 文件类型定义
export const FILE_TYPES = {
  image: {
    name: '图片',
    extensions: ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'],
    icon: 'el-icon-picture',
    mimeTypes: ['image/jpeg', 'image/png', 'image/gif', 'image/bmp', 'image/webp']
  },
  video: {
    name: '视频',
    extensions: ['mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv'],
    icon: 'el-icon-video-play',
    mimeTypes: ['video/mp4', 'video/x-msvideo', 'video/quicktime', 'video/x-ms-wmv', 'video/x-flv', 'video/x-matroska']
  },
  pdf: {
    name: 'PDF',
    extensions: ['pdf'],
    icon: 'el-icon-document-copy',
    mimeTypes: ['application/pdf']
  },
  document: {
    name: '文档',
    extensions: ['doc', 'docx', 'txt', 'rtf'],
    icon: 'el-icon-document',
    mimeTypes: ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain', 'application/rtf']
  },
  spreadsheet: {
    name: '表格',
    extensions: ['xls', 'xlsx', 'csv'],
    icon: 'el-icon-document',
    mimeTypes: ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'text/csv']
  }
}

/**
 * 根据文件名获取文件类型
 * @param {string} filename - 文件名
 * @returns {string|null} - 文件类型 ('image', 'video', 'pdf', 'document', 'spreadsheet') 或 null
 */
export function getFileType(filename) {
  if (!filename) return null
  
  const ext = filename.split('.').pop().toLowerCase()
  
  for (const [type, config] of Object.entries(FILE_TYPES)) {
    if (config.extensions.includes(ext)) {
      return type
    }
  }
  
  return null
}

/**
 * 获取文件类型的中文名称
 * @param {string} fileType - 文件类型
 * @returns {string} - 中文名称
 */
export function getFileTypeName(fileType) {
  return FILE_TYPES[fileType]?.name || '未知'
}

/**
 * 获取文件类型的显示名称（别名）
 * @param {string} fileType - 文件类型
 * @returns {string} - 显示名称
 */
export function getFileTypeDisplay(fileType) {
  return getFileTypeName(fileType)
}

/**
 * 获取文件类型的图标类名
 * @param {string} fileType - 文件类型
 * @returns {string} - 图标类名
 */
export function getFileTypeIcon(fileType) {
  return FILE_TYPES[fileType]?.icon || 'el-icon-document'
}

/**
 * 获取支持的文件扩展名列表
 * @returns {string} - 逗号分隔的扩展名列表
 */
export function getSupportedExtensions() {
  const extensions = []
  for (const config of Object.values(FILE_TYPES)) {
    extensions.push(...config.extensions)
  }
  return extensions.join(',')
}

/**
 * 获取 accept 属性值
 * @returns {string} - accept 属性值
 */
export function getAcceptAttribute() {
  const accepts = []
  for (const config of Object.values(FILE_TYPES)) {
    accepts.push(...config.mimeTypes)
  }
  return accepts.join(',')
}

/**
 * 判断是否为图片
 * @param {string} fileType - 文件类型
 * @returns {boolean}
 */
export function isImage(fileType) {
  return fileType === 'image'
}

/**
 * 判断是否为视频
 * @param {string} fileType - 文件类型
 * @returns {boolean}
 */
export function isVideo(fileType) {
  return fileType === 'video'
}

/**
 * 判断是否为 PDF
 * @param {string} fileType - 文件类型
 * @returns {boolean}
 */
export function isPdf(fileType) {
  return fileType === 'pdf'
}

/**
 * 判断是否为文档
 * @param {string} fileType - 文件类型
 * @returns {boolean}
 */
export function isDocument(fileType) {
  return fileType === 'document'
}

/**
 * 判断是否为表格
 * @param {string} fileType - 文件类型
 * @returns {boolean}
 */
export function isSpreadsheet(fileType) {
  return fileType === 'spreadsheet'
}

/**
 * 判断是否支持预览
 * @param {string} fileType - 文件类型
 * @returns {boolean}
 */
export function isSupportedPreview(fileType) {
  return ['image', 'video', 'pdf'].includes(fileType)
}

/**
 * 获取文件大小限制（字节）
 * @param {string} fileType - 文件类型
 * @returns {number} - 文件大小限制
 */
export function getFileSizeLimit(fileType) {
  const limits = {
    image: 5 * 1024 * 1024,      // 5MB
    video: 50 * 1024 * 1024,     // 50MB
    pdf: 10 * 1024 * 1024,       // 10MB
    document: 10 * 1024 * 1024,  // 10MB
    spreadsheet: 10 * 1024 * 1024 // 10MB
  }
  return limits[fileType] || 10 * 1024 * 1024
}

/**
 * 格式化文件大小限制为可读字符串
 * @param {string} fileType - 文件类型
 * @returns {string} - 格式化后的大小限制
 */
export function formatFileSizeLimit(fileType) {
  const limit = getFileSizeLimit(fileType)
  return `${limit / (1024 * 1024)}MB`
}

