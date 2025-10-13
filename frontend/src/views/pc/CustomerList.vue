<template>
  <div class="customer-list-container">
    <el-container>
      <el-header class="header">
        <div class="header-content">
          <h2>客户资料管理</h2>
          <div class="user-info">
            <span>{{ userStore.username }}</span>
            <el-button type="text" @click="handleLogout">退出</el-button>
          </div>
        </div>
      </el-header>
      
      <el-main>
        <div class="toolbar">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索客户姓名、身份证号、手机号"
            style="width: 300px"
            clearable
            @change="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          
          <el-select
            v-model="statusFilter"
            placeholder="状态筛选"
            style="width: 150px; margin-left: 10px"
            clearable
            @change="handleSearch"
          >
            <el-option label="资料收集中" value="pending" />
            <el-option label="资料已齐全" value="complete" />
            <el-option label="审核中" value="reviewing" />
            <el-option label="已通过" value="approved" />
            <el-option label="已拒绝" value="rejected" />
          </el-select>
          
          <el-button type="primary" @click="handleCreate">
            <el-icon><Plus /></el-icon>
            新建客户
          </el-button>
        </div>
        
        <el-table
          v-loading="loading"
          :data="customerList"
          style="width: 100%; margin-top: 20px"
          stripe
        >
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="name" label="姓名" width="120" />
          <el-table-column prop="id_card" label="身份证号" width="180" />
          <el-table-column prop="phone" label="手机号" width="130" />
          <el-table-column prop="status" label="状态" width="120">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)">
                {{ getStatusText(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_by_name" label="创建人" width="100" />
          <el-table-column prop="created_at" label="创建时间" width="180" />
          <el-table-column label="操作" fixed="right" width="200">
            <template #default="{ row }">
              <el-button type="primary" size="small" @click="handleDetail(row.id)">
                详情
              </el-button>
              <el-button type="warning" size="small" @click="handleEdit(row.id)">
                编辑
              </el-button>
              <el-button type="danger" size="small" @click="handleDelete(row.id)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <el-pagination
          v-if="pagination.total > 0"
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          style="margin-top: 20px; justify-content: center"
          @current-change="fetchCustomers"
          @size-change="fetchCustomers"
        />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { getCustomers, deleteCustomer } from '@/api/customer'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const customerList = ref([])
const searchKeyword = ref('')
const statusFilter = ref('')

const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

const statusMap = {
  pending: { text: '资料收集中', type: 'info' },
  complete: { text: '资料已齐全', type: 'success' },
  reviewing: { text: '审核中', type: 'warning' },
  approved: { text: '已通过', type: 'success' },
  rejected: { text: '已拒绝', type: 'danger' }
}

const getStatusText = (status) => statusMap[status]?.text || status
const getStatusType = (status) => statusMap[status]?.type || 'info'

const fetchCustomers = async () => {
  loading.value = true
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
    customerList.value = response.results || []
    pagination.total = response.count || 0
  } catch (error) {
    ElMessage.error('获取客户列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  fetchCustomers()
}

const handleCreate = () => {
  router.push('/customers/create')
}

const handleDetail = (id) => {
  router.push(`/customers/${id}`)
}

const handleEdit = (id) => {
  router.push(`/customers/${id}/edit`)
}

const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除这个客户吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await deleteCustomer(id)
    ElMessage.success('删除成功')
    fetchCustomers()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
    }
  }
}

const handleLogout = async () => {
  await userStore.logout()
  router.push('/login')
}

onMounted(() => {
  fetchCustomers()
})
</script>

<style scoped>
.customer-list-container {
  height: 100vh;
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

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.toolbar {
  display: flex;
  align-items: center;
  gap: 10px;
}
</style>

