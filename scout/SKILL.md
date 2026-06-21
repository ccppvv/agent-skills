---
name: scout
description: Monitor and intercept HTTP/HTTPS requests from Go backend using mitmproxy. Use when you need to (1) Debug API requests sent by the backend, (2) View request/response details for OpenAI API calls, (3) Troubleshoot API key testing issues, (4) Analyze network traffic patterns, (5) Inspect authentication headers and payloads, or (6) Monitor proxy behavior in the codex backend service.
---

# Scout

Monitor HTTP/HTTPS requests from Go backend applications using mitmproxy.

## Quick Start

### Option 1: One-Command Launch (推荐)

启动 mitmweb 和带代理的后端服务：

```bash
bash scripts/start_all.sh
```

这会自动：
- 启动 mitmweb（后台运行）
- 配置代理环境变量
- 启动后端服务
- 在浏览器中打开 http://127.0.0.1:8081 查看请求

### Option 2: 分步启动

**步骤 1**: 启动 mitmweb

```bash
bash scripts/start_mitmweb.sh [代理端口] [Web端口]
# 默认: 代理端口=8080, Web端口=8081
```

**步骤 2**: 在另一个终端启动后端

```bash
bash scripts/start_backend_with_proxy.sh [代理端口] [后端目录]
# 默认: 代理端口=8080, 后端目录=./backend
```

### Option 3: 只监听 OpenAI 请求

```bash
bash scripts/filter_openai.sh [代理端口] [Web端口]
```

## 使用场景

### 场景 1: 调试 API Key 测试

当测试 API Key 时，查看实际发送的请求：

1. 启动监听：`bash scripts/filter_openai.sh`
2. 在后端执行 Key 测试
3. 在 Web 界面查看请求详情（Authorization header、请求体、响应）

### 场景 2: 排查代理问题

检查后端的代理请求是否正确转发：

1. 启动完整监听：`bash scripts/start_all.sh`
2. 触发代理请求（如 `/v1/chat/completions`）
3. 验证请求头、Key 选择、响应处理

### 场景 3: 分析错误响应

当遇到 401/403/429 错误时：

1. 启动监听
2. 重现错误场景
3. 在 mitmweb 中查看完整的错误响应体和状态码

## Web 界面操作

访问 http://127.0.0.1:8081 后：

- **查看请求列表** - 实时显示所有拦截的请求
- **点击请求** - 查看详细的请求头、请求体、响应头、响应体
- **搜索过滤** - 使用搜索框过滤特定请求
- **导出数据** - 保存请求数据用于后续分析

## 高级用法

### 自定义过滤器

编辑脚本中的 `--set flow_filter` 参数：

```bash
# 只显示 POST 请求
--set flow_filter='~m POST'

# 显示特定路径
--set flow_filter='~u /v1/chat/completions'

# 组合条件
--set flow_filter='~d api.openai.com & ~m POST'
```

更多过滤器语法见 [references/mitmproxy_commands.md](references/mitmproxy_commands.md)

### 保存请求日志

```bash
# 保存到文件
mitmdump -w requests.flow

# 回放查看
mitmdump -r requests.flow
```

### 手动配置代理

如果需要手动配置：

```bash
export HTTP_PROXY=http://localhost:8080
export HTTPS_PROXY=http://localhost:8080
go run cmd/main.go
```

## HTTPS 证书问题

如果遇到证书错误，有两种解决方案：

### 方案 1: 安装 mitmproxy 证书（推荐）

```bash
# macOS
open ~/.mitmproxy/mitmproxy-ca-cert.pem
```

在钥匙串访问中将证书设为"始终信任"。

### 方案 2: 跳过证书验证（仅测试）

在 Go 代码中临时添加：

```go
import (
    "crypto/tls"
    "net/http"
)

client := &http.Client{
    Transport: &http.Transport{
        TLSClientConfig: &tls.Config{
            InsecureSkipVerify: true,
        },
    },
}
```

**警告**: 生产环境不要使用 `InsecureSkipVerify`！

## 故障排除

### 看不到请求

1. 确认 mitmweb 正在运行
2. 检查环境变量：`echo $HTTP_PROXY`
3. 确保后端在设置代理后启动
4. 检查端口是否被占用：`lsof -i :8080`

### 代理连接失败

1. 确认 mitmproxy 已安装：`mitmproxy --version`
2. 检查端口冲突
3. 尝试更换端口

### 请求超时

1. 检查网络连接
2. 确认 OpenAI API 可访问
3. 查看 mitmweb 中的错误信息

## 参考资料

- 完整命令参考：[references/mitmproxy_commands.md](references/mitmproxy_commands.md)
- mitmproxy 官方文档：https://docs.mitmproxy.org/
