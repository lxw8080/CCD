#!/bin/bash

# ============================================
# CCD 项目停止脚本 - 无 HMR 模式
# ============================================

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
RESET='\033[0m'

printf "\n"
printf "========================================\n"
printf "  停止 CCD 项目服务\n"
printf "========================================\n"
printf "\n"

# 检查PID文件
BACKEND_PID_FILE="logs/backend.pid"
FRONTEND_PID_FILE="logs/frontend.pid"

STOPPED=0

# 停止后端
if [ -f "$BACKEND_PID_FILE" ]; then
    BACKEND_PID=$(cat "$BACKEND_PID_FILE")
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        printf "${YELLOW}停止后端服务 (PID: $BACKEND_PID)...${RESET}\n"
        kill $BACKEND_PID 2>/dev/null || true
        sleep 1
        # 如果还在运行，强制终止
        if ps -p $BACKEND_PID > /dev/null 2>&1; then
            kill -9 $BACKEND_PID 2>/dev/null || true
        fi
        printf "${GREEN}✓ 后端服务已停止${RESET}\n"
        STOPPED=$((STOPPED + 1))
    else
        printf "${YELLOW}后端服务未运行 (PID: $BACKEND_PID)${RESET}\n"
    fi
    rm -f "$BACKEND_PID_FILE"
else
    printf "${YELLOW}未找到后端PID文件${RESET}\n"
fi

# 停止前端
if [ -f "$FRONTEND_PID_FILE" ]; then
    FRONTEND_PID=$(cat "$FRONTEND_PID_FILE")
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        printf "${YELLOW}停止前端服务 (PID: $FRONTEND_PID)...${RESET}\n"
        kill $FRONTEND_PID 2>/dev/null || true
        sleep 1
        # 如果还在运行，强制终止
        if ps -p $FRONTEND_PID > /dev/null 2>&1; then
            kill -9 $FRONTEND_PID 2>/dev/null || true
        fi
        printf "${GREEN}✓ 前端服务已停止${RESET}\n"
        STOPPED=$((STOPPED + 1))
    else
        printf "${YELLOW}前端服务未运行 (PID: $FRONTEND_PID)${RESET}\n"
    fi
    rm -f "$FRONTEND_PID_FILE"
else
    printf "${YELLOW}未找到前端PID文件${RESET}\n"
fi

# 清理可能残留的进程
printf "\n${YELLOW}检查并清理残留进程...${RESET}\n"
pkill -f "manage.py runserver" 2>/dev/null && printf "  清理了 Django 进程\n" || true
pkill -f "npm run preview" 2>/dev/null && printf "  清理了 npm preview 进程\n" || true
pkill -f "vite preview" 2>/dev/null && printf "  清理了 vite preview 进程\n" || true

printf "\n"
if [ $STOPPED -gt 0 ]; then
    printf "${GREEN}========================================${RESET}\n"
    printf "${GREEN}  服务已全部停止！${RESET}\n"
    printf "${GREEN}========================================${RESET}\n"
else
    printf "${YELLOW}========================================${RESET}\n"
    printf "${YELLOW}  没有运行中的服务${RESET}\n"
    printf "${YELLOW}========================================${RESET}\n"
fi
printf "\n"
