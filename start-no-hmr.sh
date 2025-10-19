#!/bin/bash

# ============================================
# CCD 项目无 HMR 模式启动脚本 (macOS/Linux)
# ============================================
# 功能：
# 1. 检查依赖环境
# 2. 启动后端服务 (Django, 端口 8000)
# 3. 构建前端项目
# 4. 启动前端预览服务 (端口 3000, 无 HMR)
# ============================================

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RESET='\033[0m'

# 错误处理
set -e
trap 'echo -e "${RED}错误：脚本执行失败${RESET}"; exit 1' ERR

echo ""
echo "========================================"
echo "  CCD 项目启动 - 无 HMR 模式"
echo "========================================"
echo ""

# 检查是否在项目根目录
if [ ! -d "backend" ]; then
    echo -e "${RED}错误：未找到 backend 目录${RESET}"
    echo "请在项目根目录下运行此脚本"
    exit 1
fi

if [ ! -d "frontend" ]; then
    echo -e "${RED}错误：未找到 frontend 目录${RESET}"
    echo "请在项目根目录下运行此脚本"
    exit 1
fi

# ============================================
# 1. 检查后端依赖
# ============================================
echo -e "${BLUE}[1/5] 检查后端依赖...${RESET}"

if [ ! -d "backend/venv" ]; then
    echo -e "${RED}错误：未找到 Python 虚拟环境${RESET}"
    echo "请先运行以下命令创建虚拟环境："
    echo "  cd backend"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

if [ ! -f "backend/venv/bin/python" ]; then
    echo -e "${RED}错误：虚拟环境不完整${RESET}"
    echo "请重新创建虚拟环境"
    exit 1
fi

echo -e "${GREEN}✓ 后端依赖检查通过${RESET}"
echo ""

# ============================================
# 2. 检查前端依赖
# ============================================
echo -e "${BLUE}[2/5] 检查前端依赖...${RESET}"

if [ ! -d "frontend/node_modules" ]; then
    echo -e "${YELLOW}警告：未找到 node_modules 目录${RESET}"
    echo "正在安装前端依赖..."
    cd frontend
    npm install
    if [ $? -ne 0 ]; then
        echo -e "${RED}错误：前端依赖安装失败${RESET}"
        exit 1
    fi
    cd ..
fi

echo -e "${GREEN}✓ 前端依赖检查通过${RESET}"
echo ""

# ============================================
# 3. 检查端口占用
# ============================================
echo -e "${BLUE}[3/5] 检查端口占用...${RESET}"

# 检查 8000 端口
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${YELLOW}警告：端口 8000 已被占用${RESET}"
    echo "请手动停止占用该端口的进程，或使用 ./stop-no-hmr.sh 停止服务"
    read -p "是否继续启动（可能会失败）？[y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 检查 3000 端口
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${YELLOW}警告：端口 3000 已被占用${RESET}"
    echo "请手动停止占用该端口的进程，或使用 ./stop-no-hmr.sh 停止服务"
    read -p "是否继续启动（可能会失败）？[y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo -e "${GREEN}✓ 端口检查通过${RESET}"
echo ""

# ============================================
# 4. 启动后端服务
# ============================================
echo -e "${BLUE}[4/5] 启动后端服务...${RESET}"

# 创建日志目录
mkdir -p logs

# 启动后端（后台运行）
cd backend
source venv/bin/activate
nohup python manage.py runserver > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > ../logs/backend.pid
cd ..

# 等待后端启动
echo "等待后端服务启动..."
sleep 5

# 检查后端是否启动成功
if curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/api/auth/login/ 2>/dev/null | grep -q "200\|405\|403"; then
    echo -e "${GREEN}✓ 后端服务启动成功 (http://127.0.0.1:8000)${RESET}"
else
    echo -e "${YELLOW}警告：后端服务可能未正常启动${RESET}"
    echo "请检查日志文件：logs/backend.log"
    read -p "是否继续启动前端？[y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        # 停止后端
        kill $BACKEND_PID 2>/dev/null || true
        exit 1
    fi
fi
echo ""

# ============================================
# 5. 构建并启动前端服务
# ============================================
echo -e "${BLUE}[5/5] 构建并启动前端服务...${RESET}"

# 构建前端
echo "正在构建前端项目..."
cd frontend
npm run build
if [ $? -ne 0 ]; then
    echo -e "${RED}错误：前端构建失败${RESET}"
    # 停止后端
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi
cd ..

echo -e "${GREEN}✓ 前端构建完成${RESET}"
echo ""

# 启动前端预览服务（后台运行）
echo "启动前端预览服务..."
cd frontend
nohup npm run preview > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../logs/frontend.pid
cd ..

# 等待前端启动
echo "等待前端服务启动..."
sleep 3

echo ""
echo "========================================"
echo -e "  ${GREEN}启动完成！${RESET}"
echo "========================================"
echo ""
echo -e "${GREEN}✓ 后端服务：${RESET} http://127.0.0.1:8000"
echo -e "${GREEN}✓ 前端服务：${RESET} http://localhost:3000"
echo ""
echo -e "${YELLOW}模式说明：${RESET}"
echo "  - 前端运行在 Preview 模式（生产构建）"
echo "  - 无 HMR（热模块替换）功能"
echo "  - 无 WebSocket 连接"
echo "  - 适合移动端测试（拍照不会刷新页面）"
echo ""
echo -e "${YELLOW}注意事项：${RESET}"
echo "  - 修改代码后需要重新构建前端"
echo "  - 使用 ./stop-no-hmr.sh 停止所有服务"
echo "  - 日志文件保存在 logs 目录"
echo ""
echo -e "${YELLOW}进程 ID：${RESET}"
echo "  - 后端 PID: $BACKEND_PID"
echo "  - 前端 PID: $FRONTEND_PID"
echo ""
echo -e "${BLUE}提示：服务已在后台运行${RESET}"
echo ""

# 在 macOS 上自动打开浏览器
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "正在打开浏览器..."
    sleep 2
    open http://localhost:3000
fi

# 在 Linux 上尝试打开浏览器
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if command -v xdg-open &> /dev/null; then
        echo "正在打开浏览器..."
        sleep 2
        xdg-open http://localhost:3000 2>/dev/null || true
    fi
fi

echo -e "${GREEN}服务已成功启动！${RESET}"
echo ""

