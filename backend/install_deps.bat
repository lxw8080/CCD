@echo off
echo ========================================
echo 安装Python依赖（多镜像源尝试）
echo ========================================

REM 清除代理
set HTTP_PROXY=
set HTTPS_PROXY=
set http_proxy=
set https_proxy=
set NO_PROXY=*

echo.
echo 尝试安装 Django...

REM 尝试1: 豆瓣镜像
pip install --no-cache-dir Django==4.2.7 -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
if %errorlevel%==0 goto install_rest

REM 尝试2: 清华镜像
echo 豆瓣镜像失败，尝试清华镜像...
pip install --no-cache-dir Django==4.2.7 -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
if %errorlevel%==0 goto install_rest

REM 尝试3: 阿里云镜像
echo 清华镜像失败，尝试阿里云镜像...
pip install --no-cache-dir Django==4.2.7 -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
if %errorlevel%==0 goto install_rest

REM 尝试4: 官方源
echo 所有镜像失败，尝试官方源...
pip install --no-cache-dir Django==4.2.7
if %errorlevel%==0 goto install_rest

echo.
echo 错误：无法安装Django，请检查网络连接
pause
exit /b 1

:install_rest
echo.
echo Django安装成功！继续安装其他依赖...
echo.

REM 安装其他依赖
pip install --no-cache-dir djangorestframework==3.14.0 -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
pip install --no-cache-dir djangorestframework-simplejwt==5.3.0 -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
pip install --no-cache-dir django-cors-headers==4.3.0 -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
pip install --no-cache-dir Pillow==10.1.0 -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
pip install --no-cache-dir python-dotenv==1.0.0 -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

echo.
echo ========================================
echo 依赖安装完成！
echo ========================================
pause

