import { defineStore } from 'pinia'
import { login, logout, getCurrentUser } from '@/api/auth'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('access_token') || '',
    refreshToken: localStorage.getItem('refresh_token') || '',
    userInfo: JSON.parse(localStorage.getItem('user_info') || 'null')
  }),
  
  getters: {
    isLoggedIn: (state) => !!state.token,
    username: (state) => state.userInfo?.username || '',
    role: (state) => state.userInfo?.role || ''
  },
  
  actions: {
    // 登录
    async login(credentials) {
      try {
        const response = await login(credentials)
        this.token = response.access
        this.refreshToken = response.refresh
        this.userInfo = response.user
        
        // 保存到localStorage
        localStorage.setItem('access_token', response.access)
        localStorage.setItem('refresh_token', response.refresh)
        localStorage.setItem('user_info', JSON.stringify(response.user))
        
        return response
      } catch (error) {
        throw error
      }
    },
    
    // 登出
    async logout() {
      try {
        await logout({ refresh: this.refreshToken })
      } catch (error) {
        console.error('登出失败:', error)
      } finally {
        this.token = ''
        this.refreshToken = ''
        this.userInfo = null
        
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user_info')
      }
    },
    
    // 获取用户信息
    async fetchUserInfo() {
      try {
        const userInfo = await getCurrentUser()
        this.userInfo = userInfo
        localStorage.setItem('user_info', JSON.stringify(userInfo))
        return userInfo
      } catch (error) {
        throw error
      }
    }
  }
})

