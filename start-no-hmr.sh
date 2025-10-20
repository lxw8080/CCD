#!/bin/bash

# ============================================
# CCD 项目无 HMR 模式启动脚本 (macOS/Linux)
# 关键修复：
# 1. 后端检查增加容错：允许curl失败，避免脚本直接中断
# 2. 延长后端等待时间至30秒，适配启动慢的场景
# 3. 增加详细日志，便于定位后端启动失败原因
# 4. 强制建议用bash执行，避免sh兼容性问题
# ============================================

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RESET='\033[0m'

# 关键配置
PDFJS_VERSION="3.4.120"
DEFAULT_VUE_PATH="frontend/src/components/FilePreview/MobilePreviewDialog.vue"
VUE_FILE_PATH=""
# 后端等待配置：15次×2秒=30秒（足够慢设备启动）
BACKEND_CHECK_TIMES=15
BACKEND_CHECK_INTERVAL=2

# 错误处理：捕获异常并清理进程
set -e
trap '
    printf "${RED}错误：脚本执行失败${RESET}\n";
    if [ -n "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
        printf "已清理后端进程：$BACKEND_PID\n"
    fi
    if [ -n "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
        printf "已清理前端进程：$FRONTEND_PID\n"
    fi
    # 提示查看后端日志
    printf "${YELLOW}建议：检查后端日志定位问题：logs/backend.log${RESET}\n"
    exit 1
' ERR

# 强制检查执行shell：建议用bash而非sh
if [ "$(basename "$SHELL")" != "bash" ] && [ "$0" != "bash" ]; then
    # 检查是否在交互式终端中
    if [ -t 0 ]; then
        printf "${YELLOW}警告：当前用 sh 执行，可能存在兼容性问题！${RESET}\n"
        printf "${YELLOW}建议用以下命令重新运行：bash '%s'\n${RESET}" "$0"
        read -p "是否继续用 sh 执行？[y/N] " -n 1 -r
        printf "\n"
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 0
        fi
    else
        # 非交互模式：自动继续
        printf "${YELLOW}提示：检测到非交互模式，自动继续执行${RESET}\n"
    fi
fi

printf "\n"
printf "========================================\n"
printf "  CCD 项目启动 - 无 HMR 模式（完整版）\n"
printf "  含 pdfjs-dist 依赖自动修复功能\n"
printf "========================================\n"
printf "\n"

# 检查项目根目录
if [ ! -d "backend" ]; then
    printf "${RED}错误：未找到 backend 目录${RESET}\n"
    printf "请在项目根目录下运行此脚本\n"
    exit 1
fi
if [ ! -d "frontend" ]; then
    printf "${RED}错误：未找到 frontend 目录${RESET}\n"
    printf "请在项目根目录下运行此脚本\n"
    exit 1
fi

# ============================================
# 1. 检查后端依赖
# ============================================
printf "${BLUE}[1/6] 检查后端依赖...${RESET}\n"

# 检查虚拟环境
if [ ! -d "backend/venv" ]; then
    printf "${RED}错误：未找到 Python 虚拟环境${RESET}\n"
    printf "请先运行：cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt\n"
    exit 1
fi
if [ ! -f "backend/venv/bin/python" ]; then
    printf "${RED}错误：虚拟环境不完整（缺失python）${RESET}\n"
    printf "请重新创建虚拟环境\n"
    exit 1
fi

# 检查Django依赖（容错：忽略pip输出的无关警告）
if ! backend/venv/bin/pip list 2>/dev/null | grep -q "Django"; then
    printf "${RED}错误：后端核心依赖（Django）未安装${RESET}\n"
    printf "请运行：cd backend && source venv/bin/activate && pip install -r requirements.txt\n"
    exit 1
fi

# 提示pip升级（非强制）
PIP_VERSION=$(backend/venv/bin/pip --version 2>/dev/null | awk '{print $2}' | cut -d '.' -f 1)
if [ -n "$PIP_VERSION" ] && [ $PIP_VERSION -lt 25 ]; then
    printf "${YELLOW}提示：pip版本较旧（当前：$PIP_VERSION.x，建议≥25.x）${RESET}\n"
    printf "可运行升级：backend/venv/bin/python -m pip install --upgrade pip\n"
fi

printf "${GREEN}✓ 后端依赖检查通过${RESET}\n"
printf "\n"

# ============================================
# 2. 检查前端依赖
# ============================================
printf "${BLUE}[2/6] 检查前端依赖（含pdfjs-dist修复）...${RESET}\n"

# 检查node/npm
if ! command -v node &> /dev/null; then
    printf "${RED}错误：未安装 node.js${RESET}\n"
    printf "请先安装 node.js（推荐≥16）\n"
    exit 1
fi
if ! command -v npm &> /dev/null; then
    printf "${RED}错误：未安装 npm${RESET}\n"
    printf "请先安装 npm（推荐≥8）\n"
    exit 1
fi

# 版本校验
NODE_VERSION=$(node -v | cut -d 'v' -f 2 | cut -d '.' -f 1)
NPM_VERSION=$(npm -v | cut -d '.' -f 1)
if [ $NODE_VERSION -lt 16 ]; then
    printf "${RED}错误：node版本过低（当前v$NODE_VERSION，需≥16）${RESET}\n"
    exit 1
fi
if [ $NPM_VERSION -lt 8 ]; then
    printf "${RED}错误：npm版本过低（当前$NPM_VERSION，需≥8）${RESET}\n"
    exit 1
fi

# 处理pdfjs-dist
printf "${BLUE}  [子步骤1] 处理 pdfjs-dist 依赖...${RESET}\n"
cd frontend
if npm list pdfjs-dist 2>&1 | grep -q "pdfjs-dist@"; then
    INSTALLED_VERSION=$(npm list pdfjs-dist 2>&1 | grep -oE 'pdfjs-dist@[0-9]+\.[0-9]+\.[0-9]+' | cut -d '@' -f 2)
    printf "${GREEN}  ✓ pdfjs-dist 已安装（版本：$INSTALLED_VERSION）${RESET}\n"
else
    printf "${YELLOW}  未找到 pdfjs-dist，正在安装（版本：$PDFJS_VERSION）...${RESET}\n"
    npm install pdfjs-dist@$PDFJS_VERSION --save
    printf "${GREEN}  ✓ pdfjs-dist 安装完成${RESET}\n"
fi
cd ..

# 确认Vue文件路径
printf "${BLUE}  [子步骤2] 确认 MobilePreviewDialog.vue 路径...${RESET}\n"
if [ -f "$DEFAULT_VUE_PATH" ]; then
    VUE_FILE_PATH="$DEFAULT_VUE_PATH"
    printf "${GREEN}  ✓ 找到默认路径：$VUE_FILE_PATH${RESET}\n"
else
    printf "${YELLOW}  未找到默认路径：$DEFAULT_VUE_PATH${RESET}\n"
    read -p "  请输入文件完整路径：" USER_VUE_PATH
    if [ ! -f "$USER_VUE_PATH" ]; then
        printf "${RED}  错误：路径 $USER_VUE_PATH 不存在${RESET}\n"
        exit 1
    fi
    VUE_FILE_PATH="$USER_VUE_PATH"
    printf "${GREEN}  ✓ 确认路径：$VUE_FILE_PATH${RESET}\n"
fi

# 检查Vue导入路径
if grep -q "from './pdfjs-dist\|from 'pdfjs-dist/build\|from '../pdfjs-dist" "$VUE_FILE_PATH"; then
    printf "${RED}  错误：$VUE_FILE_PATH 导入路径错误！${RESET}\n"
    printf "  正确写法：import * as pdfjsLib from 'pdfjs-dist'\n"
    exit 1
else
    printf "${GREEN}  ✓ $VUE_FILE_PATH 导入路径正确${RESET}\n"
fi

# 安装其他前端依赖
if [ ! -d "frontend/node_modules" ]; then
    printf "${YELLOW}  未找到 node_modules，正在安装前端依赖...${RESET}\n"
    cd frontend && npm install && cd ..
    printf "${GREEN}  ✓ 前端依赖安装完成${RESET}\n"
fi

printf "${GREEN}✓ 前端依赖检查通过${RESET}\n"
printf "\n"

# ============================================
# 3. 检查端口占用
# ============================================
printf "${BLUE}[3/6] 检查端口占用...${RESET}\n"
check_port() {
    local PORT=$1
    local PORT_NAME=$2
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        printf "${YELLOW}警告：$PORT_NAME 端口 $PORT 已被占用${RESET}\n"
        if [ -t 0 ]; then
            read -p "是否继续启动？[y/N] " -n 1 -r
            printf "\n"
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
        else
            printf "${YELLOW}非交互模式：自动继续${RESET}\n"
        fi
    fi
}
check_port 8000 "后端"
check_port 3000 "前端"
printf "${GREEN}✓ 端口检查通过${RESET}\n"
printf "\n"

# ============================================
# 4. 启动后端服务（核心优化：容错检查）
# ============================================
printf "${BLUE}[4/6] 启动后端服务...${RESET}\n"

# 确保日志目录可写
mkdir -p logs && chmod 755 logs

# 启动后端（后台运行）
cd backend
# 激活虚拟环境后运行，确保环境变量正确
nohup bash -c 'source venv/bin/activate && python manage.py runserver' > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > ../logs/backend.pid
cd ..

# 优化：后端启动检查（容错+详细日志）
printf "等待后端服务启动（最多%d秒）...\n" $((BACKEND_CHECK_TIMES * BACKEND_CHECK_INTERVAL))
BACKEND_READY=0
for ((i=1; i<=BACKEND_CHECK_TIMES; i++)); do
    # 用curl容错：-f忽略错误，-s静默模式，避免set -e中断
    # 使用 || true 确保curl失败不会触发ERR陷阱
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/api/auth/login/ 2>/dev/null || echo "000")
    # 允许200（正常）、405（方法不允许）、403（权限）、000（未启动）
    if echo "$HTTP_CODE" | grep -q "200\|405\|403"; then
        BACKEND_READY=1
        printf "${GREEN}后端响应正常（HTTP $HTTP_CODE）${RESET}\n"
        break
    elif [ "$i" -lt "$BACKEND_CHECK_TIMES" ]; then
        printf "等待中...（第%d/%d次检查，HTTP响应: %s）\n" $i $BACKEND_CHECK_TIMES "$HTTP_CODE"
        sleep $BACKEND_CHECK_INTERVAL
    fi
done

# 处理检查结果
if [ $BACKEND_READY -eq 1 ]; then
    printf "${GREEN}✓ 后端服务启动成功 (http://127.0.0.1:8000)${RESET}\n"
else
    printf "${YELLOW}警告：后端服务未检测到正常响应（可能仍在启动中）${RESET}\n"
    printf "${YELLOW}后端日志位置：logs/backend.log${RESET}\n"
    if [ -t 0 ]; then
        read -p "是否继续启动前端？[y/N] " -n 1 -r
        printf "\n"
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            kill $BACKEND_PID 2>/dev/null || true
            exit 1
        fi
    else
        printf "${YELLOW}非交互模式：自动继续启动前端${RESET}\n"
    fi
fi
printf "\n"

# ============================================
# 5. 构建并启动前端服务
# ============================================
printf "${BLUE}[5/6] 构建并启动前端服务...${RESET}\n"

printf "正在构建前端项目...\n"
cd frontend
npm run build
if [ $? -ne 0 ]; then
    printf "${RED}错误：前端构建失败${RESET}\n"
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi
cd ..
printf "${GREEN}✓ 前端构建完成${RESET}\n"
printf "\n"

# 启动前端预览
printf "启动前端预览服务...\n"
cd frontend
nohup npm run preview > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../logs/frontend.pid
cd ..

# 检查前端启动
printf "等待前端服务启动（最多10秒）...\n"
FRONTEND_READY=0
for ((i=1; i<=10; i++)); do
    if curl -s -f -o /dev/null http://localhost:3000 2>/dev/null; then
        FRONTEND_READY=1
        break
    fi
    sleep 1
done

if [ $FRONTEND_READY -eq 1 ]; then
    printf "${GREEN}✓ 前端服务启动成功 (http://localhost:3000)${RESET}\n"
else
    printf "${YELLOW}警告：前端服务未检测到正常响应${RESET}\n"
    printf "${YELLOW}前端日志位置：logs/frontend.log${RESET}\n"
    if [ -t 0 ]; then
        read -p "是否继续？[y/N] " -n 1 -r
        printf "\n"
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            kill $BACKEND_PID 2>/dev/null || true
            kill $FRONTEND_PID 2>/dev/null || true
            exit 1
        fi
    else
        printf "${YELLOW}非交互模式：自动继续${RESET}\n"
    fi
fi
printf "\n"

# ============================================
# 6. 启动完成
# ============================================
printf "========================================\n"
printf "${GREEN}  启动完成！${RESET}\n"
printf "========================================\n"
printf "\n"
printf "${GREEN}✓ 后端服务：${RESET} http://127.0.0.1:8000\n"
printf "${GREEN}✓ 前端服务：${RESET} http://localhost:3000\n"
printf "\n"
printf "${YELLOW}注意：${RESET}\n"
printf "  1. 若后端无法访问，查看日志：logs/backend.log\n"
printf "  2. 停止服务：用 ./stop-no-hmr.sh（需单独创建）\n"
printf "  3. 后端PID：$BACKEND_PID，前端PID：$FRONTEND_PID\n"
printf "\n"

# 自动打开浏览器
if [ $FRONTEND_READY -eq 1 ]; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
        printf "正在打开浏览器...\n"
        open http://localhost:3000
    elif [[ "$OSTYPE" == "linux-gnu"* ]] && command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:3000 2>/dev/null || true
    fi
fi

printf "\n${GREEN}服务启动流程结束！${RESET}\n"