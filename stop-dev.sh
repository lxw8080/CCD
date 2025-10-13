#!/bin/bash

# 停止开发环境脚本
# 使用方法: bash stop-dev.sh

echo "停止开发服务器..."

# 读取PID并停止进程
if [ -f ".backend.pid" ]; then
    BACKEND_PID=$(cat .backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo "停止后端服务器 (PID: $BACKEND_PID)..."
        kill $BACKEND_PID
    fi
    rm .backend.pid
fi

if [ -f ".frontend.pid" ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        echo "停止前端服务器 (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID
    fi
    rm .frontend.pid
fi

# 额外清理（查找并停止可能残留的进程）
pkill -f "manage.py runserver" 2>/dev/null
pkill -f "vite" 2>/dev/null

echo "开发服务器已停止"

