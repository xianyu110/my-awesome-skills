# 快速开始指南

## 5分钟上手

### 步骤1：准备 GitHub Token

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 生成并复制 token（格式：`ghp_xxxxxxxxxxxx`）

### 步骤2：运行命令

```bash
bun .claude/skills/ai-mirror-publisher/scripts/publish.ts \
  --tools "chatgpt-gpt5.2,claude-opus-4.5,gemini-3-pro" \
  --github-user "你的GitHub用户名" \
  --github-token "你的GitHub Token" \
  --main-url "https://geminiai.asia/list/#/home" \
  --nav-url "https://chatgpt-plus.top/"
```

### 步骤3：等待完成

- 每个工具约2-3分钟
- 3个工具总共约8-10分钟
- 自动生成图片、内容、创建仓库、推送代码

### 步骤4：查看结果

命令完成后会显示所有仓库的URL：

```
✅ 完成！共创建 3 个图文并茂的仓库

📦 仓库列表：
1. https://github.com/你的用户名/chatgpt-gpt5.2-mirror
2. https://github.com/你的用户名/claude-opus-4.5-mirror
3. https://github.com/你的用户名/gemini-3-pro-mirror
```

## 使用配置文件（推荐）

### 创建配置文件

```bash
cat > my-config.json << 'EOF'
{
  "ai_tools": [
    "chatgpt-gpt5.2",
    "claude-opus-4.5",
    "gemini-3-pro"
  ],
  "github_username": "你的用户名",
  "github_token": "你的Token",
  "mirror_urls": {
    "main": "https://geminiai.asia/list/#/home",
    "nav": "https://chatgpt-plus.top/"
  }
}
EOF
```

### 运行

```bash
bun .claude/skills/ai-mirror-publisher/scripts/publish.ts --config my-config.json
```

## 支持的AI工具

### 2025年最新版本

- `chatgpt-gpt5.2` - ChatGPT GPT-5.2（2025年12月）
- `claude-opus-4.5` - Claude Opus 4.5（编码最强）
- `gemini-3-pro` - Gemini 3 Pro（100万token）
- `grok-4.1` - Grok 4.1（实时信息）
- `deepseek-v3.2` - DeepSeek v3.2（开源）

### 其他版本

- `chatgpt-gpt4o` - GPT-4o
- `claude-35-sonnet` - Claude 3.5 Sonnet
- `gemini-25-pro` - Gemini 2.5 Pro

## 生成内容预览

每个AI工具自动生成：

### 1. 6张专业配图

- **封面图** - notion风格，品牌色点缀
- **概念图** - tech风格，技术架构
- **流程图** - notion风格，注册步骤
- **对比图** - minimal风格，功能对比
- **场景图** - warm风格，应用场景
- **FAQ图** - notion风格，常见问题

### 2. 完整使用指南

```markdown
# ChatGPT GPT-5.2官网镜像站使用指南（国内直连）

## ✅ 精选入口
- 主入口：https://geminiai.asia/list/#/home
- 镜像导航：https://chatgpt-plus.top/

## 📋 目录导航
- 什么是 ChatGPT GPT-5.2？
- 为什么选择镜像网站？
- 精选镜像站推荐
- 核心优势与功能
- 快速开始使用
- 常见问题FAQ
- 隐私安全建议

[详细内容...]
```

### 3. GitHub仓库

- 自动创建仓库
- 推送所有文件
- 包含图片和文档
- 可直接访问

## 常见问题

### Q: 需要多长时间？

A: 
- 单个工具：2-3分钟
- 3个工具：8-10分钟
- 5个工具：12-15分钟

### Q: 图片生成失败怎么办？

A: 单张图片失败不影响整体流程，会继续生成其他图片和内容

### Q: 仓库已存在怎么办？

A: 自动跳过创建步骤，直接推送更新内容

### Q: 如何自定义内容？

A: 修改配置文件中的参数，或编辑生成后的文件

### Q: Token 安全吗？

A: 
- ⚠️ 不要将 token 提交到版本控制
- ⚠️ 使用配置文件时添加到 .gitignore
- ✅ 定期轮换 token

## 下一步

### 批量生成更多工具

```bash
bun .claude/skills/ai-mirror-publisher/scripts/publish.ts \
  --tools "chatgpt-gpt5.2,claude-opus-4.5,gemini-3-pro,grok-4.1,deepseek-v3.2" \
  --github-user "你的用户名" \
  --github-token "你的Token" \
  --main-url "https://geminiai.asia/list/#/home" \
  --nav-url "https://chatgpt-plus.top/"
```

### 自定义配图风格

```bash
# 使用 tech 风格（科技感）
--style tech

# 使用 minimal 风格（极简）
--style minimal

# 使用 warm 风格（温暖）
--style warm
```

### 查看完整文档

```bash
cat .claude/skills/ai-mirror-publisher/SKILL.md
cat .claude/skills/ai-mirror-publisher/README.md
```

## 获取帮助

```bash
# 查看帮助信息
bun .claude/skills/ai-mirror-publisher/scripts/publish.ts --help

# 查看示例配置
cat .claude/skills/ai-mirror-publisher/examples/config.json
```

---

**开始一键生成图文并茂的AI镜像站指南吧！🚀**
