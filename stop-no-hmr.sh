#!/bin/bash

# ============================================
# CCD 项目停止脚本 (macOS/Linux)
# ============================================
# 功能：停止所有运行中的后端和前端服务
# ============================================

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RESET='\033[0m'

echo ""
echo "========================================"
echo "  CCD 项目停止服务"
echo "========================================"
echo ""

# ============================================
# 停止后端服务 (端口 8000)
# ============================================
echo -e "${BLUE}正在停止后端服务 (端口 8000)...${RESET}"

# 方法1：从 PID 文件读取并停止
if [ -f "logs/backend.pid" ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo "找到后端进程 PID: $BACKEND_PID"
        kill $BACKEND_PID 2>/dev/null
        sleep 2
        # 如果进程仍在运行，强制停止
        if ps -p $BACKEND_PID > /dev/null 2>&1; then
            echo "强制停止后端进程..."
            kill -9 $BACKEND_PID 2>/dev/null
        fi
        echo -e "${GREEN}✓ 后端服务已停止${RESET}"
    else
        echo -e "${YELLOW}后端进程已不存在${RESET}"
    fi
    rm -f logs/backend.pid
else
    # 方法2：通过端口查找并停止
    BACKEND_PID=$(lsof -ti:8000 2>/dev/null)
    if [ ! -z "$BACKEND_PID" ]; then
        echo "找到占用端口 8000 的进程 PID: $BACKEND_PID"
        kill $BACKEND_PID 2>/dev/null
        sleep 2
        # 如果进程仍在运行，强制停止
        if ps -p $BACKEND_PID > /dev/null 2>&1; then
            echo "强制停止进程..."
            kill -9 $BACKEND_PID 2>/dev/null
        fi
        echo -e "${GREEN}✓ 后端服务已停止${RESET}"
    else
        echo -e "${YELLOW}未找到运行中的后端服务${RESET}"
    fi
fi

echo ""

# ============================================
# 停止前端服务 (端口 3000)
# ============================================
echo -e "${BLUE}正在停止前端服务 (端口 3000)...${RESET}"

# 方法1：从 PID 文件读取并停止
if [ -f "logs/frontend.pid" ]; then
    FRONTEND_PID=$(cat logs/frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        echo "找到前端进程 PID: $FRONTEND_PID"
        kill $FRONTEND_PID 2>/dev/null
        sleep 2
        # 如果进程仍在运行，强制停止
        if ps -p $FRONTEND_PID > /dev/null 2>&1; then
            echo "强制停止前端进程..."
            kill -9 $FRONTEND_PID 2>/dev/null
        fi
        echo -e "${GREEN}✓ 前端服务已停止${RESET}"
    else
        echo -e "${YELLOW}前端进程已不存在${RESET}"
    fi
    rm -f logs/frontend.pid
else
    # 方法2：通过端口查找并停止
    FRONTEND_PID=$(lsof -ti:3000 2>/dev/null)
    if [ ! -z "$FRONTEND_PID" ]; then
        echo "找到占用端口 3000 的进程 PID: $FRONTEND_PID"
        kill $FRONTEND_PID 2>/dev/null
        sleep 2
        # 如果进程仍在运行，强制停止
        if ps -p $FRONTEND_PID > /dev/null 2>&1; then
            echo "强制停止进程..."
            kill -9 $FRONTEND_PID 2>/dev/null
        fi
        echo -e "${GREEN}✓ 前端服务已停止${RESET}"
    else
        echo -e "${YELLOW}未找到运行中的前端服务${RESET}"
    fi
fi

echo ""

# ============================================
# 额外清理：停止所有相关的 Python 和 Node 进程
# ============================================
echo -e "${BLUE}清理相关进程...${RESET}"

# 停止所有 Django runserver 进程
DJANGO_PIDS=$(ps aux | grep "manage.py runserver" | grep -v grep | awk '{print $2}')
if [ ! -z "$DJANGO_PIDS" ]; then
    echo "找到 Django 进程: $DJANGO_PIDS"
    echo "$DJANGO_PIDS" | xargs kill 2>/dev/null
    echo -e "${GREEN}✓ Django 进程已清理${RESET}"
fi

# 停止所有 vite preview 进程
VITE_PIDS=$(ps aux | grep "vite preview" | grep -v grep | awk '{print $2}')
if [ ! -z "$VITE_PIDS" ]; then
    echo "找到 Vite 进程: $VITE_PIDS"
    echo "$VITE_PIDS" | xargs kill 2>/dev/null
    echo -e "${GREEN}✓ Vite 进程已清理${RESET}"
fi

echo ""

# ============================================
# 验证服务是否已停止
# ============================================
echo -e "${BLUE}验证服务状态...${RESET}"

BACKEND_RUNNING=0
FRONTEND_RUNNING=0

if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    BACKEND_RUNNING=1
fi

if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    FRONTEND_RUNNING=1
fi

if [ $BACKEND_RUNNING -eq 0 ]; then
    echo -e "${GREEN}✓ 后端服务已完全停止${RESET}"
else
    echo -e "${RED}✗ 后端服务仍在运行（端口 8000）${RESET}"
    echo "请手动检查并停止相关进程："
    echo "  lsof -ti:8000 | xargs kill -9"
fi

if [ $FRONTEND_RUNNING -eq 0 ]; then
    echo -e "${GREEN}✓ 前端服务已完全停止${RESET}"
else
    echo -e "${RED}✗ 前端服务仍在运行（端口 3000）${RESET}"
    echo "请手动检查并停止相关进程："
    echo "  lsof -ti:3000 | xargs kill -9"
fi

echo ""
echo "========================================"
echo -e "  ${GREEN}停止完成！${RESET}"
echo "========================================"
echo ""

# 清理日志文件（可选）
if [ -f "logs/backend.log" ]; then
    echo -e "${YELLOW}日志文件保留在 logs 目录${RESET}"
fi

echo ""

