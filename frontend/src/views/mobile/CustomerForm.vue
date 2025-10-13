<template>
  <div class="mobile-customer-form">
    <van-nav-bar
      :title="isEdit ? '编辑客户' : '新建客户'"
      left-arrow
      fixed
      @click-left="handleBack"
    />
    
    <div class="content">
      <van-form @submit="handleSubmit">
        <van-cell-group inset>
          <van-field
            v-model="form.name"
            name="name"
            label="姓名"
            placeholder="请输入姓名"
            :rules="[{ required: true, message: '请输入姓名' }]"
          />
          
          <van-field
            v-model="form.id_card"
            name="id_card"
            label="身份证号"
            placeholder="请输入身份证号"
            :rules="[
              { required: true, message: '请输入身份证号' },
              { pattern: /^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$/, message: '身份证号格式不正确' }
            ]"
          />
          
          <van-field
            v-model="form.phone"
            name="phone"
            label="手机号"
            type="tel"
            placeholder="请输入手机号"
            :rules="[
              { required: true, message: '请输入手机号' },
              { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确' }
            ]"
          />
          
          <van-field
            v-model="form.address"
            name="address"
            label="地址"
            type="textarea"
            rows="3"
            placeholder="请输入地址"
            autosize
          />
          
          <van-field
            v-model="form.status"
            name="status"
            label="状态"
            placeholder="请选择状态"
            readonly
            is-link
            @click="showStatusPicker = true"
            :rules="[{ required: true, message: '请选择状态' }]"
          />
          
          <van-field
            v-model="form.remarks"
            name="remarks"
            label="备注"
            type="textarea"
            rows="4"
            placeholder="请输入备注"
            autosize
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
            保存
          </van-button>
        </div>
      </van-form>
    </div>
    
    <van-popup v-model:show="showStatusPicker" position="bottom">
      <van-picker
        :columns="statusColumns"
        @confirm="onStatusConfirm"
        @cancel="showStatusPicker = false"
      />
    </van-popup>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getCustomer, createCustomer, updateCustomer } from '@/api/customer'
import { showToast } from 'vant'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const showStatusPicker = ref(false)
const isEdit = computed(() => !!route.params.id)

const form = reactive({
  name: '',
  id_card: '',
  phone: '',
  address: '',
  status: '资料收集中',
  remarks: ''
})

const statusColumns = [
  { text: '资料收集中', value: 'pending' },
  { text: '资料已齐全', value: 'complete' },
  { text: '审核中', value: 'reviewing' },
  { text: '已通过', value: 'approved' },
  { text: '已拒绝', value: 'rejected' }
]

const statusMap = {
  pending: '资料收集中',
  complete: '资料已齐全',
  reviewing: '审核中',
  approved: '已通过',
  rejected: '已拒绝'
}

const onStatusConfirm = ({ selectedOptions }) => {
  form.status = selectedOptions[0].text
  showStatusPicker.value = false
}

const getStatusValue = (text) => {
  return Object.keys(statusMap).find(key => statusMap[key] === text) || 'pending'
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
      status: statusMap[customer.status] || '资料收集中',
      remarks: customer.remarks || ''
    })
  } catch (error) {
    showToast('获取客户信息失败')
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  loading.value = true
  try {
    const data = {
      ...form,
      status: getStatusValue(form.status)
    }
    
    if (isEdit.value) {
      await updateCustomer(route.params.id, data)
      showToast({ message: '更新成功', type: 'success' })
    } else {
      await createCustomer(data)
      showToast({ message: '创建成功', type: 'success' })
    }
    router.push('/customers')
  } catch (error) {
    showToast(isEdit.value ? '更新失败' : '创建失败')
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
.mobile-customer-form {
  min-height: 100vh;
  background: #f7f8fa;
}

.content {
  padding-top: 46px;
}
</style>

