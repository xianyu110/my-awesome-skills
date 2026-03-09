# Nano Banana Image Generation - 快速开始

使用 Chat Completions 格式生成图片的 OpenClaw Skill。

## 🚀 快速开始（3步）

### 第1步：测试生成

```bash
cd skills/bananapro-image-gen

# 生成一张图片
python scripts/generate_image.py \
  --prompt "画一只可爱的橙色猫咪" \
  --filename "cat.png"
```

### 第2步：查看结果

```bash
# macOS
open cat.png

# Linux
xdg-open cat.png
```

### 第3步：生成白板图

```bash
python scripts/generate_image.py \
  --prompt "生成一张白板图片，手写字体风格，内容是OpenClaw核心概念" \
  --filename "whiteboard.png"
```

## 📋 常用命令

### 基础生成

```bash
python scripts/generate_image.py -p "画只猫" -f "cat.png"
```

### 指定分辨率

```bash
python scripts/generate_image.py -p "画只猫" -f "cat.png" -r 2K
```

### 指定模型

```bash
python scripts/generate_image.py -p "画只猫" -m "gpt-4o-image" -f "cat.png"
```

## 🎨 实用示例

### 1. 社交媒体配图

```bash
python scripts/generate_image.py \
  -p "科技感的社交媒体封面，AI助手主题，蓝色渐变" \
  -f "social_cover.png" \
  -r 2K
```

### 2. Logo 设计

```bash
python scripts/generate_image.py \
  -p "极简AI机器人Logo，蓝白配色，线条简洁" \
  -f "logo.png"
```

### 3. 概念白板图

```bash
python scripts/generate_image.py \
  -p "白板图，手写字体，OpenClaw vs ChatGPT对比表格" \
  -f "comparison.png"
```

### 4. 流程图

```bash
python scripts/generate_image.py \
  -p "流程图，手绘风格，展示OpenClaw工作流程，包含5个步骤" \
  -f "workflow.png"
```

## ⚙️ 配置说明

### 默认配置（无需设置）

脚本已内置 API 配置，可直接使用。

### 自定义配置（可选）

```bash
# 设置环境变量
export KEY=xxx

# 或使用命令行参数
python scripts/generate_image.py -p "画只猫" -k "your-api-key"
```

## 📊 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `-p` | 图片描述（必需） | "画只猫" |
| `-f` | 输出文件名 | "cat.png" |
| `-m` | 模型名称 | "gpt-4o-image" |
| `-r` | 分辨率 | "1K", "2K", "4K" |
| `-k` | API Key | "sk-xxx" |

## 🐛 常见问题

### 问题1：生成失败

**解决方案**：
- 检查网络连接
- 确认 API Key 有效
- 简化提示词重试

### 问题2：图片质量不理想

**解决方案**：
- 使用更详细的提示词
- 指定风格和细节
- 尝试不同的模型

### 问题3：生成速度慢

**说明**：
- 正常情况 10-30 秒
- 复杂图片可能需要 1-2 分钟
- 请耐心等待

## 📚 更多信息

- 完整文档：[SKILL.md](SKILL.md)
- 提示词技巧：查看 SKILL.md 中的"提示词技巧"章节
- 实战案例：查看 SKILL.md 中的"实战案例"章节

## 💡 提示词技巧

### 白板图模板

```
生成一张白板图片，手写字体风格，内容包含：
- 标题：[主题]
- 要点1：[内容]
- 要点2：[内容]
使用箭头和框图
```

### 对比表格模板

```
生成对比表格图片，清晰易读：
- 标题：[A vs B]
- 对比维度：[维度1、维度2]
- 对比结果
```

## 🎯 下一步

1. ✅ 阅读完整文档：[SKILL.md](SKILL.md)
2. ✅ 尝试不同的提示词
3. ✅ 生成自己的图片
4. ✅ 集成到 OpenClaw 工作流

## 📞 需要帮助？

- GitHub Issues: [提交问题](https://github.com/xianyu110/awesome-openclaw-tutorial/issues)
- 完整教程：[OpenClaw 超级个体实战指南](https://github.com/xianyu110/awesome-openclaw-tutorial)
