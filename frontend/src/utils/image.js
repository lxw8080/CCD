/**
 * 上传工具：保留旧接口但不进行压缩，确保返回原始文件。
 */

export function compressImage(file) {
  return Promise.resolve(file)
}

export function compressImages(files) {
  if (!Array.isArray(files)) {
    return Promise.resolve([])
  }
  return Promise.all(files.map((file) => compressImage(file)))
}

export function formatFileSize(size) {
  if (!Number.isFinite(size)) {
    return '0 B'
  }

  if (size >= 1024 * 1024) {
    return `${(size / (1024 * 1024)).toFixed(2)} MB`
  }

  if (size >= 1024) {
    return `${(size / 1024).toFixed(2)} KB`
  }

  if (size > 0) {
    return `${size} B`
  }

  return '0 B'
}
