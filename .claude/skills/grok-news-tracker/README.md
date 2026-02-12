# Grok News Tracker

自动追踪热点资讯，定时汇总整理。从「你问我答」到「主动汇报」，让信息主动找到你。

## ✨ 特性

- 🔥 自动追踪多个信息源的热点话题
- 🤖 使用 Grok AI 智能分析和总结
- 📊 生成结构化的日报/周报
- ⏰ 支持定时自动执行
- 🎯 可自定义关注领域
- 📝 支持多种输出格式（Markdown、JSON、HTML）

## 🚀 快速开始

### 1. 设置 API 密钥

```bash
export GROK_API_KEY="sk-0bJSrMXaPm4Uvvs9RzjDWYh3eO81UkNpYELtfTMPJGRTxl6C"
```

### 2. 追踪今日热点

```bash
npx -y bun scripts/tracker.ts track
```

### 3. 查看生成的报告

```bash
cat reports/$(date +%Y-%m-%d).md
```

## 📖 使用指南

### 基础用法

```bash
# 追踪默认领域（tech, ai, startup）
npx -y bun scripts/tracker.ts track

# 追踪特定领域
npx -y bun scripts/tracker.ts track --sources ai,tech,dev

# 指定输出文件
npx -y bun scripts/tracker.ts track --output my-report.md

# 生成 HTML 格式报告
npx -y bun scripts/tracker.ts track --format html --output report.html

# 生成 JSON 格式（便于程序处理）
npx -y bun scripts/tracker.ts track --format json --output report.json
```

### 支持的信息源

- `tech` - 科技资讯
- `ai` - AI/机器学习
- `startup` - 创业/商业
- `finance` - 金融/投资
- `dev` - 开发者资讯
- `design` - 设计/创意
- `product` - 产品/运营

### 定时任务

使用系统 cron 实现每天自动追踪：

```bash
# 编辑 crontab
crontab -e

# 添加定时任务（每天早上8点执行）
0 8 * * * cd /path/to/project && export GROK_API_KEY="your-key" && npx -y bun .claude/skills/grok-news-tracker/scripts/tracker.ts track
```

或使用 Kiro Hooks（推荐）：

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

## 🔧 配置

### 环境变量

| 变量 | 说明 | 默认值 | 必需 |
|------|------|--------|------|
| `GROK_API_KEY` | Grok API 密钥 | - | ✅ |
| `GROK_BASE_URL` | API 基础地址 | `https://apipro.maynor1024.live` | ❌ |
| `GROK_MODEL` | 使用的模型 | `grok-4.1-fast` | ❌ |
| `OUTPUT_DIR` | 报告输出目录 | `reports` | ❌ |

### API 配置

本 skill 使用 Grok API（OpenAI 兼容接口）：

- **基础地址**：`https://apipro.maynor1024.live`
- **端点**：`/v1/chat/completions`
- **模型**：`grok-4.1-fast`
- **API 密钥**：`sk-0bJSrMXaPm4Uvvs9RzjDWYh3eO81UkNpYELtfTMPJGRTxl6C`

## 📊 输出示例

### Markdown 格式

```markdown
# 热点资讯日报 - 2024-01-15

## 📋 今日概览

今日科技领域最受关注的是...

## 🔥 详细资讯

### AI/机器学习

#### OpenAI 发布新模型

- **摘要**：OpenAI 发布了最新的 GPT-5 模型...
- **重要性**：⭐⭐⭐⭐⭐⭐⭐⭐⭐
- **来源**：OpenAI 官方博客
- **时间**：2024-01-15T08:00:00.000Z
```

### JSON 格式

```json
{
  "date": "2024-01-15",
  "categories": [
    {
      "name": "AI/机器学习",
      "topics": [
        {
          "title": "OpenAI 发布新模型",
          "summary": "OpenAI 发布了最新的 GPT-5 模型...",
          "source": "OpenAI 官方博客",
          "importance": 9,
          "timestamp": "2024-01-15T08:00:00.000Z",
          "category": "AI/机器学习"
        }
      ]
    }
  ]
}
```

## 🎯 使用场景

### 1. 个人信息管理

每天早上自动生成前一天的热点汇总，喝咖啡时快速浏览。

### 2. 团队信息同步

定时生成报告并分享到团队频道，保持团队对行业动态的了解。

### 3. 内容创作灵感

追踪热点话题，为内容创作提供灵感和素材。

### 4. 投资决策参考

关注金融、科技、创业领域的热点，辅助投资决策。

## 🛠️ 开发

### 项目结构

```
grok-news-tracker/
├── scripts/
│   ├── tracker.ts          # 主程序
│   ├── grok-client.ts      # Grok API 客户端
│   ├── formatter.ts        # 报告格式化
│   └── types.ts            # 类型定义
├── SKILL.md                # Skill 文档
├── README.md               # 项目说明
└── skill.json              # Skill 配置
```

### 依赖

- Bun >= 1.0.0

### 本地开发

```bash
# 克隆项目
git clone <repo-url>

# 进入目录
cd .claude/skills/grok-news-tracker

# 设置环境变量
export GROK_API_KEY="your-api-key"

# 运行
bun scripts/tracker.ts track
```

## 📝 待办事项

- [ ] 支持更多信息源（RSS、Twitter、Reddit 等）
- [ ] 添加关键词过滤和订阅
- [ ] 支持多语言资讯
- [ ] 添加趋势分析和预测
- [ ] 集成通知服务（邮件、Slack、微信等）
- [ ] Web 界面查看历史报告
- [ ] 实现历史报告汇总功能
- [ ] 添加数据持久化（SQLite）
- [ ] 支持自定义分析提示词

## 📄 许可证

MIT

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📮 联系

- GitHub: [@baoyu](https://github.com/baoyu)
- Email: baoyu@example.com
