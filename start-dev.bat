@echo off
REM Windows开发环境快速启动脚本
REM 使用方法: start-dev.bat

echo ======================================
echo 启动客户资料收集系统开发环境
echo ======================================

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

REM 启动后端
echo 1. 启动后端服务...
cd backend

REM 检查虚拟环境
if not exist "venv" (
    echo 创建Python虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 安装依赖
if not exist "venv\.installed" (
    echo 安装Python依赖...
    pip install -r requirements.txt
    echo. > venv\.installed
)

REM 检查数据库迁移
echo 检查数据库迁移...
python manage.py migrate

REM 启动Django开发服务器
echo 启动Django开发服务器...
start /B python manage.py runserver

cd ..

REM 启动前端
echo.
echo 2. 启动前端服务...
cd frontend

REM 检查node_modules
if not exist "node_modules" (
    echo 安装Node.js依赖...
    call npm install
)

REM 启动Vite开发服务器
echo 启动Vite开发服务器...
start cmd /k npm run dev

cd ..

echo.
echo ======================================
echo 开发环境启动完成！
echo ======================================
echo 后端地址: http://127.0.0.1:8000
echo 前端地址: http://localhost:5173
echo 管理后台: http://127.0.0.1:8000/admin
echo.
echo 关闭命令窗口即可停止服务
echo.
pause

