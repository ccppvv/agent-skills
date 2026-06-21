#!/bin/bash
# 一键启动 mitmweb 和带代理的后端服务

PROXY_PORT=8080
WEB_PORT=8081
BACKEND_DIR="./backend"

# 启动 mitmweb（后台运行）
echo "🚀 启动 mitmweb（后台运行）..."
mitmweb --listen-port "$PROXY_PORT" --web-port "$WEB_PORT" > /dev/null 2>&1 &
MITMWEB_PID=$!

echo "   代理端口: $PROXY_PORT"
echo "   Web 界面: http://127.0.0.1:$WEB_PORT"
echo "   进程 PID: $MITMWEB_PID"
echo ""

# 等待 mitmweb 启动
echo "⏳ 等待 mitmweb 启动..."
sleep 3

# 配置代理环境变量
export HTTP_PROXY="http://localhost:$PROXY_PORT"
export HTTPS_PROXY="http://localhost:$PROXY_PORT"

echo "🚀 启动后端服务（使用代理）..."
cd "$BACKEND_DIR" && go run cmd/main.go

# 清理：当后端退出时，停止 mitmweb
echo ""
echo "🛑 停止 mitmweb..."
kill $MITMWEB_PID 2>/dev/null
