# 快速参考 - PC 端 PDF 预览修复

**日期**: 2025-10-19  
**版本**: 1.0

---

## 🔧 修复内容速览

### 问题 1: Element Plus 图标未导入

**症状**: 浏览器控制台出现 "Failed to resolve component" 警告

**修复**:

#### Login.vue
```javascript
import { User, Lock } from '@element-plus/icons-vue'
```

#### CustomerDetail.vue
```javascript
import { Plus } from '@element-plus/icons-vue'
```

#### CustomerList.vue
```javascript
import { Search, Plus } from '@element-plus/icons-vue'
```

---

### 问题 2: CORS 配置不支持 3001 端口

**症状**: 前端在 3001 端口运行，但后端 CORS 配置不允许

**修复**: `backend/config/settings.py`

```python
CORS_ALLOWED_ORIGINS = os.getenv(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:5173,http://127.0.0.1:5173,'
    'http://localhost:3000,http://127.0.0.1:3000,'
    'http://localhost:3001,http://127.0.0.1:3001'
).split(',')
```

---

### 问题 3: PDF 预览功能

**状态**: ✅ 正常工作

**验证**:
- PDF 文件上传成功
- 文件 URL 可以访问
- PDF.js worker 配置正确

---

## 📊 修改统计

| 项目 | 数量 |
|------|------|
| 修改文件 | 4 个 |
| 新增导入 | 5 个 |
| 修改行数 | ~10 行 |

---

## ✅ 验证清单

- [x] Element Plus 图标正常显示
- [x] CORS 跨域请求正常
- [x] PDF 文件上传成功
- [x] PDF 文件 URL 可访问
- [x] 浏览器控制台无错误

---

## 🚀 启动服务

```bash
# 后端
cd backend
python manage.py runserver

# 前端
cd frontend
npm run dev
```

**访问地址**:
- 前端: http://127.0.0.1:3001
- 后端: http://127.0.0.1:8000

---

## 🧪 测试步骤

### 测试 PDF 预览

1. 打开浏览器访问 http://127.0.0.1:3001
2. 使用 admin/admin123 登录
3. 进入客户详情页面
4. 上传 PDF 文件
5. 点击预览按钮
6. 验证 PDF 正常显示

### 检查浏览器控制台

1. 打开开发者工具 (F12)
2. 检查 Console 标签页
3. 确保没有错误信息
4. 确保没有警告信息

---

## 📝 文件清单

### 修改的文件

1. `frontend/src/views/Login.vue`
2. `frontend/src/views/pc/CustomerDetail.vue`
3. `frontend/src/views/pc/CustomerList.vue`
4. `backend/config/settings.py`

### 资源文件

- `frontend/public/pdf.worker.min.mjs` (已存在)

---

## 💡 关键要点

1. **Element Plus 图标**:
   - 从 `@element-plus/icons-vue` 导入
   - 在 `<el-icon>` 中使用

2. **CORS 配置**:
   - 支持多个源
   - 用逗号分隔

3. **PDF.js**:
   - 使用本地 worker 文件
   - 配置: `GlobalWorkerOptions.workerSrc = '/pdf.worker.min.mjs'`

---

## 🎯 预期效果

✅ 前端界面图标正常显示  
✅ PDF 文件可以上传和预览  
✅ 跨域请求正常  
✅ 浏览器控制台无错误

---

**快速参考完成** ✅

