---
name: wechat-reader
description: 读取微信公众号文章内容，通过 curl + User-Agent 伪装绕过防爬
agent_created: true
tags: [wechat, 微信, 抓取, 文章读取]
tools: [Bash, WebFetch]
---

# Wechat Reader

读取微信公众号文章（mp.weixin.qq.com），提取标题、正文概要等信息。

## 核心方法

微信文章有防爬限制，直接 WebFetch 会失败。正确方法是 **curl + User-Agent 伪装**：

```bash
curl -s --max-time 15 \
  -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  "https://mp.weixin.qq.com/s/{article_id}" \
  | grep -E "og:title|og:description|og:image" \
  | sed 's/.*content="//;s/".*//'
```

### 关键技术点

1. **User-Agent 必须伪装桌面浏览器**，移动端或默认 curl 的 UA 会被拦截
2. **macOS grep 不支持 `-P`**，用 `sed` 代替正则提取
3. **sed 提取语法**：`sed 's/.*content="//;s/".*//'` 从 `<meta content="xxx"` 提取 xxx
4. **超时设置**：`--max-time 15` 防止长时间等待
5. **重试策略**：可以尝试不同的 UA（桌面 Chrome 效果最好）

### 可用的 User-Agent

```bash
# 桌面 Chrome（推荐，成功率最高）
-A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# iPhone Safari（备选）
-A "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15"

# Windows Chrome（备选）
-A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
```

## 提取内容

### 标题
```bash
curl -s -A "..." "https://mp.weixin.qq.com/s/{id}" | grep -oP '(?<=og:title" content=")[^"]*'
# 或用 sed（macOS 兼容）
curl -s -A "..." "https://mp.weixin.qq.com/s/{id}" | sed -n 's/.*og:title.*content="\([^"]*\)".*/\1/p'
```

### 描述/摘要
```bash
curl -s -A "..." "https://mp.weixin.qq.com/s/{id}" | grep "og:description" | sed 's/.*content="//;s/".*//'
```

### 封面图
```bash
curl -s -A "..." "https://mp.weixin.qq.com/s/{id}" | grep "og:image" | sed 's/.*content="//;s/".*//'
```

### 完整摘要（og:description 通常包含全文）
微信文章的 `og:description` meta 标签会包含完整正文，是获取内容的最佳方式。

## 完整工作流

```bash
#!/bin/bash
# wechat-fetch.sh

UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
URL=$1

if [ -z "$URL" ]; then
  echo "Usage: $0 <wechat_article_url>"
  exit 1
fi

echo "=== 微信文章抓取 ==="
echo "URL: $URL"
echo ""

CONTENT=$(curl -s --max-time 15 -A "$UA" "$URL")

TITLE=$(echo "$CONTENT" | grep "og:title" | sed 's/.*content="//;s/".*//')
DESC=$(echo "$CONTENT" | grep "og:description" | sed 's/.*content="//;s/".*//')
IMAGE=$(echo "$CONTENT" | grep "og:image" | sed 's/.*content="//;s/".*//')

echo "标题: $TITLE"
echo ""
echo "内容:"
echo "$DESC"
echo ""
[ -n "$IMAGE" ] && echo "封面: $IMAGE"
```

## 注意事项

- **不能获取完整正文**：微信只会在 og:description 暴露摘要，正文需要 JS 动态加载
- **代理问题**：如果系统有代理（如 HTTPS_PROXY），curl 可能被代理拦截导致超时，加 `--noproxy '*'` 绕过
- **时间戳 URL**：微信文章 URL 可能带时间戳参数，不影响抓取
- **多次请求失败**：可能是 IP 被临时封禁，等几分钟再试

## 示例

```bash
# 抓取文章
curl -s -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  "https://mp.weixin.qq.com/s/xie1wKx3risBi_sTKr5OEQ" \
  | grep "og:description" \
  | sed 's/.*content="//;s/".*//'
```
