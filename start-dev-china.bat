@echo off
REM Windows开发环境快速启动脚本（中国大陆优化版）
REM 使用方法: start-dev-china.bat

echo ======================================
echo 启动客户资料收集系统开发环境（中国镜像）
echo ======================================

REM 清除可能的代理设置
set HTTP_PROXY=
set HTTPS_PROXY=
set http_proxy=
set https_proxy=

REM 检查是否在项目根目录
if not exist "backend" (
    echo 错误：请在项目根目录运行此脚本
    pause
    exit /b 1
)
if not exist "frontend" (
    echo 错误：请在项目根目录运行此脚本
    pause
    exit /b 1
)

REM 配置npm镜像
echo.
echo 配置npm使用淘宝镜像...
call npm config set registry https://registry.npmmirror.com
call npm config get registry

REM 启动后端
echo.
echo ======================================
echo 1. 启动后端服务
echo ======================================
cd backend

REM 检查虚拟环境
if not exist "venv" (
    echo 创建Python虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装依赖（使用清华镜像，禁用代理）
if not exist "venv\.installed" (
    echo 安装Python依赖（使用清华镜像）...
    set HTTP_PROXY=
    set HTTPS_PROXY=
    python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
    pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn -r requirements.txt
    if errorlevel 1 (
        echo.
        echo 警告：pip安装失败，尝试使用阿里云镜像...
        pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r requirements.txt
    )
    echo. > venv\.installed
)

REM 检查数据库迁移
echo.
echo 检查数据库迁移...
python manage.py migrate --run-syncdb

REM 启动Django开发服务器
echo.
echo 启动Django开发服务器...
start "CCD Backend" cmd /k "cd /d %CD% && venv\Scripts\activate.bat && python manage.py runserver"

cd ..

REM 等待后端启动
timeout /t 3 /nobreak > nul

REM 启动前端
echo.
echo ======================================
echo 2. 启动前端服务
echo ======================================
cd frontend

REM 检查node_modules
if not exist "node_modules" (
    echo 安装Node.js依赖（使用淘宝镜像）...
    call npm install
)

REM 启动Vite开发服务器
echo.
echo 启动Vite开发服务器...
start "CCD Frontend" cmd /k "cd /d %CD% && npm run dev"

cd ..

echo.
echo ======================================
echo 开发环境启动完成！
echo ======================================
echo 后端地址: http://127.0.0.1:8000
echo 前端地址: http://localhost:5173
echo 管理后台: http://127.0.0.1:8000/admin
echo.
echo 两个新窗口已打开，关闭窗口即可停止服务
echo.
pause

