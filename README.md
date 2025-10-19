# 客户资料收集系统 (CCD)

一个用于信贷公司的多端协同客户资料收集管理系统，支持PC和移动端同时操作，实现高效的资料收集、管理和审核流程。

## 项目简介

本系统解决了信贷公司在客户资料收集过程中的痛点：
- ✅ 多端协同：支持手机拍照、电脑截图、扫描仪扫描等多种方式上传
- ✅ 实时同步：多个设备可以同时为同一客户补充资料
- ✅ 自动检查：系统自动检查资料完整性，提示缺失资料
- ✅ 降本增效：无需人工归集整理，系统自动分类管理

## 技术架构

### 后端
- **框架**: Django 4.2 + Django REST Framework
- **数据库**: PostgreSQL
- **认证**: JWT Token
- **文件处理**: Pillow

### 前端
- **框架**: Vue 3 + Vite
- **PC端UI**: Element Plus
- **移动端UI**: Vant
- **状态管理**: Pinia
- **HTTP客户端**: Axios
- **图片处理**: Compressor.js

### 部署
- **Web服务器**: Nginx
- **应用服务器**: Gunicorn
- **平台**: 云服务器（阿里云/腾讯云）

## 核心功能

### 1. 用户认证
- JWT token认证机制
- 角色权限管理（管理员、客服人员、审核人员）
- 登录/登出功能

### 2. 客户管理
- 创建客户档案
- 客户信息维护
- 客户列表查询（支持搜索、筛选）
- 客户状态跟踪

### 3. 资料上传
- 多图片批量上传
- 支持拖拽上传（PC端）
- 支持拍照上传（移动端）
- 自动图片压缩
- 资料类型分类管理

### 4. 资料完整性检查
- 预设必要资料清单
- 自动检查资料是否齐全
- 缺失资料实时提醒
- 完整度可视化展示

### 5. 响应式设计
- PC端：表格列表 + 详情页面
- 移动端：卡片列表 + 优化的操作界面
- 自动适配不同设备

## 📚 文档导航

### 快速链接
- **[快速开始指南](QUICK_START.md)** - 快速搭建开发环境
- **[完整用户手册](docs/guides/USER_GUIDE.md)** - 系统使用指南
- **[文档中心](docs/README.md)** - 所有文档的导航
- **[更新日志](CHANGELOG.md)** - 版本历史
- **[项目结构](PROJECT_STRUCTURE.md)** - 代码结构说明

### 按角色查找
- **用户**: [用户使用指南](docs/guides/USER_GUIDE.md)
- **开发者**: [后端文档](backend/README.md) | [前端文档](frontend/README.md)
- **运维**: [部署文档](deployment/README.md)

---

## 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+

### 后端设置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
copy .env.example .env  # 编辑.env文件配置数据库

# 创建数据库（在PostgreSQL中）
# CREATE DATABASE ccd_db;

# 运行数据库迁移
python manage.py makemigrations
python manage.py migrate

# 初始化资料类型数据
python manage.py init_document_types

# 创建超级管理员
python manage.py createsuperuser

# 运行开发服务器
python manage.py runserver
```

后端服务将在 http://127.0.0.1:8000 启动。

### 前端设置

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 运行开发服务器
npm run dev
```

前端应用将在 http://localhost:5173 启动。

### 访问系统

1. 打开浏览器访问 http://localhost:5173
2. 使用创建的超级管理员账号登录
3. 开始使用系统

## 项目结构

```
CCD/
├── backend/                 # Django后端
│   ├── apps/
│   │   ├── users/          # 用户模块
│   │   ├── customers/      # 客户模块
│   │   └── documents/      # 资料模块
│   ├── config/             # 项目配置
│   ├── media/              # 上传文件存储
│   ├── requirements.txt    # Python依赖
│   └── manage.py
│
├── frontend/               # Vue前端
│   ├── src/
│   │   ├── api/           # API接口
│   │   ├── components/    # 组件
│   │   ├── router/        # 路由
│   │   ├── store/         # 状态管理
│   │   ├── utils/         # 工具函数
│   │   └── views/         # 页面
│   │       ├── pc/        # PC端页面
│   │       └── mobile/    # 移动端页面
│   ├── package.json       # Node依赖
│   └── vite.config.js     # Vite配置
│
└── README.md              # 项目说明
```

## API接口文档

### 认证接口
- `POST /api/auth/login/` - 用户登录
- `POST /api/auth/logout/` - 用户登出
- `GET /api/auth/me/` - 获取当前用户信息

### 客户接口
- `GET /api/customers/` - 客户列表
- `POST /api/customers/` - 创建客户
- `GET /api/customers/{id}/` - 客户详情
- `PUT /api/customers/{id}/` - 更新客户
- `DELETE /api/customers/{id}/` - 删除客户
- `GET /api/customers/{id}/completeness/` - 资料完整性检查

### 资料接口
- `GET /api/documents/types/` - 资料类型列表
- `GET /api/documents/` - 资料列表
- `POST /api/documents/upload/` - 上传资料
- `POST /api/documents/batch-upload/` - 批量上传
- `DELETE /api/documents/{id}/` - 删除资料

## 数据库设计

### User（用户表）
- 基于Django AbstractUser
- 扩展字段：role（角色）、phone（手机号）

### Customer（客户表）
- 基本信息：姓名、身份证号、手机号、地址
- 状态字段：pending/complete/reviewing/approved/rejected
- 关联字段：created_by（创建人）

### DocumentType（资料类型表）
- 资料类型名称
- 是否必需标识
- 排序顺序

### Document（资料表）
- 关联客户和资料类型
- 文件存储路径
- 上传人和上传时间
- 审核状态

## 生产部署

### Nginx配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # 前端静态文件
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    
    # 后端API
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # 媒体文件
    location /media {
        alias /path/to/backend/media;
    }
    
    # 静态文件
    location /static {
        alias /path/to/backend/staticfiles;
    }
}
```

### 使用Gunicorn运行后端

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

## 常见问题

### 1. 数据库连接失败
检查 `.env` 文件中的数据库配置是否正确，确保PostgreSQL服务已启动。

### 2. 前端无法访问后端API
检查Vite配置中的代理设置，确保后端服务正在运行。

### 3. 图片上传失败
检查后端 `media` 目录的写入权限，确保文件大小不超过限制（10MB）。

### 4. 移动端无法拍照
确保使用HTTPS协议或localhost，现代浏览器要求安全上下文才能访问摄像头。

## 后续优化建议

- [ ] 接入阿里云OSS存储图片
- [ ] 添加OCR识别功能自动提取证件信息
- [ ] 实现工作流审批功能
- [ ] 添加消息通知（邮件/短信）
- [ ] 实现统计报表功能
- [ ] 添加数据导出功能
- [ ] 支持Docker一键部署

## 开发团队

本项目用于信贷公司降本增效，提升客户资料收集的效率和准确性。

## 许可证

本项目仅供学习和内部使用。

