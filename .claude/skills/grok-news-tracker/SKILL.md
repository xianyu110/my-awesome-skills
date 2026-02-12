---
name: grok-news-tracker
description: 自动追踪热点资讯，定时汇总整理。使用 Grok AI 分析和总结热点话题，让信息主动找到你。
---

# Grok News Tracker

自动追踪热点资讯，一觉醒来所有资讯已整理完毕。从「你问我答」到「主动汇报」，让信息主动找到你。

## 快速开始

```bash
# 追踪今日热点
npx -y bun scripts/tracker.ts track

# 追踪特定领域
npx -y bun scripts/tracker.ts track --sources tech,ai,startup

# 生成报告
npx -y bun scripts/tracker.ts track --output daily-report.md

# 查看历史报告
npx -y bun scripts/tracker.ts report --days 7
```

## 功能特性

- 🔥 自动追踪多个信息源的热点话题
- 🤖 使用 Grok AI 智能分析和总结
- 📊 生成结构化的日报/周报
- ⏰ 支持定时自动执行
- 🎯 可自定义关注领域
- 📝 支持多种输出格式（Markdown、JSON、HTML）

## 命令说明

### track - 追踪热点

立即追踪热点资讯并生成报告。

```bash
# 基础用法
npx -y bun scripts/tracker.ts track

# 指定信息源
npx -y bun scripts/tracker.ts track --sources tech,ai,startup,finance

# 指定输出文件
npx -y bun scripts/tracker.ts track --output reports/$(date +%Y-%m-%d).md

# 指定输出格式
npx -y bun scripts/tracker.ts track --format json

# 组合使用
npx -y bun scripts/tracker.ts track --sources ai,tech --output ai-report.md
```

### report - 生成汇总报告

生成历史数据的汇总报告。

```bash
# 生成最近7天的报告
npx -y bun scripts/tracker.ts report --days 7

# 生成HTML格式报告
npx -y bun scripts/tracker.ts report --days 7 --format html --output weekly.html

# 生成JSON格式（便于程序处理）
npx -y bun scripts/tracker.ts report --days 1 --format json
```

### schedule - 设置定时任务

配置自动追踪的时间表。

```bash
# 每天早上8点执行
npx -y bun scripts/tracker.ts schedule --cron "0 8 * * *"

# 每天早晚各执行一次
npx -y bun scripts/tracker.ts schedule --cron "0 8,20 * * *"

# 工作日早上执行
npx -y bun scripts/tracker.ts schedule --cron "0 8 * * 1-5"
```

## 配置选项

### 环境变量

| 变量 | 说明 | 必需 |
|------|------|------|
| `GROK_API_KEY` | Grok API 密钥 | 是 |
| `GROK_BASE_URL` | API 基础地址 | 否 |
| `GROK_MODEL` | 使用的模型 | 否 |
| `NEWS_SOURCES` | 默认信息源（逗号分隔） | 否 |
| `OUTPUT_DIR` | 报告输出目录 | 否 |

### 信息源类型

- `tech` - 科技资讯
- `ai` - AI/机器学习
- `startup` - 创业/商业
- `finance` - 金融/投资
- `dev` - 开发者资讯
- `design` - 设计/创意
- `product` - 产品/运营

## 输出格式

### Markdown 格式（默认）

```markdown
# 热点资讯日报 - 2024-01-15

## 🔥 今日热点

### AI 领域
- **OpenAI 发布新模型**
  - 摘要：...
  - 来源：...
  - 链接：...

### 科技领域
- **Apple Vision Pro 上市**
  - 摘要：...
  ...
```

### JSON 格式

```json
{
  "date": "2024-01-15",
  "categories": [
    {
      "name": "AI",
      "topics": [
        {
          "title": "OpenAI 发布新模型",
          "summary": "...",
          "source": "...",
          "url": "...",
          "importance": 9
        }
      ]
    }
  ]
}
```

## 使用场景

### 1. 每日晨报

配置每天早上自动生成前一天的热点汇总：

```bash
# 设置定时任务
npx -y bun scripts/tracker.ts schedule --cron "0 8 * * *"

# 或使用系统 cron
0 8 * * * cd /path/to/project && npx -y bun .claude/skills/grok-news-tracker/scripts/tracker.ts track --output reports/$(date +\%Y-\%m-\%d).md
```

### 2. 领域专注

只关注特定领域的资讯：

```bash
# AI 从业者
npx -y bun scripts/tracker.ts track --sources ai,tech,dev

# 创业者
npx -y bun scripts/tracker.ts track --sources startup,finance,product

# 设计师
npx -y bun scripts/tracker.ts track --sources design,product,tech
```

### 3. 周报生成

每周一生成上周汇总：

```bash
# 每周一早上8点
0 8 * * 1 cd /path/to/project && npx -y bun .claude/skills/grok-news-tracker/scripts/tracker.ts report --days 7 --output reports/weekly-$(date +\%Y-W\%V).md
```

## API 配置

本 skill 使用 Grok API（OpenAI 兼容接口）：

- 基础地址：`https://apipro.maynor1024.live`
- 端点：`/v1/chat/completions`
- 模型：`grok-4.1-fast`

## 示例工作流

### 配合 Kiro Hooks 实现自动化

创建一个 hook，每天自动追踪并通知：

```json
{
  "name": "Daily News Tracker",
  "version": "1.0.0",
  "when": {
    "type": "userTriggered"
  },
  "then": {
    "type": "askAgent",
    "prompt": "使用 grok-news-tracker 追踪今日热点，生成报告并总结最重要的3条资讯"
  }
}
```

## 高级用法

### 自定义分析提示词

创建 `prompts/analysis.md` 文件自定义分析逻辑：

```markdown
请分析以下资讯，重点关注：
1. 对行业的影响
2. 技术创新点
3. 商业价值
4. 发展趋势
```

### 集成到工作流

```bash
# 生成报告并发送到企业微信
npx -y bun scripts/tracker.ts track --format json | \
  jq '.categories[0].topics[0]' | \
  curl -X POST https://qyapi.weixin.qq.com/...
```

## 故障排查

### API 密钥错误

确保环境变量正确设置：

```bash
export GROK_API_KEY="sk-0bJSrMXaPm4Uvvs9RzjDWYh3eO81UkNpYELtfTMPJGRTxl6C"
```

### 网络连接问题

检查 API 基础地址是否可访问：

```bash
curl https://apipro.maynor1024.live/v1/models
```

### 输出目录不存在

自动创建输出目录，或手动创建：

```bash
mkdir -p reports
```

## 开发计划

- [ ] 支持更多信息源（RSS、Twitter、Reddit 等）
- [ ] 添加关键词过滤和订阅
- [ ] 支持多语言资讯
- [ ] 添加趋势分析和预测
- [ ] 集成通知服务（邮件、Slack、微信等）
- [ ] Web 界面查看历史报告
