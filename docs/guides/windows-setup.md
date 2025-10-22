# Windows系统安装指南（中国大陆）

本指南专门针对Windows系统和中国大陆网络环境优化。

## ⚠️ 常见问题：代理错误

如果您看到类似 `ValueError: check_hostname requires server_hostname` 的错误，说明系统设置了代理。

### 解决方法

#### 方法1：使用无HMR启动脚本（推荐）

```cmd
start-no-hmr.bat
```

这个脚本会自动：
- 检查所有依赖
- 构建前端生产版本
- 启动后端和前端服务

#### 方法2：手动清除代理

打开PowerShell或CMD，执行：

```cmd
set HTTP_PROXY=
set HTTPS_PROXY=
set http_proxy=
set https_proxy=
```

然后继续安装。

## 📦 手动安装步骤

### 第一步：配置镜像源

#### 配置npm镜像（淘宝）

```cmd
npm config set registry https://registry.npmmirror.com
npm config get registry
```

#### 配置pip镜像（清华）

创建或编辑文件 `C:\Users\你的用户名\pip\pip.ini`：

```ini
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
```

或者在每次安装时使用 `-i` 参数：

```cmd
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple 包名
```

### 第二步：安装后端依赖

```cmd
cd backend

REM 创建虚拟环境
python -m venv venv

REM 激活虚拟环境
venv\Scripts\activate.bat

REM 清除代理
set HTTP_PROXY=
set HTTPS_PROXY=

REM 升级pip
python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn

REM 安装依赖
pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn -r requirements.txt
```

#### 如果清华镜像失败，尝试阿里云镜像：

```cmd
pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r requirements.txt
```

#### 如果还是失败，尝试豆瓣镜像：

```cmd
pip install --no-cache-dir -i https://pypi.douban.com/simple --trusted-host pypi.douban.com -r requirements.txt
```

### 第三步：初始化数据库

**注意：本项目需要PostgreSQL数据库。如果您还没有安装，请先安装PostgreSQL。**

#### 临时方案：使用SQLite（仅用于测试）

如果您暂时没有PostgreSQL，可以修改为使用SQLite：

编辑 `backend/config/settings.py`，找到 `DATABASES` 配置，替换为：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

然后运行迁移：

```cmd
python manage.py makemigrations
python manage.py migrate
```

#### 初始化数据

```cmd
REM 初始化资料类型
python manage.py init_document_types

REM 创建测试数据（可选）
python manage.py create_demo_data

REM 或创建超级管理员
python manage.py createsuperuser
```

### 第四步：启动后端

```cmd
python manage.py runserver
```

保持这个窗口打开，后端将运行在 http://127.0.0.1:8000

### 第五步：安装前端依赖

**打开新的CMD窗口**：

```cmd
cd frontend

REM 安装依赖（使用淘宝镜像）
npm install

REM 如果npm install很慢或失败，可以使用cnpm
npm install -g cnpm --registry=https://registry.npmmirror.com
cnpm install
```

### 第六步：启动前端

```cmd
npm run dev
```

前端将运行在 http://localhost:5173

## 🎯 访问系统

1. 打开浏览器访问：http://localhost:5173
2. 使用测试账号登录（如果运行了create_demo_data）：
   - 管理员：`admin` / `admin123`
   - 客服：`staff1` / `staff123`

## 🔧 常见问题

### Q1: pip安装一直卡住

**A**: 使用 `--no-cache-dir` 参数并指定镜像：

```cmd
pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn Django
```

### Q2: npm install很慢

**A**: 确认已配置淘宝镜像：

```cmd
npm config get registry
```

应该显示：`https://registry.npmmirror.com`

### Q3: 提示"无法加载文件 venv\Scripts\activate.ps1"

**A**: PowerShell执行策略问题，使用CMD而不是PowerShell，或者运行：

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Q4: 没有安装PostgreSQL

**A**: 有三个选择：

1. **安装PostgreSQL**（推荐）
   - 下载：https://www.postgresql.org/download/windows/
   - 或使用国内镜像：https://mirrors.tuna.tsinghua.edu.cn/postgresql/

2. **使用SQLite**（仅测试）
   - 按照上面"临时方案"修改配置

3. **使用Docker**
   ```cmd
   docker run --name ccd-postgres -e POSTGRES_PASSWORD=123456 -e POSTGRES_DB=ccd_db -p 5432:5432 -d postgres:14
   ```

### Q5: 端口被占用

**A**: 修改端口或停止占用进程

```cmd
REM 查看端口占用
netstat -ano | findstr "8000"
netstat -ano | findstr "5173"

REM 停止进程（替换<PID>为实际进程ID）
taskkill /F /PID <PID>
```

### Q6: 图片上传失败

**A**: 创建media目录并设置权限

```cmd
cd backend
mkdir media\documents
```

## 📝 完整的命令序列

如果您想一步步手动执行，这是完整的命令序列：

```cmd
REM 1. 配置镜像
npm config set registry https://registry.npmmirror.com

REM 2. 后端设置
cd backend
python -m venv venv
venv\Scripts\activate.bat
set HTTP_PROXY=
set HTTPS_PROXY=
python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn -r requirements.txt

REM 3. 数据库初始化（使用SQLite临时方案）
python manage.py migrate
python manage.py init_document_types
python manage.py create_demo_data

REM 4. 启动后端（新窗口）
start cmd /k "cd /d %CD% && venv\Scripts\activate.bat && python manage.py runserver"

REM 5. 前端设置（回到项目根目录）
cd ..
cd frontend
npm install

REM 6. 启动前端（新窗口）
start cmd /k "cd /d %CD% && npm run dev"
```

## 🌐 中国大陆可用的镜像源

### Python (pip)
- 清华：https://pypi.tuna.tsinghua.edu.cn/simple
- 阿里云：https://mirrors.aliyun.com/pypi/simple/
- 豆瓣：https://pypi.douban.com/simple
- 中科大：https://pypi.mirrors.ustc.edu.cn/simple/

### Node.js (npm)
- 淘宝：https://registry.npmmirror.com
- 腾讯云：https://mirrors.cloud.tencent.com/npm/
- 华为云：https://mirrors.huaweicloud.com/repository/npm/

## ✅ 验证安装

### 检查后端

访问：http://127.0.0.1:8000/admin

应该能看到Django管理后台登录页面。

### 检查前端

访问：http://localhost:5173

应该能看到登录页面。

### 检查API

访问：http://127.0.0.1:8000/api/documents/types/

应该返回JSON数据（需要先登录）。

## 🎉 成功标志

如果您看到：
- ✅ 后端窗口显示：`Starting development server at http://127.0.0.1:8000/`
- ✅ 前端窗口显示：`Local: http://localhost:5173/`
- ✅ 浏览器能打开登录页面

恭喜！系统已成功启动！

## 💡 提示

1. 每次启动都需要激活虚拟环境
2. 保持两个CMD窗口打开（后端和前端）
3. 按 Ctrl+C 可以停止服务
4. 关闭窗口也会停止服务

## 📞 需要帮助？

如果遇到其他问题，请：
1. 检查错误信息
2. 查看本文档的常见问题部分
3. 确认Python和Node.js版本符合要求
4. 尝试使用不同的镜像源

