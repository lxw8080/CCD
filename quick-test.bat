@echo off
REM 快速测试脚本 - 使用SQLite数据库
echo ======================================
echo 快速测试启动（使用SQLite）
echo ======================================

cd backend

REM 设置环境变量使用SQLite
set USE_SQLITE=True
set SECRET_KEY=django-insecure-test-key-12345
set DEBUG=True

REM 检查虚拟环境
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 清除代理
set HTTP_PROXY=
set HTTPS_PROXY=

REM 安装依赖
if not exist "venv\.installed" (
    echo 安装依赖（使用清华镜像）...
    python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
    pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn Django==4.2.7 djangorestframework==3.14.0 djangorestframework-simplejwt==5.3.0 django-cors-headers==4.3.0 Pillow==10.1.0 python-dotenv==1.0.0
    
    if errorlevel 1 (
        echo 清华镜像失败，尝试阿里云镜像...
        pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com Django==4.2.7 djangorestframework==3.14.0 djangorestframework-simplejwt==5.3.0 django-cors-headers==4.3.0 Pillow==10.1.0 python-dotenv==1.0.0
    )
    
    echo. > venv\.installed
)

REM 运行迁移
echo.
echo 运行数据库迁移...
python manage.py makemigrations
python manage.py migrate

REM 初始化数据
echo.
echo 初始化资料类型...
python manage.py init_document_types

echo.
echo 创建测试数据...
python manage.py create_demo_data

REM 启动服务器
echo.
echo ======================================
echo 启动Django服务器...
echo ======================================
echo.
echo 测试账号：
echo   管理员: admin / admin123
echo   客服: staff1 / staff123
echo.
python manage.py runserver

pause

