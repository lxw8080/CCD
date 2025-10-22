# 快速开始指南

本指南将帮助您在5分钟内启动客户资料收集系统。

## 前置要求

确保您的系统已安装以下软件：

- ✅ Python 3.8+ （推荐 3.10）
- ✅ Node.js 16+ （推荐 18）
- ✅ PostgreSQL 12+ （推荐 14）

### 检查安装

```bash
python --version
node --version
npm --version
psql --version
```

## 一键启动（无HMR模式）

### Windows用户

```cmd
start-no-hmr.bat
```

### Linux/Mac用户

```bash
bash start-no-hmr.sh
```

**就这么简单！** 脚本会自动：
1. 创建Python虚拟环境
2. 安装所有依赖
3. 运行数据库迁移
4. 启动后端服务（8000端口）
5. 启动前端服务（5173端口）

## 手动启动（详细步骤）

如果一键启动遇到问题，可以按照以下步骤手动启动。

### 第一步：准备数据库

```bash
# 启动PostgreSQL（根据系统不同）
# Windows: 通过服务管理器启动
# Linux: sudo systemctl start postgresql
# Mac: brew services start postgresql

# 连接PostgreSQL
psql -U postgres

# 创建数据库和用户
CREATE DATABASE ccd_db;
CREATE USER ccd_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE ccd_db TO ccd_user;
\q
```

### 第二步：配置后端

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
# Windows:
copy .env.example .env
# Linux/Mac:
cp .env.example .env

# 编辑.env文件，配置数据库连接
# DB_NAME=ccd_db
# DB_USER=ccd_user
# DB_PASSWORD=your_password
# DB_HOST=localhost
# DB_PORT=5432
```

### 第三步：初始化数据库

```bash
# 运行数据库迁移
python manage.py makemigrations
python manage.py migrate

# 初始化资料类型数据
python manage.py init_document_types

# 创建测试数据（可选）
python manage.py create_demo_data

# 或创建超级管理员
python manage.py createsuperuser
```

### 第四步：启动后端

```bash
# 在backend目录下
python manage.py runserver
```

后端服务运行在：http://127.0.0.1:8000

### 第五步：启动前端

打开**新的终端窗口**：

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端应用运行在：http://localhost:5173

## 访问系统

1. 打开浏览器访问：http://localhost:5173
2. 使用测试账号登录（如果运行了create_demo_data）：
   - 管理员：`admin` / `admin123`
   - 客服1：`staff1` / `staff123`
   - 客服2：`staff2` / `staff123`
   - 审核员：`auditor` / `auditor123`

3. 或使用创建的超级管理员账号登录

## 访问管理后台

访问：http://127.0.0.1:8000/admin

使用超级管理员账号登录，可以管理所有数据。

## 测试功能

### 1. 创建客户

- 点击"新建客户"按钮
- 填写客户信息（姓名、身份证号、手机号等）
- 点击"保存"

### 2. 上传资料

- 进入客户详情页
- 选择资料类型
- 点击上传图片（PC端可拖拽，移动端可拍照）
- 点击"上传"按钮

### 3. 查看完整性

- 在客户详情页自动显示资料完整性
- 绿色进度条表示完整度
- 查看缺失的必需资料

### 4. 移动端测试

- PC端：按F12打开开发者工具，切换到移动设备模式
- 或直接用手机访问：http://your-ip:5173

## 常见问题

### Q1: 数据库连接失败

**A**: 检查PostgreSQL是否启动，.env文件配置是否正确

```bash
# 检查PostgreSQL状态
# Windows: 任务管理器 → 服务
# Linux: sudo systemctl status postgresql
# Mac: brew services list
```

### Q2: 端口被占用

**A**: 修改端口或停止占用端口的程序

```bash
# 查看端口占用
# Windows: netstat -ano | findstr "8000"
# Linux/Mac: lsof -i :8000

# 停止后端
# Windows: taskkill /F /PID <PID>
# Linux/Mac: kill -9 <PID>
```

### Q3: npm install 很慢

**A**: 使用国内镜像

```bash
npm config set registry https://registry.npmmirror.com
npm install
```

### Q4: Python依赖安装失败

**A**: 升级pip后重试

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Q5: 图片上传失败

**A**: 检查media目录权限

```bash
# 在backend目录下
mkdir -p media/documents
chmod -R 755 media  # Linux/Mac
```

### Q6: 移动端无法拍照

**A**: 需要HTTPS或localhost环境

- 开发环境使用localhost
- 生产环境配置HTTPS

## 停止服务

### 使用脚本

```bash
# Linux/Mac
bash stop-dev.sh
```

### 手动停止

- 在运行服务的终端按 `Ctrl+C`
- 或关闭终端窗口

## 下一步

- 📖 阅读 [README.md](README.md) 了解项目详情
- 🏗️ 查看 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) 了解项目结构
- 🚀 阅读 [deployment/README.md](deployment/README.md) 了解生产部署
- 📝 查看 [CHANGELOG.md](CHANGELOG.md) 了解版本更新

## 需要帮助？

如果遇到问题：

1. 检查终端的错误信息
2. 查看日志文件
3. 搜索错误信息
4. 联系技术支持

## 开发建议

- 使用Git管理代码版本
- 定期备份数据库
- 不要在生产环境使用DEBUG=True
- 定期更新依赖包
- 编写测试代码

祝您使用愉快！🎉

