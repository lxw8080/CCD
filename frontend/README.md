# 客户资料收集系统 - 前端

基于 Vue 3 + Vite 的响应式前端应用，支持PC和移动端访问。

## 技术栈

- Vue 3
- Vite
- Vue Router
- Pinia (状态管理)
- Element Plus (PC端UI)
- Vant (移动端UI)
- Axios (HTTP请求)
- Compressor.js (图片压缩)

## 功能特性

- 📱 响应式设计，自动适配PC和移动端
- 🔐 JWT token 认证
- 👥 客户管理（增删改查）
- 📄 资料上传与管理
- ✅ 资料完整性检查
- 📸 支持拍照和选择图片
- 🗜️ 自动图片压缩
- 🖼️ 图片预览功能

## 安装步骤

### 1. 安装依赖

```bash
npm install
```

### 2. 运行开发服务器

```bash
npm run dev
```

应用将在 http://localhost:5173 启动。

### 3. 构建生产版本

```bash
npm run build
```

构建产物将生成在 `dist/` 目录。

### 4. 预览生产版本

```bash
npm run preview
```

## 项目结构

```
frontend/
├── src/
│   ├── api/              # API接口
│   │   ├── auth.js       # 认证接口
│   │   ├── customer.js   # 客户接口
│   │   └── document.js   # 资料接口
│   ├── components/       # 通用组件
│   ├── router/           # 路由配置
│   │   └── index.js
│   ├── store/            # 状态管理
│   │   ├── user.js       # 用户状态
│   │   └── customer.js   # 客户状态
│   ├── utils/            # 工具函数
│   │   ├── device.js     # 设备检测
│   │   ├── request.js    # HTTP请求封装
│   │   └── image.js      # 图片处理
│   ├── views/            # 页面组件
│   │   ├── pc/           # PC端页面
│   │   │   ├── CustomerList.vue
│   │   │   ├── CustomerForm.vue
│   │   │   └── CustomerDetail.vue
│   │   ├── mobile/       # 移动端页面
│   │   │   ├── CustomerList.vue
│   │   │   ├── CustomerForm.vue
│   │   │   └── CustomerDetail.vue
│   │   └── Login.vue     # 登录页
│   ├── App.vue
│   └── main.js
├── index.html
├── vite.config.js
└── package.json
```

## 环境配置

前端通过Vite代理连接后端API。开发环境配置在 `vite.config.js` 中：

```javascript
server: {
  port: 5173,
  proxy: {
    '/api': {
      target: 'http://127.0.0.1:8000',
      changeOrigin: true
    },
    '/media': {
      target: 'http://127.0.0.1:8000',
      changeOrigin: true
    }
  }
}
```

生产环境需要配置Nginx反向代理。

## 响应式设计

系统会自动检测设备类型：
- PC端（宽度 > 768px）：使用 Element Plus UI
- 移动端（宽度 ≤ 768px）：使用 Vant UI

设备检测逻辑在 `src/utils/device.js` 中。

## 图片上传

- 支持多图片上传
- 自动压缩图片（默认质量0.8，最大尺寸1920x1920）
- 移动端支持拍照上传
- 文件大小限制：10MB

## 状态管理

使用 Pinia 进行状态管理：
- `user.js`：用户认证状态
- `customer.js`：客户数据缓存

## 路由守卫

在 `router/index.js` 中配置了路由守卫：
- 未登录用户访问需要认证的页面将跳转到登录页
- 已登录用户访问登录页将跳转到客户列表页

## 注意事项

1. 确保后端服务已启动
2. 移动端测试可以使用Chrome DevTools的设备模拟
3. 生产环境需要配置正确的API地址

