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

            <!-- 动态自定义字段 -->
            <template v-for="field in customFields" :key="field.id">
              <el-form-item
                :label="field.name"
                :prop="`custom_fields.${field.id}`"
                :rules="getFieldRules(field)"
              >
                <!-- 文本输入 -->
                <el-input
                  v-if="field.field_type === 'text' || field.field_type === 'email' || field.field_type === 'url'"
                  v-model="form.custom_fields[field.id]"
                  :placeholder="field.placeholder || `请输入${field.name}`"
                  :type="field.field_type === 'email' ? 'email' : field.field_type === 'url' ? 'url' : 'text'"
                />

                <!-- 数字输入 -->
                <el-input-number
                  v-else-if="field.field_type === 'number'"
                  v-model="form.custom_fields[field.id]"
                  :placeholder="field.placeholder || `请输入${field.name}`"
                  :min="field.min_value"
                  :max="field.max_value"
                  style="width: 100%"
                />

                <!-- 日期选择 -->
                <el-date-picker
                  v-else-if="field.field_type === 'date'"
                  v-model="form.custom_fields[field.id]"
                  type="date"
                  :placeholder="field.placeholder || `请选择${field.name}`"
                  format="YYYY-MM-DD"
                  value-format="YYYY-MM-DD"
                  style="width: 100%"
                />

                <!-- 下拉选择 -->
                <el-select
                  v-else-if="field.field_type === 'select'"
                  v-model="form.custom_fields[field.id]"
                  :placeholder="field.placeholder || `请选择${field.name}`"
                  style="width: 100%"
                >
                  <el-option
                    v-for="option in field.options"
                    :key="option"
                    :label="option"
                    :value="option"
                  />
                </el-select>

                <!-- 多行文本 -->
                <el-input
                  v-else-if="field.field_type === 'textarea'"
                  v-model="form.custom_fields[field.id]"
                  type="textarea"
                  :rows="3"
                  :placeholder="field.placeholder || `请输入${field.name}`"
                />

                <!-- 手机号 -->
                <el-input
                  v-else-if="field.field_type === 'phone'"
                  v-model="form.custom_fields[field.id]"
                  :placeholder="field.placeholder || `请输入${field.name}`"
                  maxlength="11"
                />

                <!-- 默认文本输入 -->
                <el-input
                  v-else
                  v-model="form.custom_fields[field.id]"
                  :placeholder="field.placeholder || `请输入${field.name}`"
                />

                <template v-if="field.help_text" #help>
                  <span class="help-text">{{ field.help_text }}</span>
                </template>
              </el-form-item>
            </template>

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
import { getCustomer, createCustomer, updateCustomer, getCustomFields } from '@/api/customer'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()

const formRef = ref(null)
const loading = ref(false)
const isEdit = computed(() => !!route.params.id)
const customFields = ref([])

const form = reactive({
  name: '',
  id_card: '',
  phone: '',
  address: '',
  status: 'pending',
  custom_fields: {}
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

// 获取字段验证规则
const getFieldRules = (field) => {
  const fieldRules = []

  if (field.is_required) {
    fieldRules.push({
      required: true,
      message: `请输入${field.name}`,
      trigger: field.field_type === 'select' || field.field_type === 'date' ? 'change' : 'blur'
    })
  }

  // 文本长度验证
  if (field.min_length || field.max_length) {
    fieldRules.push({
      min: field.min_length || 0,
      max: field.max_length || 999999,
      message: `长度在 ${field.min_length || 0} 到 ${field.max_length || 999999} 个字符`,
      trigger: 'blur'
    })
  }

  // 数字范围验证
  if (field.field_type === 'number' && (field.min_value || field.max_value)) {
    fieldRules.push({
      validator: (rule, value, callback) => {
        if (value === '' || value === null || value === undefined) {
          callback()
          return
        }
        const num = Number(value)
        if (field.min_value && num < field.min_value) {
          callback(new Error(`最小值为 ${field.min_value}`))
        } else if (field.max_value && num > field.max_value) {
          callback(new Error(`最大值为 ${field.max_value}`))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    })
  }

  // 正则表达式验证
  if (field.regex_pattern) {
    fieldRules.push({
      pattern: new RegExp(field.regex_pattern),
      message: `${field.name}格式不正确`,
      trigger: 'blur'
    })
  }

  // 特定类型验证
  if (field.field_type === 'email') {
    fieldRules.push({
      type: 'email',
      message: '请输入正确的邮箱地址',
      trigger: 'blur'
    })
  } else if (field.field_type === 'phone') {
    fieldRules.push({
      pattern: /^1[3-9]\d{9}$/,
      message: '请输入正确的手机号',
      trigger: 'blur'
    })
  } else if (field.field_type === 'url') {
    fieldRules.push({
      type: 'url',
      message: '请输入正确的网址',
      trigger: 'blur'
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
      status: customer.status
    })

    // 填充自定义字段值
    if (customer.custom_field_values && customer.custom_field_values.length > 0) {
      customer.custom_field_values.forEach(fieldValue => {
        form.custom_fields[fieldValue.custom_field] = fieldValue.value
      })
    }
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

onMounted(async () => {
  await fetchCustomFields()
  await fetchCustomerDetail()
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

.help-text {
  font-size: 12px;
  color: #909399;
  line-height: 1.5;
}
</style>

