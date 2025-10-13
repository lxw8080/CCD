# 文档索引

快速找到您需要的文档。

## 🚀 快速开始

### 我想要快速运行系统
👉 [QUICK_START.md](QUICK_START.md) - 5分钟快速启动指南

### 我想了解项目概况
👉 [README.md](README.md) - 项目总览和介绍

### 我想了解项目完成情况
👉 [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - 项目完成总结

## 📖 开发文档

### 后端开发
- [backend/README.md](backend/README.md) - 后端开发指南
- Django项目配置: `backend/config/settings.py`
- API路由: `backend/config/urls.py`

#### 模块文档
- **用户模块**: `backend/apps/users/`
  - 模型: `models.py`
  - 视图: `views.py`
  - 序列化器: `serializers.py`

- **客户模块**: `backend/apps/customers/`
  - 模型: `models.py`
  - 视图: `views.py` (含完整性检查)
  - 序列化器: `serializers.py`

- **资料模块**: `backend/apps/documents/`
  - 模型: `models.py`
  - 视图: `views.py` (含上传功能)
  - 序列化器: `serializers.py`

### 前端开发
- [frontend/README.md](frontend/README.md) - 前端开发指南
- Vite配置: `frontend/vite.config.js`
- 路由配置: `frontend/src/router/index.js`

#### 页面文档
- **PC端页面**: `frontend/src/views/pc/`
  - CustomerList.vue - 客户列表
  - CustomerForm.vue - 客户表单
  - CustomerDetail.vue - 客户详情

- **移动端页面**: `frontend/src/views/mobile/`
  - CustomerList.vue - 客户列表
  - CustomerForm.vue - 客户表单
  - CustomerDetail.vue - 客户详情

- **通用页面**: `frontend/src/views/`
  - Login.vue - 登录页面

#### API接口
- `frontend/src/api/auth.js` - 认证接口
- `frontend/src/api/customer.js` - 客户接口
- `frontend/src/api/document.js` - 资料接口

#### 工具函数
- `frontend/src/utils/device.js` - 设备检测
- `frontend/src/utils/request.js` - HTTP请求
- `frontend/src/utils/image.js` - 图片处理

## 🏗️ 架构文档

### 项目结构
👉 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - 完整的项目结构说明

### 技术架构
详见 [README.md](README.md) 中的技术架构章节

### 数据库设计
详见 [README.md](README.md) 中的数据库设计章节

### API设计
详见 [README.md](README.md) 中的API接口设计章节

## 🚢 部署文档

### 部署指南
👉 [deployment/README.md](deployment/README.md) - 完整的部署文档

### 配置文件
- [deployment/nginx.conf](deployment/nginx.conf) - Nginx配置
- [deployment/gunicorn_config.py](deployment/gunicorn_config.py) - Gunicorn配置
- [deployment/systemd/ccd-backend.service](deployment/systemd/ccd-backend.service) - Systemd服务

### 部署脚本
- [deployment/deploy.sh](deployment/deploy.sh) - 自动化部署脚本
- [start-dev.sh](start-dev.sh) / [start-dev.bat](start-dev.bat) - 开发环境启动
- [stop-dev.sh](stop-dev.sh) - 开发环境停止

## 📝 其他文档

### 更新日志
👉 [CHANGELOG.md](CHANGELOG.md) - 版本更新记录

### 环境配置
- `backend/.env.example` - 后端环境变量示例
- `frontend/vite.config.js` - 前端代理配置

### Git配置
- [.gitignore](.gitignore) - Git忽略文件配置

## 🔍 按场景查找

### 我是新手，第一次接触项目
1. 阅读 [README.md](README.md) 了解项目
2. 查看 [QUICK_START.md](QUICK_START.md) 快速开始
3. 参考 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) 了解结构

### 我要开发新功能
1. 查看 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) 了解代码组织
2. 后端: 参考 [backend/README.md](backend/README.md)
3. 前端: 参考 [frontend/README.md](frontend/README.md)

### 我要部署到服务器
1. 阅读 [deployment/README.md](deployment/README.md) 完整部署指南
2. 准备配置文件（Nginx、Gunicorn、Systemd）
3. 执行部署脚本或手动部署

### 我遇到了问题
1. 检查 [QUICK_START.md](QUICK_START.md) 中的常见问题
2. 查看 [deployment/README.md](deployment/README.md) 中的故障排除
3. 查看终端错误日志

### 我想了解实现细节
1. 后端模型: `backend/apps/*/models.py`
2. 后端视图: `backend/apps/*/views.py`
3. 前端页面: `frontend/src/views/`
4. API接口: `frontend/src/api/`

## 📊 文档清单

### 主要文档 (8个)
✅ README.md - 项目总览  
✅ QUICK_START.md - 快速开始  
✅ PROJECT_SUMMARY.md - 项目总结  
✅ PROJECT_STRUCTURE.md - 项目结构  
✅ CHANGELOG.md - 更新日志  
✅ backend/README.md - 后端文档  
✅ frontend/README.md - 前端文档  
✅ deployment/README.md - 部署文档  

### 配置文件 (5个)
✅ backend/.env.example - 环境变量  
✅ deployment/nginx.conf - Nginx  
✅ deployment/gunicorn_config.py - Gunicorn  
✅ deployment/systemd/ccd-backend.service - Systemd  
✅ .gitignore - Git忽略  

### 脚本文件 (4个)
✅ start-dev.sh / start-dev.bat - 启动脚本  
✅ stop-dev.sh - 停止脚本  
✅ deployment/deploy.sh - 部署脚本  

## 🎯 推荐阅读顺序

### 初次使用
1. README.md （5分钟）
2. QUICK_START.md （10分钟）
3. 实际操作 （30分钟）

### 深入开发
1. PROJECT_STRUCTURE.md （10分钟）
2. backend/README.md （15分钟）
3. frontend/README.md （15分钟）
4. 代码阅读 （2小时）

### 生产部署
1. deployment/README.md （30分钟）
2. 配置文件编辑 （20分钟）
3. 实际部署 （1小时）

## 💡 提示

- 📌 所有文档都使用Markdown格式，可用任意文本编辑器查看
- 📌 代码中包含详细注释，建议配合代码阅读
- 📌 遇到问题先查看相关文档的"常见问题"章节
- 📌 建议使用VS Code等编辑器查看，支持Markdown预览

## 🔗 快速链接

- [项目主页](README.md)
- [快速开始](QUICK_START.md)
- [后端文档](backend/README.md)
- [前端文档](frontend/README.md)
- [部署文档](deployment/README.md)
- [项目结构](PROJECT_STRUCTURE.md)

---

📚 **提示**: 按 `Ctrl+F` (或 `Cmd+F`) 在此页面中搜索关键词

