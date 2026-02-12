# WeChat Z-Image Generator

> 为微信公众号文章生成高质量AI配图的完整解决方案

## 🎯 核心优势

- **快速**: 20-30秒生成一张图，批量生成5张图约2-3分钟
- **稳定**: 基于智谱AI ModelScope API，成功率接近100%
- **易用**: 一条命令完成批量生成，支持配置文件
- **集成**: 可直接与 `baoyu-post-to-wechat` 发布工具配合使用

## 📦 安装要求

```bash
# 需要 Bun 运行时
curl -fsSL https://bun.sh/install | bash

# 或使用 npm
npm install -g bun
```

## 🚀 快速开始

### 1. 单图生成

```bash
bun scripts/generate-image.ts \
  --prompt "科技感的AI大脑，蓝色调，未来感" \
  --style cover \
  --output my-cover.jpg
```

### 2. 批量生成（推荐）

创建 `my-images.json`:

```json
{
  "outputDir": "./output",
  "images": [
    {
      "prompt": "科技感的AI，蓝色调",
      "output": "cover.jpg"
    },
    {
      "prompt": "办公场景，温馨",
      "output": "scene-1.jpg"
    }
  ]
}
```

运行：

```bash
bun scripts/batch-simple.ts my-images.json
```

## 📖 完整示例

查看 `examples/` 目录：

- `article-images.json` - 通用文章配图
- `gemini-article-config.json` - Gemini论文文章配图
- `claude-vs-chatgpt-config.json` - AI对比文章配图

## 🎨 风格预设

| 风格 | 效果 | 使用场景 |
|------|------|----------|
| `cover` | 16:9专业封面 | 文章头图 |
| `illustration` | 明亮插画风格 | 文章内配图 |
| `photo` | 高清摄影风格 | 真实场景 |

## 🔧 API配置

### 使用默认Key（内置）

无需配置，直接使用。

### 使用自己的Key

```bash
export ZIMAGE_API_KEY="your-modelscope-api-key"
```

获取Key: https://modelscope.cn/

## 🔗 与公众号发布集成

### 完整工作流

```bash
# 1. 生成配图
bun scripts/batch-simple.ts article-images.json

# 2. 发布到公众号
bun ../baoyu-post-to-wechat/scripts/wechat-article.ts \
  --markdown article.md \
  --theme grace \
  --submit
```

## 💡 提示词技巧

### ✅ 好的提示词

- "科技感的AI大脑，蓝色调，电路纹理，专业设计"
- "温馨的办公场景，笔记本电脑，咖啡杯，明亮"
- "学生在图书馆学习，专注认真，温暖色调"

### ❌ 避免的提示词

- "好看的图片" (太模糊)
- "图" (信息不足)
- 超过100字的长提示词

### 🎯 提示词公式

```
[主题] + [风格/氛围] + [色调] + [细节元素]
```

示例:
- 主题: AI人工智能
- 风格: 科技感，未来感
- 色调: 蓝色调，深色背景
- 细节: 电路纹理，数据流光效

完整提示词: "AI人工智能，科技感未来感，蓝色调深色背景，电路纹理数据流光效"

## 📊 性能数据

| 指标 | 数值 |
|------|------|
| 单图生成时间 | 20-30秒 |
| 批量5张时间 | 2-3分钟 |
| 成功率 | ~100% |
| 图片分辨率 | 1024x1024 |
| 支持格式 | PNG, JPG |

## 🐛 故障排除

### 生成超时

- 默认超时5分钟
- 如遇超时，重试即可
- 简化提示词可能有帮助

### API Key错误

```bash
# 测试你的Key
export ZIMAGE_API_KEY="your-key"
bun scripts/generate-image.ts --prompt "test" --output test.jpg
```

### 图片质量不佳

- 使用风格预设 (`--style cover/illustration/photo`)
- 添加质量关键词: "高质量"、"专业"、"清晰"
- 指定比例: "16:9比例"（封面图）

## 📝 更新日志

### v1.0.0 (2026-01-17)

- ✅ 单图生成功能
- ✅ 批量生成功能
- ✅ 三种风格预设
- ✅ 完整示例和文档
- ✅ 与公众号发布工具集成

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🔗 相关项目

- [baoyu-post-to-wechat](../baoyu-post-to-wechat) - 公众号文章发布工具
- [baoyu-article-illustrator](../baoyu-article-illustrator) - 智能文章配图生成器
- [baoyu-cover-image](../baoyu-cover-image) - 封面图生成器
