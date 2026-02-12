# 使用示例

## 示例1：生成单个AI工具指南

### ChatGPT GPT-5.2

```bash
bun .claude/skills/ai-mirror-publisher/scripts/publish.ts \
  --tools "chatgpt-gpt5.2" \
  --github-user "glpfive25-cyber" \
  --github-token "ghp_xxx" \
  --main-url "https://geminiai.asia/list/#/home" \
  --nav-url "https://chatgpt-plus.top/"
```

**预期输出：**
- 1个GitHub仓库
- 6张专业配图
- 完整使用指南
- 耗时：约2-3分钟

---

## 示例2：生成3个主流AI工具指南

### ChatGPT + Claude + Gemini

```bash
bun .claude/skills/ai-mirror-publisher/scripts/publish.ts \
  --tools "chatgpt-gpt5.2,claude-opus-4.5,gemini-3-pro" \
  --github-user "glpfive25-cyber" \
  --github-token "ghp_xxx" \
  --main-url "https://geminiai.asia/list/#/home" \
  --secondary-url "https://claudeapp.asia/list/#/home" \
  --nav-url "https://chatgpt-plus.top/"
```

**预期输出：**
- 3个GitHub仓库
- 18张专业配图（每个工具6张）
- 3份完整使用指南
- 耗时：约8-10分钟

**生成的仓库：**
1. `chatgpt-gpt5.2-mirror`
2. `claude-opus-4.5-mirror`
3. `gemini-3-pro-mirror`

---

## 示例3：生成5个AI工具完整指南

### 全平台覆盖

```bash
bun .claude/skills/ai-mirror-publisher/scripts/publish.ts \
  --tools "chatgpt-gpt5.2,claude-opus-4.5,gemini-3-pro,grok-4.1,deepseek-v3.2" \
  --github-user "glpfive25-cyber" \
  --github-token "ghp_xxx" \
  --main-url "https://geminiai.asia/list/#/home" \
  --secondary-url "https://claudeapp.asia/list/#/home" \
  --nav-url "https://chatgpt-plus.top/" \
  --images 6 \
  --style notion
```

**预期输出：**
- 5个GitHub仓库
- 30张专业配图（每个工具6张）
- 5份完整使用指南
- 耗时：约12-15分钟

**生成的仓库：**
1. `chatgpt-gpt5.2-mirror` - OpenAI最新
2. `claude-opus-4.5-mirror` - Anthropic编码最强
3. `gemini-3-pro-mirror` - Google多模态
4. `grok-4.1-mirror` - xAI实时信息
5. `deepseek-v3.2-mirror` - 国产开源

---

## 示例4：使用配置文件（推荐）

### 创建配置文件

```bash
cat > my-ai-tools.json << 'EOF'
{
  "ai_tools": [
    "chatgpt-gpt5.2",
    "claude-opus-4.5",
    "gemini-3-pro",
    "grok-4.1",
    "deepseek-v3.2"
  ],
  "github_username": "glpfive25-cyber",
  "github_token": "ghp_YOUR_GITHUB_TOKEN_HERE",
  "mirror_urls": {
    "main": "https://geminiai.asia/list/#/home",
    "secondary": "https://claudeapp.asia/list/#/home",
    "nav": "https://chatgpt-plus.top/"
  },
  "image_count": 6,
  "image_style": "notion",
  "base_directory": "./ai-mirror-repos"
}
EOF
```

### 运行

```bash
bun .claude/skills/ai-mirror-publisher/scripts/publish.ts --config my-ai-tools.json
```

**优势：**
- ✅ 配置可复用
- ✅ 参数清晰
- ✅ 易于版本控制
- ✅ 支持注释

---

## 示例5：自定义配图风格

### Tech 科技风格

```bash
bun .claude/skills/ai-mirror-publisher/scripts/publish.ts \
  --tools "chatgpt-gpt5.2" \
  --github-user "glpfive25-cyber" \
  --github-token "ghp_xxx" \
  --main-url "https://geminiai.asia/list/#/home" \
  --nav-url "https://chatgpt-plus.top/" \
  --style tech
```

**特点：**
- 深蓝电光青色
- 科技感强
- 适合技术类文章

### Minimal 极简风格

```bash
--style minimal
```

**特点：**
- 纯黑纯白
- 简洁专业
- 适合数据对比

### Warm 温暖风格

```bash
--style warm
```

**特点：**
- 温暖橙金黄色
- 亲和友好
- 适合场景展示

---

## 示例6：指定输出目录

```bash
bun .claude/skills/ai-mirror-publisher/scripts/publish.ts \
  --tools "chatgpt-gpt5.2,claude-opus-4.5" \
  --github-user "glpfive25-cyber" \
  --github-token "ghp_xxx" \
  --main-url "https://geminiai.asia/list/#/home" \
  --nav-url "https://chatgpt-plus.top/" \
  --output "./my-custom-repos"
```

**输出结构：**
```
my-custom-repos/
├── chatgpt-gpt5.2-mirror/
│   ├── images/
│   │   ├── cover.jpg
│   │   ├── concept.jpg
│   │   ├── flow.jpg
│   │   ├── comparison.jpg
│   │   ├── scenario.jpg
│   │   └── faq.jpg
│   ├── README.md
│   └── index.html
└── claude-opus-4.5-mirror/
    ├── images/
    ├── README.md
    └── index.html
```

---

## 示例7：测试单个工具（快速验证）

```bash
# 只生成1个工具，快速测试
bun .claude/skills/ai-mirror-publisher/scripts/publish.ts \
  --tools "deepseek-v3.2" \
  --github-user "glpfive25-cyber" \
  --github-token "ghp_xxx" \
  --main-url "https://geminiai.asia/list/#/home" \
  --nav-url "https://chatgpt-plus.top/"
```

**用途：**
- 验证配置是否正确
- 测试 GitHub Token 权限
- 检查图片生成效果
- 预览内容质量

---

## 实际使用场景

### 场景1：AI工具评测博主

**需求：** 为多个AI工具创建对比评测内容

```bash
bun .claude/skills/ai-mirror-publisher/scripts/publish.ts \
  --tools "chatgpt-gpt5.2,claude-opus-4.5,gemini-3-pro,grok-4.1" \
  --github-user "ai-reviewer" \
  --github-token "ghp_xxx" \
  --main-url "https://geminiai.asia/list/#/home" \
  --nav-url "https://chatgpt-plus.top/"
```

**产出：**
- 4个专业评测仓库
- 24张对比配图
- 详细功能说明
- 可直接分享链接

### 场景2：技术文档维护者

**需求：** 为团队维护AI工具使用文档

```bash
bun .claude/skills/ai-mirror-publisher/scripts/publish.ts \
  --tools "claude-opus-4.5,deepseek-v3.2" \
  --github-user "tech-team" \
  --github-token "ghp_xxx" \
  --main-url "https://geminiai.asia/list/#/home" \
  --nav-url "https://chatgpt-plus.top/" \
  --style tech
```

**产出：**
- 技术风格文档
- 清晰的使用流程
- 团队可共享
- 易于更新维护

### 场景3：教育培训机构

**需求：** 为学员提供AI工具学习资料

```bash
bun .claude/skills/ai-mirror-publisher/scripts/publish.ts \
  --tools "chatgpt-gpt5.2,gemini-3-pro" \
  --github-user "edu-institute" \
  --github-token "ghp_xxx" \
  --main-url "https://geminiai.asia/list/#/home" \
  --nav-url "https://chatgpt-plus.top/" \
  --style warm
```

**产出：**
- 友好的学习资料
- 图文并茂
- 易于理解
- 学员可自学

---

## 输出示例

### 控制台输出

```
🚀 开始批量生成AI镜像站指南...
========================================

[1/3] 处理 chatgpt-gpt5.2...
  ✓ 创建目录: ./ai-mirror-repos/chatgpt-gpt5.2-mirror
  [图片] 开始生成配图...
  [图片] 生成中: cover.jpg
  [图片] ✓ 完成: cover.jpg
  [图片] 生成中: concept.jpg
  [图片] ✓ 完成: concept.jpg
  [图片] 生成中: flow.jpg
  [图片] ✓ 完成: flow.jpg
  [图片] 生成中: comparison.jpg
  [图片] ✓ 完成: comparison.jpg
  [图片] 生成中: scenario.jpg
  [图片] ✓ 完成: scenario.jpg
  [图片] 生成中: faq.jpg
  [图片] ✓ 完成: faq.jpg
  [图片] ✓ 完成！成功生成 6/6 张图片
  ✓ 生成内容: README.md
  ✓ 生成内容: index.html
  ✓ Git 初始化
  ✓ 创建GitHub仓库: chatgpt-gpt5.2-mirror
  ✓ 推送代码到GitHub
  📦 https://github.com/glpfive25-cyber/chatgpt-gpt5.2-mirror

[2/3] 处理 claude-opus-4.5...
  ...

[3/3] 处理 gemini-3-pro...
  ...

========================================
✅ 完成！共创建 3 个图文并茂的仓库

📦 仓库列表：
1. https://github.com/glpfive25-cyber/chatgpt-gpt5.2-mirror
2. https://github.com/glpfive25-cyber/claude-opus-4.5-mirror
3. https://github.com/glpfive25-cyber/gemini-3-pro-mirror

⏱️  总耗时：8分32秒
📊 成功率：100% (3/3)
📸 图片生成：100% (18/18)
========================================
```

### 生成的 README.md 预览

```markdown
# ChatGPT GPT-5.2官网镜像站使用指南（国内直连）

![封面图](images/cover.jpg)

## ✅ 精选入口

- **主入口**：https://geminiai.asia/list/#/home
- **备用入口**：https://claudeapp.asia/list/#/home
- **镜像导航**：https://chatgpt-plus.top/

## 📋 目录导航

- [什么是 ChatGPT GPT-5.2？](#什么是-chatgpt-gpt-52)
- [为什么选择镜像网站？](#为什么选择镜像网站)
- [精选镜像站推荐](#精选镜像站推荐)
- [核心优势与功能](#核心优势与功能)
- [快速开始使用](#快速开始使用)
- [常见问题FAQ](#常见问题faq)
- [隐私安全建议](#隐私安全建议)

## 什么是 ChatGPT GPT-5.2？

![概念图](images/concept.jpg)

ChatGPT GPT-5.2 是 OpenAI 于 2025年12月 发布的最新版本...

[详细内容...]
```

---

## 下一步

查看完整文档：
- [SKILL.md](./SKILL.md) - 完整技能说明
- [README.md](./README.md) - 使用指南
- [QUICKSTART.md](./QUICKSTART.md) - 快速开始

开始使用：
```bash
bun .claude/skills/ai-mirror-publisher/scripts/publish.ts --help
```
