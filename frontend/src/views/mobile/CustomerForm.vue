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

          <!-- 动态自定义字段 -->
          <template v-for="field in customFields" :key="field.id">
            <!-- 文本输入 -->
            <van-field
              v-if="field.field_type === 'text' || field.field_type === 'email' || field.field_type === 'url'"
              v-model="form.custom_fields[field.id]"
              :name="`custom_field_${field.id}`"
              :label="field.name"
              :placeholder="field.placeholder || `请输入${field.name}`"
              :type="field.field_type === 'email' ? 'email' : field.field_type === 'url' ? 'url' : 'text'"
              :rules="getFieldRules(field)"
            />

            <!-- 数字输入 -->
            <van-field
              v-else-if="field.field_type === 'number'"
              v-model="form.custom_fields[field.id]"
              :name="`custom_field_${field.id}`"
              :label="field.name"
              type="number"
              :placeholder="field.placeholder || `请输入${field.name}`"
              :rules="getFieldRules(field)"
            />

            <!-- 日期选择 -->
            <van-field
              v-else-if="field.field_type === 'date'"
              v-model="form.custom_fields[field.id]"
              :name="`custom_field_${field.id}`"
              :label="field.name"
              :placeholder="field.placeholder || `请选择${field.name}`"
              readonly
              is-link
              @click="showDatePicker(field.id)"
              :rules="getFieldRules(field)"
            />

            <!-- 下拉选择 -->
            <van-field
              v-else-if="field.field_type === 'select'"
              v-model="form.custom_fields[field.id]"
              :name="`custom_field_${field.id}`"
              :label="field.name"
              :placeholder="field.placeholder || `请选择${field.name}`"
              readonly
              is-link
              @click="showSelectPicker(field)"
              :rules="getFieldRules(field)"
            />

            <!-- 多行文本 -->
            <van-field
              v-else-if="field.field_type === 'textarea'"
              v-model="form.custom_fields[field.id]"
              :name="`custom_field_${field.id}`"
              :label="field.name"
              type="textarea"
              rows="3"
              :placeholder="field.placeholder || `请输入${field.name}`"
              autosize
              :rules="getFieldRules(field)"
            />

            <!-- 手机号 -->
            <van-field
              v-else-if="field.field_type === 'phone'"
              v-model="form.custom_fields[field.id]"
              :name="`custom_field_${field.id}`"
              :label="field.name"
              type="tel"
              maxlength="11"
              :placeholder="field.placeholder || `请输入${field.name}`"
              :rules="getFieldRules(field)"
            />

            <!-- 默认文本输入 -->
            <van-field
              v-else
              v-model="form.custom_fields[field.id]"
              :name="`custom_field_${field.id}`"
              :label="field.name"
              :placeholder="field.placeholder || `请输入${field.name}`"
              :rules="getFieldRules(field)"
            />
          </template>
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

    <!-- 日期选择器 -->
    <van-popup v-model:show="showDatePickerPopup" position="bottom">
      <van-date-picker
        v-model="currentDate"
        @confirm="onDateConfirm"
        @cancel="showDatePickerPopup = false"
      />
    </van-popup>

    <!-- 自定义字段选择器 -->
    <van-popup v-model:show="showCustomSelectPicker" position="bottom">
      <van-picker
        :columns="currentSelectOptions"
        @confirm="onCustomSelectConfirm"
        @cancel="showCustomSelectPicker = false"
      />
    </van-popup>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getCustomer, createCustomer, updateCustomer, getCustomFields } from '@/api/customer'
import { showToast } from 'vant'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const showStatusPicker = ref(false)
const showDatePickerPopup = ref(false)
const showCustomSelectPicker = ref(false)
const isEdit = computed(() => !!route.params.id)
const customFields = ref([])
const currentDate = ref(new Date())
const currentDateFieldId = ref(null)
const currentSelectOptions = ref([])
const currentSelectFieldId = ref(null)

const form = reactive({
  name: '',
  id_card: '',
  phone: '',
  address: '',
  status: '资料收集中',
  custom_fields: {}
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

// 获取字段验证规则
const getFieldRules = (field) => {
  const fieldRules = []

  if (field.is_required) {
    fieldRules.push({
      required: true,
      message: `请输入${field.name}`
    })
  }

  // 文本长度验证
  if (field.min_length || field.max_length) {
    fieldRules.push({
      validator: (val) => {
        if (!val) return true
        const len = val.length
        if (field.min_length && len < field.min_length) {
          return `长度不能少于${field.min_length}个字符`
        }
        if (field.max_length && len > field.max_length) {
          return `长度不能超过${field.max_length}个字符`
        }
        return true
      }
    })
  }

  // 数字范围验证
  if (field.field_type === 'number' && (field.min_value || field.max_value)) {
    fieldRules.push({
      validator: (val) => {
        if (!val) return true
        const num = Number(val)
        if (field.min_value && num < field.min_value) {
          return `最小值为${field.min_value}`
        }
        if (field.max_value && num > field.max_value) {
          return `最大值为${field.max_value}`
        }
        return true
      }
    })
  }

  // 正则表达式验证
  if (field.regex_pattern) {
    fieldRules.push({
      pattern: new RegExp(field.regex_pattern),
      message: `${field.name}格式不正确`
    })
  }

  // 特定类型验证
  if (field.field_type === 'email') {
    fieldRules.push({
      pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
      message: '请输入正确的邮箱地址'
    })
  } else if (field.field_type === 'phone') {
    fieldRules.push({
      pattern: /^1[3-9]\d{9}$/,
      message: '请输入正确的手机号'
    })
  } else if (field.field_type === 'url') {
    fieldRules.push({
      pattern: /^https?:\/\/.+/,
      message: '请输入正确的网址'
    })
  }

  return fieldRules
}

// 获取自定义字段列表
const fetchCustomFields = async () => {
  try {
    const fields = await getCustomFields()
    customFields.value = fields || []

    // 只在新建模式下初始化自定义字段的默认值
    // 编辑模式下，默认值会在 fetchCustomerDetail 中从服务器加载
    if (!isEdit.value) {
      fields.forEach(field => {
        if (field.default_value && !form.custom_fields[field.id]) {
          let defaultValue = field.default_value

          // 处理动态默认值
          if (field.field_type === 'date' && defaultValue === 'TODAY') {
            // 获取当前日期，格式: YYYY-MM-DD
            const today = new Date()
            const year = today.getFullYear()
            const month = String(today.getMonth() + 1).padStart(2, '0')
            const day = String(today.getDate()).padStart(2, '0')
            defaultValue = `${year}-${month}-${day}`
          }

          form.custom_fields[field.id] = defaultValue
        }
      })
    }
  } catch (error) {
    console.error('获取自定义字段失败:', error)
  }
}

// 显示日期选择器
const showDatePicker = (fieldId) => {
  currentDateFieldId.value = fieldId
  const currentValue = form.custom_fields[fieldId]
  if (currentValue) {
    currentDate.value = new Date(currentValue)
  } else {
    currentDate.value = new Date()
  }
  showDatePickerPopup.value = true
}

// 日期选择确认
const onDateConfirm = ({ selectedValues }) => {
  const [year, month, day] = selectedValues
  const dateStr = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`
  form.custom_fields[currentDateFieldId.value] = dateStr
  showDatePickerPopup.value = false
}

// 显示自定义字段选择器
const showSelectPicker = (field) => {
  currentSelectFieldId.value = field.id
  currentSelectOptions.value = field.options || []
  showCustomSelectPicker.value = true
}

// 自定义字段选择确认
const onCustomSelectConfirm = ({ selectedOptions }) => {
  form.custom_fields[currentSelectFieldId.value] = selectedOptions[0]
  showCustomSelectPicker.value = false
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
      status: statusMap[customer.status] || '资料收集中'
    })

    // 填充自定义字段值
    if (customer.custom_field_values && customer.custom_field_values.length > 0) {
      customer.custom_field_values.forEach(fieldValue => {
        form.custom_fields[fieldValue.custom_field] = fieldValue.value
      })
    }
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

onMounted(async () => {
  await fetchCustomFields()
  await fetchCustomerDetail()
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

