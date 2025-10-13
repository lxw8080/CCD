import axios from 'axios'
import { isMobile } from './device'

// 创建axios实例
const request = axios.create({
  baseURL: '/api',
  timeout: 30000
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    // 从localStorage获取token
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('响应错误:', error)
    
    if (error.response) {
      const { status } = error.response
      
      // 401 未授权，跳转到登录页
      if (status === 401) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user_info')
        window.location.href = '/login'
      }
      
      // 显示错误消息
      const message = error.response.data?.error || error.response.data?.detail || '请求失败'
      
      if (isMobile()) {
        // 移动端使用 Vant Toast
        import('vant').then(({ showToast }) => {
          showToast(message)
        })
      } else {
        // PC端使用 Element Plus Message
        import('element-plus').then(({ ElMessage }) => {
          ElMessage.error(message)
        })
      }
    }
    
    return Promise.reject(error)
  }
)

export default request

