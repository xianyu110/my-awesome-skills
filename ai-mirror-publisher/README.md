# AI Mirror Site Publisher

一键生成图文并茂的AI镜像站使用指南并发布到GitHub

## 快速开始

### 1. 安装依赖

```bash
# 确保已安装 bun
curl -fsSL https://bun.sh/install | bash

# 确保已安装 git
git --version
```

### 2. 准备 GitHub Token

访问 https://github.com/settings/tokens 创建 Personal Access Token

权限需要：
- `repo` (完整仓库访问权限)
- `workflow` (可选，如果需要 GitHub Actions)

### 3. 基础用法

```bash
bun .claude/skills/ai-mirror-publisher/scripts/publish.ts \
  --tools "chatgpt-gpt5.2,claude-opus-4.5,gemini-3-pro" \
  --github-user "your-username" \
  --github-token "ghp_xxxxxxxxxxxx" \
  --main-url "https://geminiai.asia/list/#/home" \
  --nav-url "https://chatgpt-plus.top/"
```

### 4. 使用配置文件（推荐）

创建 `config.json`:

```json
{
  "ai_tools": [
    "chatgpt-gpt5.2",
    "claude-opus-4.5",
    "gemini-3-pro",
    "grok-4.1",
    "deepseek-v3.2"
  ],
  "github_username": "your-username",
  "github_token": "ghp_xxxxxxxxxxxx",
  "mirror_urls": {
    "main": "https://geminiai.asia/list/#/home",
    "nav": "https://chatgpt-plus.top/"
  },
  "image_count": 6,
  "image_style": "notion",
  "base_directory": "./ai-mirror-repos"
}
```

运行：

```bash
bun .claude/skills/ai-mirror-publisher/scripts/publish.ts --config config.json
```

## 支持的AI工具

- `chatgpt-gpt5.2` - ChatGPT GPT-5.2 (2025年12月最新)
- `claude-opus-4.5` - Claude Opus 4.5 (编码最强)
- `gemini-3-pro` - Gemini 3 Pro (100万token上下文)
- `grok-4.1` - Grok 4.1 (实时信息)
- `deepseek-v3.2` - DeepSeek v3.2 (开源性价比)

## 生成内容

每个AI工具自动生成：

1. **6张专业配图**
   - 封面图（notion风格）
   - 概念图（tech风格）
   - 流程图（notion风格）
   - 对比图（minimal风格）
   - 场景图（warm风格）
   - FAQ图（notion风格）

2. **完整的使用指南**
   - README.md（Markdown格式）
   - index.html（网页版本）
   - 图片资源

3. **GitHub仓库**
   - 自动创建仓库
   - 推送所有内容
   - 返回仓库URL

## 命令行参数

### 必需参数

- `--tools` - AI工具列表（逗号分隔）
- `--github-user` - GitHub用户名
- `--github-token` - GitHub Token
- `--main-url` - 主镜像站入口
- `--nav-url` - 镜像导航入口

### 可选参数

- `--secondary-url` - 备用镜像站入口
- `--images` - 图片数量（默认6）
- `--style` - 配图风格（默认notion）
- `--output` - 输出目录（默认./ai-mirror-repos）
- `--config` - 配置文件路径

## 预期输出

```
🚀 开始批量生成AI镜像站指南...
========================================

[1/3] 处理 chatgpt-gpt5.2...
  ✓ 创建目录
  [图片] 生成中: cover.jpg
  [图片] ✓ 完成: cover.jpg
  [图片] 生成中: concept.jpg
  [图片] ✓ 完成: concept.jpg
  ...
  [图片] ✓ 完成！成功生成 6/6 张图片
  ✓ 生成内容
  ✓ 创建GitHub仓库
  ✓ 推送代码
  📦 https://github.com/your-username/chatgpt-gpt5.2-mirror

[2/3] 处理 claude-opus-4.5...
  ...

========================================
✅ 完成！共创建 3 个图文并茂的仓库

📦 仓库列表：
1. https://github.com/your-username/chatgpt-gpt5.2-mirror
2. https://github.com/your-username/claude-opus-4.5-mirror
3. https://github.com/your-username/gemini-3-pro-mirror

⏱️  总耗时：约 8-10 分钟
📊 成功率：100%
========================================
```

## 性能指标

- 单个工具处理时间：2-3分钟
- 图片生成：1.5-2分钟（6张）
- 内容生成：10-20秒
- GitHub操作：20-30秒
- 5个工具总时间：约10-15分钟

## 故障排查

### 图片生成失败

检查：
- Z-Image API Key 是否有效
- 网络连接是否正常
- 单张失败不影响整体流程

### GitHub推送失败

检查：
- Token 权限是否正确
- 仓库名是否已存在
- 网络连接是否正常

### 仓库已存在

自动跳过创建步骤，直接推送更新

## 安全提示

⚠️ **重要：**
- 不要将 GitHub Token 提交到版本控制
- 使用配置文件时，将其添加到 `.gitignore`
- 定期轮换 Token
- 使用环境变量存储敏感信息

## 相关技能

- `wechat-zimage-generator` - 配图生成器
- `batch-ai-mirror-github-uploader` - 批量上传器

## 技术栈

- Bun - 运行环境
- Z-Image Turbo API - 图片生成
- GitHub API - 仓库管理
- Git - 版本控制

## License

MIT
