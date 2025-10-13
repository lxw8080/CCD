#!/bin/bash

# 开发环境快速启动脚本
# 使用方法: bash start-dev.sh

echo "======================================"
echo "启动客户资料收集系统开发环境"
echo "======================================"

# 检查是否在项目根目录
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "错误：请在项目根目录运行此脚本"
    exit 1
fi

# 启动后端
echo "1. 启动后端服务..."
cd backend

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建Python虚拟环境..."
    python -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null

# 安装依赖（如果需要）
if [ ! -f "venv/.installed" ]; then
    echo "安装Python依赖..."
    pip install -r requirements.txt
    touch venv/.installed
fi

# 检查数据库迁移
echo "检查数据库迁移..."
python manage.py migrate

# 在后台启动Django开发服务器
echo "启动Django开发服务器..."
python manage.py runserver > ../backend.log 2>&1 &
BACKEND_PID=$!
echo "后端服务器PID: $BACKEND_PID"

cd ..

# 启动前端
echo ""
echo "2. 启动前端服务..."
cd frontend

# 检查node_modules
if [ ! -d "node_modules" ]; then
    echo "安装Node.js依赖..."
    npm install
fi

# 启动Vite开发服务器
echo "启动Vite开发服务器..."
npm run dev &
FRONTEND_PID=$!
echo "前端服务器PID: $FRONTEND_PID"

cd ..

# 保存PID到文件
echo $BACKEND_PID > .backend.pid
echo $FRONTEND_PID > .frontend.pid

echo ""
echo "======================================"
echo "开发环境启动完成！"
echo "======================================"
echo "后端地址: http://127.0.0.1:8000"
echo "前端地址: http://localhost:5173"
echo "管理后台: http://127.0.0.1:8000/admin"
echo ""
echo "按 Ctrl+C 停止服务，或运行 bash stop-dev.sh"
echo ""

# 等待用户中断
wait

