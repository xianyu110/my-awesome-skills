---
name: wechat-zimage-generator
description: Generate images for WeChat articles using Z-Image API. Supports single/batch generation, style presets, and ONE-COMMAND article creation from topic to publish. SPECIALIZED for AI tools (ChatGPT/Claude/Gemini/Grok) mirror site guides. Use when user asks to "generate images for article", "create article with images", "write article about [topic]", "create AI mirror guide", or "create cover image".
---

# WeChat Z-Image Generator (公众号配图生成器)

使用智谱 AI 的 Z-Image Turbo API 为微信公众号文章生成高质量配图。支持单图生成、批量生成、风格预设，以及**从选题到发布的一键生成**。

**🎯 特别优化**：专门针对 ChatGPT、Claude、Gemini、Grok 等 AI 工具镜像站使用指南优化了提示词库和配图方案。

## 核心功能

- ✅ **快速生成**: Z-Image Turbo 模型，20-30秒生成一张图
- ✅ **风格预设**: 9种专业风格（notion/tech/warm/minimal等）
- ✅ **批量处理**: 一次命令生成多张图片
- ✅ **公众号优化**: 提示词针对文章配图优化
- ✅ **完整工作流**: 从生成配图到发布文章一条龙
- ✅ **AI工具专用**: 专门的 AI 镜像站配图提示词库

---

## 🚀 一键生成 AI 工具镜像站指南（推荐）⭐

**专门针对 ChatGPT、Claude、Gemini、Grok 等 AI 工具镜像站使用指南优化！**

### 快速生成完整文章

```bash
# ChatGPT 镜像站指南
bun .claude/skills/wechat-zimage-generator/scripts/topic-to-article.ts \
  --topic "ChatGPT镜像站使用指南" \
  --style notion \
  --images 6

# Claude 镜像站指南
bun .claude/skills/wechat-zimage-generator/scripts/topic-to-article.ts \
  --topic "Claude镜像站完整教程" \
  --style notion \
  --images 6

# Gemini 镜像站指南
bun .claude/skills/wechat-zimage-generator/scripts/topic-to-article.ts \
  --topic "Gemini镜像站访问指南" \
  --style notion \
  --images 6

# 多AI工具对比
bun .claude/skills/wechat-zimage-generator/scripts/topic-to-article.ts \
  --topic "ChatGPT vs Claude vs Gemini 镜像站对比" \
  --style minimal \
  --images 5
```

### 使用专用配图模板

我们提供了完整的 AI 工具镜像站配图提示词库（`AI-TOOLS-PROMPTS.md`），包含：

**11种配图类型**：
1. 封面图 - ChatGPT/Claude/Gemini/Grok 专用封面
2. 功能对比图 - 核心功能、性能、价格对比
3. 镜像站访问教程图 - 注册、登录、导航流程
4. 技术原理图 - 工作原理、网络路径、CDN加速
5. 安全隐私图 - 数据加密、隐私保护
6. 实用场景图 - 办公、学习、创作场景
7. 问题解决图 - FAQ、故障排除
8. 优势特点图 - 核心优势、速度稳定性
9. 推荐选择图 - 推荐列表、决策树
10. 提示词技巧图 - 基础结构、高级技巧
11. 未来展望图 - 发展趋势、技术演进

**5个完整配图方案**：
- 方案A：ChatGPT镜像站完整指南（7张）
- 方案B：多AI工具镜像站对比（6张）
- 方案C：Claude镜像站深度教程（6张）
- 方案D：Gemini镜像站多模态指南（6张）
- 方案E：镜像站技术原理深度解析（7张）

### 快速使用配图方案

```bash
# 使用预设的配图方案
cat > chatgpt-mirror.json << 'EOF'
{
  "outputDir": "./chatgpt-mirror-guide",
  "images": [
    {
      "prompt": "ChatGPT镜像站访问指南，notion风格，极简手绘线条，黑色线条白色背景，绿色点缀，对话框图标，火柴人使用笔记本电脑，网络连接符号，浅蓝云朵，清晰明了，16:9横版",
      "output": "cover.jpg"
    },
    {
      "prompt": "AI镜像站概念图，tech科技风格，深蓝电光青色，深灰背景，中心服务器图标，周围多个镜像节点，网络连接线，全球地图轮廓，科技感强，16:9横版",
      "output": "concept.jpg"
    },
    {
      "prompt": "镜像站注册登录流程，notion风格，极简手绘线条，黑色线条白色背景，浅蓝点缀，1-2-3-4步骤数字，箭头连接，邮箱图标密码图标，火柴人操作界面，流程清晰，16:9横版",
      "output": "registration.jpg"
    }
  ]
}
EOF

bun .claude/skills/wechat-zimage-generator/scripts/batch-simple.ts chatgpt-mirror.json
```

---

## 🎨 AI 工具专用提示词特点

### 设计原则
- **notion风格为主**: 极简手绘线条，清晰易懂，适合技术教程
- **tech风格辅助**: 科技感强，适合镜像站、网络访问等技术概念
- **minimal风格对比**: 数据对比、性能展示用极简图表
- **品牌色融合**: ChatGPT绿、Claude橙、Gemini蓝紫、Grok黑白红

### 提示词优化
- ✅ 技术概念可视化（服务器、节点、网络连接）
- ✅ 教程步骤清晰（1-2-3-4数字+箭头）
- ✅ 品牌识别度高（适度使用品牌色）
- ✅ 信息层次分明（对比表格、流程图）

查看完整提示词库：
```bash
cat .claude/skills/wechat-zimage-generator/AI-TOOLS-PROMPTS.md
```

---

## 🚀 通用文章生成（其他主题）

**支持的风格**:
- `tech` - 科技类（默认）
- `business` - 商业类
- `education` - 教育类
- `lifestyle` - 生活类
- `notion` - 通用知识分享

```bash
# 生成科技类文章
bun .claude/skills/wechat-zimage-generator/scripts/topic-to-article.ts \
  --topic "Claude Cowork" \
  --style tech

# 生成教育类文章  
bun .claude/skills/wechat-zimage-generator/scripts/topic-to-article.ts \
  --topic "Python编程入门" \
  --style education \
  --images 6

# 生成商业类文章
bun .claude/skills/wechat-zimage-generator/scripts/topic-to-article.ts \
  --topic "AI创业机会" \
  --style business \
  --author "商业观察"
```

**自动完成**:
1. ✅ 生成文章结构和内容框架
2. ✅ 根据章节自动生成配图
3. ✅ 创建发布脚本
4. ✅ 组织文件结构

---

## 快速开始

### 方式一：单图生成

```bash
# 生成封面图
bun .claude/skills/wechat-zimage-generator/scripts/generate-image.ts \
  --prompt "科技感的AI大脑，蓝色光芒" \
  --style cover \
  --output cover.jpg

# 生成文章插图
bun .claude/skills/wechat-zimage-generator/scripts/generate-image.ts \
  --prompt "温馨的办公场景，有电脑和咖啡" \
  --style illustration \
  --output article-1.jpg
```

### 方式二：批量生成（推荐）⭐

创建配置文件 `images.json`:

```json
{
  "outputDir": "./article-images",
  "images": [
    {
      "prompt": "科技感的AI大脑，蓝色调",
      "output": "cover.jpg",
      "style": "cover"
    },
    {
      "prompt": "程序员在写代码",
      "output": "coding.jpg",
      "style": "illustration"
    },
    {
      "prompt": "现代化的办公室",
      "output": "office.jpg",
      "style": "photo"
    }
  ]
}
```

然后运行：

```bash
# 使用简化版批量生成（推荐，更稳定）
bun .claude/skills/wechat-zimage-generator/scripts/batch-simple.ts images.json
```

**实测效果**: 5张图片约2-3分钟完成，成功率100%

## 风格预设

| 风格 | 描述 | 适用场景 | 提示词增强 |
|------|------|----------|-----------|
| `cover` | 16:9比例，专业设计感 | 文章封面图 | 自动添加"公众号封面图，高质量，专业设计，16:9比例" |
| `illustration` | 明亮清晰，插画风格 | 文章内配图 | 自动添加"文章配图，清晰明亮，插画风格" |
| `photo` | 高清摄影，真实场景 | 写实场景 | 自动添加"摄影作品，高清，专业摄影" |

**提示**: 使用风格预设可以显著提升图片质量和一致性

## Integration with WeChat Publisher

### Workflow 1: Generate then Publish

```bash
# 1. Generate images
bun .claude/skills/wechat-zimage-generator/scripts/batch-generate.ts images.json

# 2. Publish article with generated images
bun .claude/skills/baoyu-post-to-wechat/scripts/wechat-article.ts \
  --markdown article.md \
  --theme grace
```

### Workflow 2: Auto-generate from Article

Create a script that:
1. Parses article markdown
2. Extracts image descriptions from comments
3. Generates images
4. Updates markdown with image paths
5. Publishes to WeChat

## API Configuration

### Environment Variable

```bash
export ZIMAGE_API_KEY="your-modelscope-api-key"
```

### Default Key

Built-in key: `ms-YOUR_MODELSCOPE_KEY_HERE`

Get your own key at: https://modelscope.cn/

## Examples

### Example 1: Tech Article Cover

```bash
bun generate-image.ts \
  --prompt "未来科技，AI人工智能，蓝色科技感，专业设计" \
  --style cover \
  --output tech-cover.jpg
```

### Example 2: Tutorial Illustrations

```json
{
  "outputDir": "./tutorial-images",
  "images": [
    {
      "prompt": "第一步：打开电脑，简洁插画风格",
      "output": "step-1.jpg",
      "style": "illustration"
    },
    {
      "prompt": "第二步：编写代码，VS Code界面",
      "output": "step-2.jpg",
      "style": "illustration"
    },
    {
      "prompt": "第三步：运行程序，终端界面",
      "output": "step-3.jpg",
      "style": "illustration"
    }
  ]
}
```

### Example 3: Lifestyle Article

```bash
# Generate warm, cozy images
bun generate-image.ts \
  --prompt "温馨的咖啡馆，阳光透过窗户，暖色调" \
  --style photo \
  --output cafe.jpg
```

## Prompt Tips

### Good Prompts for AI Mirror Guides

**封面图**：
- ✅ "ChatGPT镜像站访问指南，notion风格，极简手绘线条，黑色线条白色背景，绿色点缀，对话框图标，火柴人使用笔记本电脑，网络连接符号，清晰明了，16:9横版"

**技术原理图**：
- ✅ "AI镜像站概念图，tech科技风格，深蓝电光青色，深灰背景，中心服务器图标，周围多个镜像节点，网络连接线，全球地图轮廓，科技感强，16:9横版"

**流程图**：
- ✅ "镜像站注册登录流程，notion风格，极简手绘线条，黑色线条白色背景，浅蓝点缀，1-2-3-4步骤数字，箭头连接，邮箱图标密码图标，火柴人操作界面，流程清晰，16:9横版"

**对比图**：
- ✅ "AI工具核心功能对比表，notion风格，极简手绘线条，黑色线条白色背景，表格布局三列四行，ChatGPT绿Claude橙Gemini蓝标识，对勾叉号图标，功能名称清晰，专业对比，16:9横版"

### General Good Prompts

- ✅ "科技感的AI大脑，蓝色调，专业设计，高质量"
- ✅ "温馨的办公场景，有笔记本电脑和咖啡，明亮"
- ✅ "现代简约风格的工作空间，白色背景"

### Avoid

- ❌ "图片" (too vague)
- ❌ "好看的" (subjective)
- ❌ Too long prompts (keep under 150 characters for best results)

## Troubleshooting

### Generation Timeout

- Default timeout: 5 minutes
- If timeout occurs, try again or simplify prompt

### API Key Issues

```bash
# Test your API key
export ZIMAGE_API_KEY="your-key"
bun generate-image.ts --prompt "test" --output test.jpg
```

### Image Quality

- Use style presets for better results
- Add quality keywords: "高质量", "专业", "清晰"
- Specify aspect ratio for covers: "16:9比例"

## Advanced Usage

### Custom Model

```bash
bun generate-image.ts \
  --prompt "your prompt" \
  --model "Tongyi-MAI/Z-Image-Turbo" \
  --output custom.jpg
```

### Programmatic Usage

```typescript
import { generateImage } from './generate-image.ts';

const imagePath = await generateImage({
  prompt: '科技感的AI',
  style: 'cover',
  output: 'my-cover.jpg'
});

console.log(`Generated: ${imagePath}`);
```

## Pricing

Z-Image Turbo on ModelScope:
- Free tier available
- Check ModelScope pricing for details

## Related Skills and Resources

### Skills
- `baoyu-post-to-wechat` - Publish articles to WeChat
- `baoyu-cover-image` - Alternative cover generation
- `baoyu-article-illustrator` - Article illustration generation

### Documentation
- [AI Mirror Quickstart](./AI-MIRROR-QUICKSTART.md) - Quick guide for AI tool mirror site articles
- [AI Tools Prompts](./AI-TOOLS-PROMPTS.md) - Complete prompt library for AI tools
- [Style Guide](./STYLE-GUIDE.md) - 9 professional styles explained
- [Prompt Templates](./PROMPT-TEMPLATES.md) - General prompt templates
- [Topic to Article](./TOPIC-TO-ARTICLE.md) - One-command article generation guide

### Examples
- `examples/ai-mirror-guide.json` - AI mirror site guide (6 images)
- `examples/article-images.json` - General article images
- `examples/gemini-article-config.json` - Gemini article
- `examples/claude-vs-chatgpt-config.json` - AI comparison

---

## 🎯 Use Cases

### AI Tool Mirror Site Guides
Perfect for creating comprehensive guides for:
- ChatGPT mirror sites
- Claude mirror sites  
- Gemini mirror sites
- Grok mirror sites
- Multi-AI tool comparisons

**Features**:
- 11 specialized image types
- 5 complete image sets
- Brand color integration
- Technical concept visualization

### General Articles
Also works great for:
- Tech tutorials
- Business analysis
- Educational content
- Lifestyle articles

---

## 📈 Performance

Based on real testing:
- ✅ **Single image**: 20-30 seconds
- ✅ **5 images batch**: 2-3 minutes
- ✅ **Success rate**: ~100%
- ✅ **Image quality**: 1024x1024, high quality
- ✅ **Supported formats**: JPG, PNG

---

## 🚀 Quick Commands

```bash
# AI mirror guide (one command)
bun scripts/topic-to-article.ts --topic "ChatGPT镜像站使用指南" --style notion --images 6

# Batch generate with preset
bun scripts/batch-simple.ts examples/ai-mirror-guide.json

# Single image
bun scripts/generate-image.ts --prompt "your prompt" --output image.jpg

# View AI tools prompts
cat AI-TOOLS-PROMPTS.md

# View examples
ls examples/
```
