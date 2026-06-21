#!/bin/bash
# 启动 mitmweb 并只显示 OpenAI API 请求

PORT=${1:-8080}
WEB_PORT=${2:-8081}

echo "🚀 启动 mitmweb（仅显示 OpenAI 请求）..."
echo "   代理端口: $PORT"
echo "   Web 界面: http://127.0.0.1:$WEB_PORT"
echo "   过滤规则: ~d api.openai.com"
echo ""

mitmweb --listen-port "$PORT" --web-port "$WEB_PORT" --set flow_filter='~d api.openai.com'
