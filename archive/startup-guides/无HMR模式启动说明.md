# CCD 项目 - 无 HMR 模式启动说明

## 📋 概述

本文档说明如何使用无 HMR（Hot Module Replacement）模式启动 CCD 项目。此模式特别适合移动端测试，可以避免拍照时页面自动刷新的问题。

## 🎯 适用场景

- ✅ **移动端测试**：拍照、文件上传等功能测试
- ✅ **生产环境模拟**：测试生产构建的性能和行为
- ✅ **稳定性测试**：避免 HMR 导致的状态不一致
- ✅ **网络不稳定环境**：避免 WebSocket 连接中断导致的页面刷新

## 🚀 快速开始

### Windows 用户

1. **启动服务**
   ```cmd
   start-no-hmr.bat
   ```

2. **停止服务**
   ```cmd
   stop-no-hmr.bat
   ```

### macOS/Linux 用户

1. **首次使用：添加可执行权限**
   ```bash
   chmod +x start-no-hmr.sh stop-no-hmr.sh
   ```

2. **启动服务**
   ```bash
   ./start-no-hmr.sh
   ```

3. **停止服务**
   ```bash
   ./stop-no-hmr.sh
   ```

## 📦 前置要求

### 后端依赖

- Python 3.8+
- 已创建虚拟环境：`backend/venv`
- 已安装依赖：`pip install -r requirements.txt`

如果未安装，请执行：
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 前端依赖

- Node.js 16+
- npm 或 yarn

如果未安装，脚本会自动执行 `npm install`

## 🔧 脚本功能详解

### 启动脚本 (start-no-hmr)

#### 执行流程

1. **环境检查**
   - 检查项目目录结构
   - 验证 Python 虚拟环境
   - 验证 Node.js 依赖
   - 检查端口占用（8000, 3000）

2. **启动后端**
   - 激活 Python 虚拟环境
   - 启动 Django 开发服务器（端口 8000）
   - 验证后端服务是否正常启动

3. **构建前端**
   - 执行 `npm run build`
   - 生成生产环境构建文件

4. **启动前端预览**
   - 执行 `npm run preview`
   - 启动 Vite 预览服务器（端口 3000）
   - **无 HMR、无 WebSocket 连接**

5. **完成**
   - 显示服务地址
   - 自动打开浏览器（可选）
   - 保存进程 ID 到日志文件

#### 日志文件

所有日志保存在 `logs/` 目录：
- `backend.log` - 后端服务日志
- `frontend.log` - 前端服务日志
- `backend.pid` - 后端进程 ID（macOS/Linux）
- `frontend.pid` - 前端进程 ID（macOS/Linux）

### 停止脚本 (stop-no-hmr)

#### 执行流程

1. **停止后端服务**
   - 从 PID 文件读取进程 ID
   - 或通过端口 8000 查找进程
   - 优雅停止（SIGTERM）
   - 如果失败，强制停止（SIGKILL）

2. **停止前端服务**
   - 从 PID 文件读取进程 ID
   - 或通过端口 3000 查找进程
   - 优雅停止（SIGTERM）
   - 如果失败，强制停止（SIGKILL）

3. **清理进程**
   - 清理所有相关的 Django 进程
   - 清理所有相关的 Vite 进程
   - 关闭相关的命令行窗口（Windows）

4. **验证**
   - 检查端口是否已释放
   - 显示停止状态

## 🌐 访问地址

启动成功后，可以通过以下地址访问：

### 后端服务
- 本地：http://127.0.0.1:8000
- API 文档：http://127.0.0.1:8000/api/

### 前端服务
- 本地：http://localhost:3000
- 网络访问：http://[你的IP]:3000

**移动端测试**：使用网络地址（如 http://192.168.5.71:3000）在手机上访问

## ⚙️ 配置说明

### Vite 配置 (frontend/vite.config.js)

```javascript
export default defineConfig({
  server: {
    hmr: false,  // 禁用 HMR
    // ... 其他配置
  },
  preview: {
    host: '0.0.0.0',
    port: 3000,
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
})
```

### 关键特性

- ✅ **无 HMR**：代码修改不会自动热更新
- ✅ **无 WebSocket**：没有开发服务器连接
- ✅ **生产构建**：运行的是优化后的生产代码
- ✅ **API 代理**：前端请求自动代理到后端

## 🔍 常见问题

### 1. 端口被占用

**问题**：启动时提示端口 8000 或 3000 已被占用

**解决方案**：
```bash
# 先停止现有服务
# Windows
stop-no-hmr.bat

# macOS/Linux
./stop-no-hmr.sh

# 如果仍然占用，手动查找并停止进程
# Windows
netstat -ano | findstr :8000
taskkill /F /PID [进程ID]

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

### 2. 虚拟环境未找到

**问题**：提示未找到 Python 虚拟环境

**解决方案**：
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
```

### 3. 前端依赖缺失

**问题**：提示未找到 node_modules

**解决方案**：
```bash
cd frontend
npm install
```

### 4. 前端构建失败

**问题**：`npm run build` 执行失败

**解决方案**：
1. 检查 Node.js 版本（需要 16+）
2. 清理缓存：`npm cache clean --force`
3. 删除 node_modules 重新安装：
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

### 5. 移动端拍照仍然刷新

**问题**：使用无 HMR 模式后，移动端拍照仍然导致页面刷新

**可能原因**：
- 使用了 `npm run dev` 而不是 preview 模式
- 浏览器缓存问题

**解决方案**：
1. 确认使用的是 `start-no-hmr` 脚本
2. 清除浏览器缓存
3. 在移动端浏览器中强制刷新页面

### 6. 无法访问网络地址

**问题**：移动设备无法通过 IP 地址访问前端

**解决方案**：
1. 确认电脑和手机在同一网络
2. 检查防火墙设置，允许端口 3000
3. 使用 `ipconfig`（Windows）或 `ifconfig`（macOS/Linux）查看正确的 IP 地址

## 📝 开发注意事项

### 代码修改后的操作

由于无 HMR 模式运行的是生产构建，代码修改后需要：

1. **停止服务**
   ```bash
   # Windows
   stop-no-hmr.bat
   
   # macOS/Linux
   ./stop-no-hmr.sh
   ```

2. **重新启动**
   ```bash
   # Windows
   start-no-hmr.bat
   
   # macOS/Linux
   ./start-no-hmr.sh
   ```

或者，只重新构建前端：
```bash
cd frontend
npm run build
# 前端服务会自动检测到新的构建文件
```

### 开发模式 vs 无 HMR 模式

| 特性 | 开发模式 (dev) | 无 HMR 模式 (preview) |
|------|----------------|----------------------|
| 启动速度 | 快 | 慢（需要构建） |
| 热更新 | ✅ 支持 | ❌ 不支持 |
| 代码优化 | ❌ 未优化 | ✅ 已优化 |
| 移动端拍照 | ⚠️ 可能刷新 | ✅ 不会刷新 |
| WebSocket | ✅ 有 | ❌ 无 |
| 适用场景 | 日常开发 | 移动端测试、生产模拟 |

### 推荐工作流程

1. **日常开发**：使用 `start-dev.bat` 或 `npm run dev`
2. **移动端测试**：使用 `start-no-hmr.bat` 或 `./start-no-hmr.sh`
3. **生产部署前**：使用无 HMR 模式进行最终测试

## 🛠️ 高级配置

### 修改端口

如需修改默认端口，编辑以下文件：

**后端端口（默认 8000）**
```bash
# 修改启动脚本中的命令
python manage.py runserver 0.0.0.0:8080
```

**前端端口（默认 3000）**
```javascript
// frontend/vite.config.js
export default defineConfig({
  preview: {
    port: 3001,  // 修改为其他端口
    // ...
  }
})
```

### 自定义日志位置

修改启动脚本中的日志路径：
```bash
# 将 logs/backend.log 改为其他路径
nohup python manage.py runserver > /path/to/your/backend.log 2>&1 &
```

## 📞 技术支持

如遇到问题，请检查：
1. 日志文件：`logs/backend.log` 和 `logs/frontend.log`
2. 浏览器控制台错误信息
3. 网络连接状态

## 📄 相关文档

- [项目快速启动指南](./QUICK_START.md)
- [Windows 安装指南](./WINDOWS_SETUP_CN.md)
- [项目结构说明](./PROJECT_STRUCTURE.md)

---

**最后更新**：2025-10-19

