# 客户资料收集系统 - 后端

基于 Django + Django REST Framework 的后端API服务。

## 技术栈

- Django 4.2
- Django REST Framework 3.14
- PostgreSQL
- JWT 认证

## 安装步骤

### 1. 创建虚拟环境

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

编辑 `.env` 文件，配置数据库连接等信息。

### 4. 创建数据库

在PostgreSQL中创建数据库：

```sql
CREATE DATABASE ccd_db;
```

### 5. 运行数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. 初始化资料类型数据

```bash
python manage.py init_document_types
```

### 7. 创建超级管理员

```bash
python manage.py createsuperuser
```

### 8. 运行开发服务器

```bash
python manage.py runserver
```

服务将在 http://127.0.0.1:8000 启动。

## API 文档

### 认证接口

- `POST /api/auth/login/` - 用户登录
- `POST /api/auth/logout/` - 用户登出
- `GET /api/auth/me/` - 获取当前用户信息
- `POST /api/auth/register/` - 用户注册

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
- `POST /api/documents/batch-upload/` - 批量上传资料
- `GET /api/documents/{id}/` - 资料详情
- `DELETE /api/documents/{id}/` - 删除资料

## 目录结构

```
backend/
├── apps/
│   ├── users/          # 用户模块
│   ├── customers/      # 客户模块
│   └── documents/      # 资料模块
├── config/             # 项目配置
├── media/              # 上传文件存储
├── manage.py
└── requirements.txt
```

## 注意事项

1. 确保PostgreSQL服务已启动
2. 生产环境需要修改 SECRET_KEY 和 DEBUG 设置
3. 上传的文件存储在 media/ 目录下
4. JWT token 有效期为1天

