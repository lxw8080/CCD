import Compressor from 'compressorjs'

/**
 * 压缩图片
 * @param {File} file - 原始文件
 * @param {Object} options - 压缩选项
 * @returns {Promise<File>}
 */
export function compressImage(file, options = {}) {
  return new Promise((resolve, reject) => {
    new Compressor(file, {
      quality: options.quality || 0.8,
      maxWidth: options.maxWidth || 1920,
      maxHeight: options.maxHeight || 1920,
      mimeType: options.mimeType || 'image/jpeg',
      success(result) {
        // 将Blob转换为File对象
        const compressedFile = new File([result], file.name, {
          type: result.type,
          lastModified: Date.now()
        })
        resolve(compressedFile)
      },
      error(err) {
        reject(err)
      }
    })
  })
}

/**
 * 批量压缩图片
 * @param {File[]} files - 文件数组
 * @param {Object} options - 压缩选项
 * @returns {Promise<File[]>}
 */
export async function compressImages(files, options = {}) {
  const promises = files.map(file => compressImage(file, options))
  return Promise.all(promises)
}

/**
 * 格式化文件大小
 * @param {number} bytes - 字节数
 * @returns {string}
 */
export function formatFileSize(bytes) {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return (bytes / Math.pow(k, i)).toFixed(2) + ' ' + sizes[i]
}

