#!/bin/bash
# 启动 mitmweb 用于监听 HTTP/HTTPS 请求

PORT=${1:-8080}
WEB_PORT=${2:-8081}

echo "🚀 启动 mitmweb..."
echo "   代理端口: $PORT"
echo "   Web 界面: http://127.0.0.1:$WEB_PORT"
echo ""

mitmweb --listen-port "$PORT" --web-port "$WEB_PORT"
