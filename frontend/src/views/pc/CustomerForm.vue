<template>
  <div class="customer-form-container">
    <el-container>
      <el-header class="header">
        <div class="header-content">
          <h2>{{ isEdit ? '编辑客户' : '新建客户' }}</h2>
          <el-button @click="handleBack">返回</el-button>
        </div>
      </el-header>
      
      <el-main>
        <el-card>
          <el-form
            ref="formRef"
            :model="form"
            :rules="rules"
            label-width="120px"
            style="max-width: 600px"
          >
            <el-form-item label="姓名" prop="name">
              <el-input v-model="form.name" placeholder="请输入姓名" />
            </el-form-item>
            
            <el-form-item label="身份证号" prop="id_card">
              <el-input v-model="form.id_card" placeholder="请输入身份证号" />
            </el-form-item>
            
            <el-form-item label="手机号" prop="phone">
              <el-input v-model="form.phone" placeholder="请输入手机号" />
            </el-form-item>
            
            <el-form-item label="地址" prop="address">
              <el-input
                v-model="form.address"
                type="textarea"
                :rows="3"
                placeholder="请输入地址"
              />
            </el-form-item>
            
            <el-form-item label="状态" prop="status">
              <el-select v-model="form.status" placeholder="请选择状态">
                <el-option label="资料收集中" value="pending" />
                <el-option label="资料已齐全" value="complete" />
                <el-option label="审核中" value="reviewing" />
                <el-option label="已通过" value="approved" />
                <el-option label="已拒绝" value="rejected" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="备注" prop="remarks">
              <el-input
                v-model="form.remarks"
                type="textarea"
                :rows="4"
                placeholder="请输入备注"
              />
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" :loading="loading" @click="handleSubmit">
                保存
              </el-button>
              <el-button @click="handleBack">取消</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getCustomer, createCustomer, updateCustomer } from '@/api/customer'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()

const formRef = ref(null)
const loading = ref(false)
const isEdit = computed(() => !!route.params.id)

const form = reactive({
  name: '',
  id_card: '',
  phone: '',
  address: '',
  status: 'pending',
  remarks: ''
})

const rules = {
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  id_card: [
    { required: true, message: '请输入身份证号', trigger: 'blur' },
    { pattern: /^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$/, message: '身份证号格式不正确', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ]
}

const fetchCustomerDetail = async () => {
  if (!isEdit.value) return
  
  loading.value = true
  try {
    const customer = await getCustomer(route.params.id)
    Object.assign(form, {
      name: customer.name,
      id_card: customer.id_card,
      phone: customer.phone,
      address: customer.address || '',
      status: customer.status,
      remarks: customer.remarks || ''
    })
  } catch (error) {
    ElMessage.error('获取客户信息失败')
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  
  loading.value = true
  try {
    if (isEdit.value) {
      await updateCustomer(route.params.id, form)
      ElMessage.success('更新成功')
    } else {
      await createCustomer(form)
      ElMessage.success('创建成功')
    }
    router.push('/customers')
  } catch (error) {
    ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
  } finally {
    loading.value = false
  }
}

const handleBack = () => {
  router.back()
}

onMounted(() => {
  fetchCustomerDetail()
})
</script>

<style scoped>
.customer-form-container {
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
</style>

