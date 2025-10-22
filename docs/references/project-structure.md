# 项目结构说明

## 整体架构

```
CCD/ (客户资料收集系统)
├── backend/                    # Django后端
├── frontend/                   # Vue前端
├── deployment/                 # 部署配置
├── README.md                   # 项目说明
├── CHANGELOG.md                # 更新日志
├── start-dev.sh/.bat          # 开发环境启动脚本
└── stop-dev.sh                # 开发环境停止脚本
```

## 后端结构 (backend/)

```
backend/
├── apps/                       # 应用模块
│   ├── users/                 # 用户模块
│   │   ├── models.py          # 用户模型
│   │   ├── serializers.py     # 序列化器
│   │   ├── views.py           # 视图
│   │   ├── urls.py            # 路由
│   │   ├── admin.py           # 管理后台
│   │   └── management/        # 管理命令
│   │       └── commands/
│   │           └── create_demo_data.py
│   │
│   ├── customers/             # 客户模块
│   │   ├── models.py          # 客户模型
│   │   ├── serializers.py     # 序列化器
│   │   ├── views.py           # 视图（包含完整性检查）
│   │   ├── urls.py            # 路由
│   │   └── admin.py           # 管理后台
│   │
│   └── documents/             # 资料模块
│       ├── models.py          # 资料模型（DocumentType, Document）
│       ├── serializers.py     # 序列化器
│       ├── views.py           # 视图（上传、查询等）
│       ├── urls.py            # 路由
│       ├── admin.py           # 管理后台
│       └── management/        # 管理命令
│           └── commands/
│               └── init_document_types.py
│
├── config/                    # 项目配置
│   ├── settings.py           # Django设置
│   ├── urls.py               # 主路由
│   ├── wsgi.py               # WSGI配置
│   └── asgi.py               # ASGI配置
│
├── media/                    # 上传文件存储
│   └── documents/           # 按客户ID分类存储
│
├── staticfiles/             # 收集的静态文件
├── requirements.txt         # Python依赖
├── manage.py               # Django管理脚本
├── .env.example            # 环境变量示例
├── .gitignore             # Git忽略文件
└── README.md              # 后端说明文档
```

## 前端结构 (frontend/)

```
frontend/
├── src/
│   ├── api/                   # API接口层
│   │   ├── auth.js           # 认证接口
│   │   ├── customer.js       # 客户接口
│   │   └── document.js       # 资料接口
│   │
│   ├── components/           # 通用组件
│   │   └── (可扩展)
│   │
│   ├── router/               # 路由配置
│   │   └── index.js         # 路由定义和守卫
│   │
│   ├── store/                # Pinia状态管理
│   │   ├── user.js          # 用户状态
│   │   └── customer.js      # 客户状态
│   │
│   ├── utils/                # 工具函数
│   │   ├── device.js        # 设备检测
│   │   ├── request.js       # HTTP请求封装
│   │   └── image.js         # 图片处理工具
│   │
│   ├── views/                # 页面组件
│   │   ├── Login.vue        # 登录页（响应式）
│   │   │
│   │   ├── pc/              # PC端页面
│   │   │   ├── CustomerList.vue      # 客户列表
│   │   │   ├── CustomerForm.vue      # 客户表单
│   │   │   └── CustomerDetail.vue    # 客户详情
│   │   │
│   │   └── mobile/          # 移动端页面
│   │       ├── CustomerList.vue      # 客户列表
│   │       ├── CustomerForm.vue      # 客户表单
│   │       └── CustomerDetail.vue    # 客户详情
│   │
│   ├── App.vue              # 根组件
│   └── main.js              # 入口文件
│
├── public/                  # 公共资源
├── index.html              # HTML模板
├── vite.config.js          # Vite配置
├── package.json            # Node依赖
├── .gitignore             # Git忽略文件
└── README.md              # 前端说明文档
```

## 部署结构 (deployment/)

```
deployment/
├── nginx.conf              # Nginx配置文件
├── gunicorn_config.py     # Gunicorn配置
├── deploy.sh              # 自动化部署脚本
├── systemd/               # Systemd服务配置
│   └── ccd-backend.service
└── README.md              # 部署文档
```

## 数据流程

### 1. 用户认证流程

```
用户输入 → Login.vue 
       → auth.js (login API)
       → /api/auth/login/
       → users/views.py (login)
       → JWT Token生成
       → 存储到localStorage
       → 跳转到客户列表
```

### 2. 客户管理流程

```
客户列表 → CustomerList.vue
        → customer.js (getCustomers API)
        → /api/customers/
        → customers/views.py (CustomerViewSet)
        → 返回客户数据
        → 渲染表格/列表
```

### 3. 资料上传流程

```
选择文件 → CustomerDetail.vue
        → image.js (compressImage)
        → document.js (uploadDocument API)
        → /api/documents/upload/
        → documents/views.py (upload_document)
        → 保存文件到media/documents/
        → 创建Document记录
        → 返回文件信息
        → 刷新资料列表
```

### 4. 完整性检查流程

```
客户详情 → CustomerDetail.vue
        → customer.js (getCustomerCompleteness API)
        → /api/customers/{id}/completeness/
        → customers/views.py (completeness action)
        → 查询必需资料类型
        → 查询已上传资料
        → 计算完整度
        → 返回检查结果
        → 可视化展示
```

## 核心技术

### 后端技术栈
- **框架**: Django 4.2, Django REST Framework 3.14
- **数据库**: PostgreSQL
- **认证**: JWT (djangorestframework-simplejwt)
- **图片处理**: Pillow
- **CORS**: django-cors-headers

### 前端技术栈
- **框架**: Vue 3.3
- **构建工具**: Vite 5.0
- **路由**: Vue Router 4.2
- **状态管理**: Pinia 2.1
- **HTTP客户端**: Axios 1.6
- **PC端UI**: Element Plus 2.4
- **移动端UI**: Vant 4.8
- **图片压缩**: Compressor.js 1.2

### 开发工具
- **版本控制**: Git
- **包管理**: pip (Python), npm (Node.js)
- **代码规范**: (可扩展ESLint、Prettier、Black等)

## 关键特性

1. **响应式设计**: 根据设备自动切换PC/移动端UI
2. **JWT认证**: 安全的token认证机制
3. **图片压缩**: 自动压缩上传图片，节省带宽
4. **完整性检查**: 自动检查资料是否齐全
5. **多端协同**: 支持多设备同时操作
6. **实时同步**: 数据实时更新
7. **分页加载**: 列表数据分页显示，提升性能
8. **权限控制**: 基于角色的权限管理

## API设计规范

- **RESTful风格**: 使用标准HTTP方法（GET、POST、PUT、DELETE）
- **JSON格式**: 统一使用JSON数据格式
- **分页**: 列表接口支持分页（page, page_size）
- **筛选**: 支持查询参数筛选（search, status等）
- **错误处理**: 统一的错误响应格式

## 数据库设计

### 表关系
```
User (用户)
  ↓ created_by
Customer (客户)
  ↓ customer
Document (资料)
  ↓ document_type
DocumentType (资料类型)
```

## 安全考虑

1. **认证**: JWT token认证
2. **密码**: 使用Django的密码哈希
3. **CORS**: 配置跨域访问白名单
4. **文件上传**: 限制文件类型和大小
5. **SQL注入**: 使用ORM防止SQL注入
6. **XSS**: 前端自动转义
7. **CSRF**: Django内置CSRF保护

## 性能优化

1. **数据库查询优化**: 使用select_related和prefetch_related
2. **分页**: 大数据量分页加载
3. **图片压缩**: 减少上传文件大小
4. **静态文件缓存**: Nginx配置静态文件缓存
5. **Gzip压缩**: Nginx开启Gzip
6. **前端路由懒加载**: 按需加载页面组件

## 扩展方向

1. **云存储**: 接入阿里云OSS/腾讯云COS
2. **OCR识别**: 自动识别证件信息
3. **工作流**: 审批流程管理
4. **通知**: 邮件/短信通知
5. **报表**: 数据统计和导出
6. **日志**: 操作日志记录
7. **Docker**: 容器化部署
8. **CI/CD**: 自动化测试和部署

