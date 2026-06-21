#!/bin/bash
# 启动 Go 后端并配置使用 mitmproxy 代理

PROXY_PORT=${1:-8080}
BACKEND_DIR=${2:-./backend}

echo "🔧 配置代理环境变量..."
export HTTP_PROXY="http://localhost:$PROXY_PORT"
export HTTPS_PROXY="http://localhost:$PROXY_PORT"

echo "   HTTP_PROXY=$HTTP_PROXY"
echo "   HTTPS_PROXY=$HTTPS_PROXY"
echo ""

echo "🚀 启动后端服务..."
cd "$BACKEND_DIR" && go run cmd/main.go
