# 🎉 无 HMR 模式启动成功！

## 服务状态

✅ **后端服务**已成功启动
- 地址: http://127.0.0.1:8000
- 管理后台: http://127.0.0.1:8000/admin
- PID: 33717, 33720, 33724

✅ **前端服务**（构建版预览）已成功启动
- 地址: http://localhost:3000
- PID: 33757

## 什么是无 HMR 模式？

**HMR** (Hot Module Replacement) 是热模块替换功能，在开发模式下自动刷新修改的代码。

**无 HMR 模式**的特点：
- ✅ 使用生产构建版本（`npm run build` + `npm run preview`）
- ✅ 性能更稳定，更接近生产环境
- ✅ 避免 HMR 相关的兼容性问题
- ❌ 修改代码后需要手动重新构建

## 两种模式对比

| 特性 | 开发模式 (dev) | 无 HMR 模式 (preview) |
|------|----------------|----------------------|
| 启动方式 | `bash start-dev.sh` | `bash start-no-hmr.sh` |
| 前端命令 | `npm run dev` | `npm run build + preview` |
| 代码修改 | 自动热更新 | 需要手动重新构建 |
| 启动速度 | 快 | 较慢（需构建） |
| 性能 | 一般 | 更好 |
| 适用场景 | 开发调试 | 测试、演示、问题排查 |
| 端口 | 5173（或 3000） | 3000 |

## 访问系统

### 浏览器访问
在浏览器中打开: **http://localhost:3000**

### 可用账户

系统中已有以下测试账户：

| 用户名 | 角色 | 说明 |
|--------|------|------|
| `admin` | 管理员 | 超级管理员，拥有所有权限 |
| `service01` | 客服人员 | 可以创建客户、上传资料 |
| `auditor01` | 审核人员 | 可以审核客户资料 |

**默认密码**：请尝试 `admin123`、`admin` 或其他常见密码

### 移动端访问

在同一局域网内，可以用手机访问：
- http://192.168.2.55:3000

## 停止服务

### 使用停止脚本（推荐）

```bash
cd /Users/lxw8080/Desktop/Project\ Workspace/CCD
bash stop-no-hmr.sh
```

### 手动停止

如果脚本无法停止，可以手动终止进程：

```bash
# 停止后端
pkill -f "manage.py runserver"

# 停止前端
pkill -f "npm run preview"
pkill -f "vite preview"
```

## 重新启动

如果需要重新启动（例如修改了代码）：

```bash
# 1. 先停止
bash stop-no-hmr.sh

# 2. 再启动
bash start-no-hmr.sh
```

**注意**：由于是构建模式，前端修改代码后必须重新构建才能看到效果。

## 查看日志

### 后端日志

```bash
# 实时查看
tail -f logs/backend.log

# 查看最近50行
tail -50 logs/backend.log
```

### 前端日志

```bash
# 实时查看
tail -f logs/frontend.log

# 查看最近50行
tail -50 logs/frontend.log
```

## 开发建议

### 什么时候使用无 HMR 模式？

✅ **推荐使用场景**：
1. HMR 出现兼容性问题时
2. 需要测试生产构建版本
3. 需要更稳定的性能表现
4. 给客户演示系统
5. 排查 HMR 相关的 bug

❌ **不推荐场景**：
1. 日常开发（频繁修改代码）
2. 需要快速迭代时

### 切换到开发模式

如果需要频繁修改代码，建议切换回开发模式：

```bash
# 停止无 HMR 模式
bash stop-no-hmr.sh

# 启动开发模式
bash start-dev.sh
```

## 性能优化说明

无 HMR 模式启动时会进行以下优化：

1. ✅ **前端构建优化**：
   - 代码压缩和混淆
   - Tree-shaking（移除未使用代码）
   - 静态资源优化
   - Gzip 压缩

2. ✅ **依赖检查**：
   - 自动检查并修复 pdfjs-dist 依赖
   - 验证 Python 和 Node.js 环境
   - 检查端口占用

3. ✅ **启动检查**：
   - 后端健康检查（最多等待 30 秒）
   - 前端健康检查（最多等待 10 秒）
   - 自动打开浏览器

## 构建信息

最新构建统计：

- **总构建时间**: ~2.5秒
- **构建产物大小**: 
  - 最大 JS 文件: 767 kB (index-UrPaMeHx.js)
  - 最大 CSS 文件: 339 kB (index-9c0uMBAG.css)
  - PDF.js 库: 287 kB (pdf-D9xrRifX.js)
  
⚠️ **注意**: 部分文件超过 500KB，建议后续考虑：
- 使用动态导入 (`import()`) 进行代码分割
- 配置手动分块策略
- 按需加载组件

## 故障排查

### Q: 后端启动失败？

检查日志：
```bash
cat logs/backend.log
```

常见原因：
- 端口 8000 被占用
- 虚拟环境未正确激活
- 数据库连接失败

### Q: 前端构建失败？

检查是否有语法错误：
```bash
cd frontend
npm run build
```

### Q: 页面无法访问？

1. 检查服务是否运行：
   ```bash
   ps aux | grep -E "(runserver|preview)"
   ```

2. 检查端口是否监听：
   ```bash
   lsof -i :8000
   lsof -i :3000
   ```

3. 查看进程 PID：
   ```bash
   cat logs/backend.pid
   cat logs/frontend.pid
   ```

### Q: 修改代码不生效？

无 HMR 模式下需要重新构建：
```bash
bash stop-no-hmr.sh
bash start-no-hmr.sh
```

## 技术细节

### 启动流程

1. **检查后端依赖** → 验证 Python 虚拟环境和 Django
2. **检查前端依赖** → 验证 Node.js、npm 和 pdfjs-dist
3. **检查端口占用** → 确保 8000 和 3000 端口可用
4. **启动后端** → 激活虚拟环境并运行 Django
5. **构建前端** → 运行 `vite build` 生成生产版本
6. **启动前端** → 运行 `vite preview` 预览构建版本

### 脚本特性

- ✅ 完整的错误处理和陷阱机制
- ✅ 非交互模式自动化支持
- ✅ 详细的启动日志
- ✅ 容错的服务健康检查
- ✅ 自动打开浏览器（macOS）
- ✅ 颜色化输出，易于阅读

---

祝您使用愉快！🚀

如有问题，请查看日志文件或联系技术支持。

