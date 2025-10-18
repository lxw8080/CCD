<template>
  <div class="mobile-customer-list">
    <van-nav-bar title="客户资料管理" fixed>
      <template #right>
        <van-button type="primary" size="small" @click="handleLogout">
          退出
        </van-button>
      </template>
    </van-nav-bar>
    
    <div class="content">
      <van-search
        v-model="searchKeyword"
        placeholder="搜索客户姓名、身份证号、手机号"
        @search="handleSearch"
      />
      
      <van-dropdown-menu>
        <van-dropdown-item v-model="statusFilter" :options="statusOptions" @change="handleSearch" />
      </van-dropdown-menu>
      
      <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
        <van-list
          v-model:loading="loading"
          :finished="finished"
          finished-text="没有更多了"
          @load="onLoad"
        >
          <van-cell
            v-for="customer in customerList"
            :key="customer.id"
            :title="customer.name"
            :label="`${customer.phone} | ${customer.id_card}`"
            is-link
            @click="handleDetail(customer.id)"
          >
            <template #right-icon>
              <van-tag :type="getStatusType(customer.status)">
                {{ getStatusText(customer.status) }}
              </van-tag>
            </template>
          </van-cell>
        </van-list>
      </van-pull-refresh>
      
      <van-empty v-if="!loading && customerList.length === 0" description="暂无数据" />
    </div>
    
    <van-button
      type="primary"
      size="large"
      round
      class="add-button"
      @click="handleCreate"
    >
      <van-icon name="plus" /> 新建客户
    </van-button>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { getCustomers } from '@/api/customer'
import { showToast } from 'vant'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const refreshing = ref(false)
const finished = ref(false)
const customerList = ref([])
const searchKeyword = ref('')
const statusFilter = ref('')

const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

const statusOptions = [
  { text: '全部状态', value: '' },
  { text: '资料收集中', value: 'pending' },
  { text: '资料已齐全', value: 'complete' },
  { text: '审核中', value: 'reviewing' },
  { text: '已通过', value: 'approved' },
  { text: '已拒绝', value: 'rejected' }
]

const statusMap = {
  pending: { text: '收集中', type: 'default' },
  complete: { text: '已齐全', type: 'success' },
  completed: { text: '已齐全', type: 'success' }, // 兼容数据库中的 completed
  reviewing: { text: '审核中', type: 'warning' },
  in_progress: { text: '审核中', type: 'warning' }, // 兼容数据库中的 in_progress
  approved: { text: '已通过', type: 'success' },
  rejected: { text: '已拒绝', type: 'danger' }
}

const getStatusText = (status) => statusMap[status]?.text || status
const getStatusType = (status) => statusMap[status]?.type || 'default'

const fetchCustomers = async (append = false) => {
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize
    }
    
    if (searchKeyword.value) {
      params.search = searchKeyword.value
    }
    
    if (statusFilter.value) {
      params.status = statusFilter.value
    }
    
    const response = await getCustomers(params)
    
    if (append) {
      customerList.value = [...customerList.value, ...(response.results || [])]
    } else {
      customerList.value = response.results || []
    }
    
    pagination.total = response.count || 0
    
    // 判断是否还有更多数据
    if (customerList.value.length >= pagination.total) {
      finished.value = true
    }
  } catch (error) {
    showToast('获取客户列表失败')
  }
}

const onLoad = async () => {
  if (refreshing.value) {
    customerList.value = []
    refreshing.value = false
    pagination.page = 1
  }
  
  await fetchCustomers(pagination.page > 1)
  loading.value = false
  
  if (customerList.value.length < pagination.total) {
    pagination.page++
  }
}

const onRefresh = () => {
  finished.value = false
  loading.value = true
  pagination.page = 1
  onLoad()
}

const handleSearch = () => {
  finished.value = false
  loading.value = true
  pagination.page = 1
  customerList.value = []
  onLoad()
}

const handleCreate = () => {
  router.push('/customers/create')
}

const handleDetail = (id) => {
  router.push(`/customers/${id}`)
}

const handleLogout = async () => {
  await userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.mobile-customer-list {
  min-height: 100vh;
  background: #f7f8fa;
  padding-bottom: 80px;
}

.content {
  padding-top: 46px;
}

.add-button {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 999;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
</style>

