#!/bin/bash

# 客户资料收集系统部署脚本
# 使用方法: bash deployment/deploy.sh

set -e  # 遇到错误立即退出

echo "======================================"
echo "开始部署客户资料收集系统"
echo "======================================"

# 项目根目录
PROJECT_ROOT="/path/to/CCD"  # 修改为实际路径
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

# 1. 更新代码（如果使用Git）
echo "1. 更新代码..."
cd $PROJECT_ROOT
# git pull origin main

# 2. 部署后端
echo "2. 部署后端..."
cd $BACKEND_DIR

# 激活虚拟环境
source venv/bin/activate

# 安装/更新依赖
pip install -r requirements.txt

# 运行数据库迁移
python manage.py migrate

# 收集静态文件
python manage.py collectstatic --noinput

# 重启Gunicorn
echo "重启Gunicorn..."
pkill -f gunicorn || true
sleep 2
gunicorn -c ../deployment/gunicorn_config.py config.wsgi:application --daemon

# 3. 部署前端
echo "3. 部署前端..."
cd $FRONTEND_DIR

# 安装依赖
npm install

# 构建生产版本
npm run build

# 4. 重启Nginx
echo "4. 重启Nginx..."
sudo systemctl reload nginx

echo "======================================"
echo "部署完成！"
echo "======================================"

# 显示服务状态
echo ""
echo "服务状态："
ps aux | grep gunicorn | grep -v grep
sudo systemctl status nginx --no-pager

