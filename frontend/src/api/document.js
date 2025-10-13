import request from '@/utils/request'

/**
 * 获取资料类型列表
 */
export function getDocumentTypes() {
  return request({
    url: '/documents/types/',
    method: 'get'
  })
}

/**
 * 获取资料列表
 */
export function getDocuments(params) {
  return request({
    url: '/documents/',
    method: 'get',
    params
  })
}

/**
 * 上传资料
 */
export function uploadDocument(data) {
  return request({
    url: '/documents/upload/',
    method: 'post',
    data,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

/**
 * 批量上传资料
 */
export function batchUploadDocuments(data) {
  return request({
    url: '/documents/batch-upload/',
    method: 'post',
    data,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

/**
 * 删除资料
 */
export function deleteDocument(id) {
  return request({
    url: `/documents/${id}/`,
    method: 'delete'
  })
}

/**
 * 更新资料状态
 */
export function updateDocumentStatus(id, data) {
  return request({
    url: `/documents/${id}/`,
    method: 'patch',
    data
  })
}

