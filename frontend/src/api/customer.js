import request from '@/utils/request'

/**
 * 获取客户列表
 */
export function getCustomers(params) {
  return request({
    url: '/customers/',
    method: 'get',
    params
  })
}

/**
 * 获取客户详情
 */
export function getCustomer(id) {
  return request({
    url: `/customers/${id}/`,
    method: 'get'
  })
}

/**
 * 创建客户
 */
export function createCustomer(data) {
  return request({
    url: '/customers/',
    method: 'post',
    data
  })
}

/**
 * 更新客户
 */
export function updateCustomer(id, data) {
  return request({
    url: `/customers/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 删除客户
 */
export function deleteCustomer(id) {
  return request({
    url: `/customers/${id}/`,
    method: 'delete'
  })
}

/**
 * 获取客户资料完整性
 */
export function getCustomerCompleteness(id) {
  return request({
    url: `/customers/${id}/completeness/`,
    method: 'get'
  })
}

/**
 * 获取自定义字段列表
 */
export function getCustomFields() {
  return request({
    url: '/customers/custom-fields/',
    method: 'get'
  })
}

/**
 * 获取自定义字段详情
 */
export function getCustomField(id) {
  return request({
    url: `/customers/custom-fields/${id}/`,
    method: 'get'
  })
}

/**
 * 创建自定义字段
 */
export function createCustomField(data) {
  return request({
    url: '/customers/custom-fields/',
    method: 'post',
    data
  })
}

/**
 * 更新自定义字段
 */
export function updateCustomField(id, data) {
  return request({
    url: `/customers/custom-fields/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 删除自定义字段
 */
export function deleteCustomField(id) {
  return request({
    url: `/customers/custom-fields/${id}/`,
    method: 'delete'
  })
}

