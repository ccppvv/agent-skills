# mitmproxy 命令参考

## 常用命令

### 启动命令

```bash
# 启动交互式界面
mitmproxy

# 启动 Web 界面（推荐）
mitmweb

# 启动命令行输出
mitmdump

# 自定义端口
mitmproxy -p 9090
mitmweb --listen-port 9090 --web-port 8081
```

### 过滤器语法

```bash
# 只显示特定域名
--set flow_filter='~d api.openai.com'

# 只显示 POST 请求
--set flow_filter='~m POST'

# 组合过滤器（域名 + 方法）
--set flow_filter='~d api.openai.com & ~m POST'

# 只显示特定路径
--set flow_filter='~u /v1/chat/completions'

# 排除特定域名
--set flow_filter='!~d example.com'
```

### 保存和回放

```bash
# 保存请求到文件
mitmdump -w requests.flow

# 回放保存的请求
mitmdump -r requests.flow

# 保存为文本日志
mitmdump -w requests.log
```

### 交互式快捷键

在 mitmproxy 交互界面中：

- `Enter` - 查看请求详情
- `Tab` - 在请求/响应之间切换
- `q` - 返回/退出
- `?` - 显示帮助
- `/` - 搜索
- `f` - 设置过滤器
- `e` - 编辑请求/响应
- `r` - 重放请求

## 过滤器表达式

| 表达式 | 说明 | 示例 |
|--------|------|------|
| `~d` | 域名匹配 | `~d openai.com` |
| `~m` | HTTP 方法 | `~m POST` |
| `~u` | URL 路径 | `~u /v1/chat` |
| `~s` | HTTP 状态码 | `~s 200` |
| `~c` | 响应码范围 | `~c 4xx` |
| `~h` | 请求头 | `~h Authorization` |
| `~b` | 请求/响应体 | `~b "error"` |
| `~q` | 请求 | `~q` |
| `~s` | 响应 | `~s` |
| `&` | 逻辑与 | `~d openai.com & ~m POST` |
| `\|` | 逻辑或 | `~m POST \| ~m PUT` |
| `!` | 逻辑非 | `!~d example.com` |

## 环境变量配置

```bash
# 配置 HTTP 代理
export HTTP_PROXY=http://localhost:8080
export HTTPS_PROXY=http://localhost:8080

# 取消代理
unset HTTP_PROXY
unset HTTPS_PROXY

# 验证代理配置
echo $HTTP_PROXY
```

## HTTPS 证书处理

### 安装证书（macOS）

```bash
# 打开证书文件
open ~/.mitmproxy/mitmproxy-ca-cert.pem

# 或使用命令行安装
sudo security add-trusted-cert -d -r trustRoot \
  -k /Library/Keychains/System.keychain \
  ~/.mitmproxy/mitmproxy-ca-cert.pem
```

### Go 程序跳过证书验证（仅测试用）

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

## 常见问题

### 问题：代理连接失败
**解决**：确保 mitmproxy 正在运行，端口未被占用

### 问题：HTTPS 请求失败
**解决**：安装 mitmproxy CA 证书，或在测试代码中跳过证书验证

### 问题：看不到请求
**解决**：
1. 确认环境变量已设置：`echo $HTTP_PROXY`
2. 确认程序在设置代理后启动
3. 检查防火墙设置
