<template>
  <div class="login-container" :class="{ 'mobile': isMobileDevice }">
    <div class="login-box">
      <h1 class="title">客户资料收集系统</h1>
      
      <!-- PC端登录表单 -->
      <el-form
        v-if="!isMobileDevice"
        ref="loginFormRef"
        :model="loginForm"
        :rules="rules"
        class="login-form"
        @submit.prevent="handleLogin"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            size="large"
          >
            <template #prefix>
              <el-icon><User /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            size="large"
            @keyup.enter="handleLogin"
          >
            <template #prefix>
              <el-icon><Lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            style="width: 100%"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
      
      <!-- 移动端登录表单 -->
      <van-form v-else @submit="handleLogin">
        <van-cell-group inset>
          <van-field
            v-model="loginForm.username"
            name="username"
            label="用户名"
            placeholder="请输入用户名"
            :rules="[{ required: true, message: '请输入用户名' }]"
          />
          <van-field
            v-model="loginForm.password"
            type="password"
            name="password"
            label="密码"
            placeholder="请输入密码"
            :rules="[{ required: true, message: '请输入密码' }]"
          />
        </van-cell-group>
        
        <div style="margin: 16px;">
          <van-button
            round
            block
            type="primary"
            native-type="submit"
            :loading="loading"
          >
            登录
          </van-button>
        </div>
      </van-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { isMobile } from '@/utils/device'
import { User, Lock } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()
const isMobileDevice = isMobile()

const loginFormRef = ref(null)
const loading = ref(false)

const loginForm = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!isMobileDevice && loginFormRef.value) {
    const valid = await loginFormRef.value.validate().catch(() => false)
    if (!valid) return
  }
  
  loading.value = true
  
  try {
    await userStore.login({
      username: loginForm.username,
      password: loginForm.password
    })
    
    if (isMobileDevice) {
      const { showToast } = await import('vant')
      showToast({ message: '登录成功', type: 'success' })
    } else {
      const { ElMessage } = await import('element-plus')
      ElMessage.success('登录成功')
    }
    
    router.push('/customers')
  } catch (error) {
    console.error('登录失败:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-box {
  width: 100%;
  max-width: 400px;
  padding: 40px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.mobile .login-box {
  max-width: 90%;
  padding: 30px 20px;
}

.title {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
  font-size: 24px;
}

.mobile .title {
  font-size: 20px;
  margin-bottom: 20px;
}

.login-form {
  margin-top: 20px;
}
</style>

