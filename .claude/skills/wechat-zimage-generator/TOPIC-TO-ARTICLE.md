# 从选题到发布：一键生成完整文章

> 最强大的功能：输入一个主题，自动生成图文并茂的公众号文章！

## 🎯 功能特点

- ✅ **自动生成文章结构** - 根据风格生成合适的章节
- ✅ **智能配图** - 每个章节自动生成匹配的配图
- ✅ **多种风格** - 科技、商业、教育、生活四大风格
- ✅ **一键发布** - 自动生成发布脚本
- ✅ **完整工作流** - 从选题到发布全自动

## 🚀 快速开始

### 基础用法

```bash
bun .claude/skills/wechat-zimage-generator/scripts/topic-to-article.ts \
  --topic "你的主题"
```

就这么简单！它会：
1. 生成文章结构和内容框架
2. 为每个章节生成配图
3. 创建发布脚本
4. 组织好所有文件

### 完整参数

```bash
bun topic-to-article.ts \
  --topic "主题名称" \
  --style tech \
  --images 5 \
  --author "作者名" \
  --theme grace \
  --output ./my-article
```

## 📋 参数说明

| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `--topic` | 文章主题（必需） | - | "Claude Cowork" |
| `--style` | 文章风格 | tech | tech, business, education, lifestyle |
| `--images` | 配图数量 | 5 | 3-10 |
| `--author` | 作者名称 | AI创作助手 | "科技观察者" |
| `--theme` | 公众号主题 | grace | default, grace, simple |
| `--output` | 输出目录 | ./articles/主题名 | ./my-articles |
| `--keywords` | 关键词 | - | "AI,自动化,效率" |

## 🎨 四种文章风格

### 1. 科技风格 (tech)

**适合主题**：AI、编程、新技术、科技产品

**文章结构**：
- 技术背景 + 封面图
- 核心功能 + 功能展示图
- 实际应用 + 应用场景图
- 技术优势
- 未来发展 + 未来展望图

**配图风格**：科技感、蓝色调、未来感

**示例**：
```bash
bun topic-to-article.ts --topic "Claude Cowork" --style tech
bun topic-to-article.ts --topic "量子计算" --style tech
bun topic-to-article.ts --topic "Web3.0" --style tech
```

---

### 2. 商业风格 (business)

**适合主题**：商业模式、创业、投资、市场分析

**文章结构**：
- 市场概况 + 封面图
- 商业模式 + 商业流程图
- 成功案例 + 案例展示图
- 投资价值
- 发展趋势 + 趋势图表

**配图风格**：商务专业、蓝灰色调、高端大气

**示例**：
```bash
bun topic-to-article.ts --topic "AI创业机会" --style business
bun topic-to-article.ts --topic "SaaS商业模式" --style business
bun topic-to-article.ts --topic "元宇宙投资" --style business
```

---

### 3. 教育风格 (education)

**适合主题**：教程、学习指南、技能培训

**文章结构**：
- 基础概念 + 封面图
- 学习路径 + 路径图
- 实践案例 + 实践场景图
- 常见问题
- 进阶建议 + 进阶技巧图

**配图风格**：温馨明亮、清新、学习氛围

**示例**：
```bash
bun topic-to-article.ts --topic "Python编程入门" --style education
bun topic-to-article.ts --topic "英语学习方法" --style education
bun topic-to-article.ts --topic "摄影技巧" --style education
```

---

### 4. 生活风格 (lifestyle)

**适合主题**：生活方式、健康、美食、旅行

**文章结构**：
- 生活场景 + 封面图
- 实用技巧 + 技巧展示图
- 体验分享 + 体验场景图
- 注意事项
- 推荐建议 + 推荐内容图

**配图风格**：温暖治愈、柔和色调、生活气息

**示例**：
```bash
bun topic-to-article.ts --topic "咖啡文化" --style lifestyle
bun topic-to-article.ts --topic "极简生活" --style lifestyle
bun topic-to-article.ts --topic "健康饮食" --style lifestyle
```

## 📁 输出文件结构

```
articles/
└── 你的主题/
    ├── 你的主题.md          # 文章内容
    ├── images/              # 配图目录
    │   ├── section-1.jpg    # 第1章配图
    │   ├── section-2.jpg    # 第2章配图
    │   └── ...
    └── publish.sh           # 发布脚本
```

## 🔄 完整工作流

### 步骤1：生成文章

```bash
bun topic-to-article.ts --topic "Claude Cowork" --style tech
```

输出：
```
========================================
  📝 一键生成图文并茂的公众号文章
========================================
主题: Claude Cowork
风格: tech
配图: 5 张
输出: ./articles/Claude-Cowork
========================================

[article] 正在生成文章内容...
[article] ✓ 文章已生成

[images] 开始生成配图...
[image] Generating: section-1.jpg
[image] ✓ Saved: section-1.jpg
...

========================================
  ✅ 完成！
========================================
```

### 步骤2：编辑内容

打开生成的 markdown 文件，补充详细内容：

```bash
# macOS
open articles/Claude-Cowork/Claude-Cowork.md

# Linux
xdg-open articles/Claude-Cowork/Claude-Cowork.md
```

### 步骤3：发布到公众号

```bash
cd articles/Claude-Cowork
bash publish.sh
```

## 💡 使用技巧

### 技巧1：选择合适的风格

| 主题类型 | 推荐风格 |
|---------|---------|
| AI、编程、科技产品 | tech |
| 商业、创业、投资 | business |
| 教程、学习、培训 | education |
| 生活、健康、美食 | lifestyle |

### 技巧2：控制配图数量

- 短文（1000字以内）：3-4张
- 中文（1000-2000字）：5-6张
- 长文（2000字以上）：7-10张

### 技巧3：自定义输出目录

```bash
# 按日期组织
bun topic-to-article.ts --topic "主题" --output ./articles/2026-01

# 按分类组织
bun topic-to-article.ts --topic "主题" --output ./tech-articles
```

### 技巧4：批量生成

创建脚本 `batch-create.sh`:

```bash
#!/bin/bash

topics=(
  "Claude Cowork"
  "GPT-5 新特性"
  "AI编程助手对比"
)

for topic in "${topics[@]}"; do
  bun topic-to-article.ts --topic "$topic" --style tech
  sleep 10
done
```

## 🎯 实战案例

### 案例1：科技评测文章

```bash
bun topic-to-article.ts \
  --topic "Claude 3.5 vs GPT-4 深度对比" \
  --style tech \
  --images 6 \
  --author "AI评测室"
```

生成的文章包含：
- 技术背景介绍
- 核心功能对比
- 实际应用测试
- 性能优势分析
- 未来发展预测
- 6张精美配图

### 案例2：商业分析文章

```bash
bun topic-to-article.ts \
  --topic "2026年AI创业趋势" \
  --style business \
  --images 5 \
  --author "创业观察"
```

生成的文章包含：
- 市场概况分析
- 商业模式解析
- 成功案例分享
- 投资价值评估
- 发展趋势预测
- 5张商务配图

### 案例3：教程类文章

```bash
bun topic-to-article.ts \
  --topic "零基础学Python" \
  --style education \
  --images 7 \
  --author "编程导师"
```

生成的文章包含：
- 基础概念讲解
- 学习路径规划
- 实践案例演示
- 常见问题解答
- 进阶建议指导
- 7张教学配图

## ⚠️ 注意事项

### 1. 内容需要编辑

生成的文章是**框架和模板**，需要你：
- 补充详细内容
- 添加具体数据
- 调整语言风格
- 优化段落结构

### 2. 配图质量检查

生成后检查配图：
- 是否符合主题
- 清晰度是否足够
- 色调是否协调
- 如不满意可重新生成

### 3. 发布前预览

使用公众号编辑器预览：
- 检查排版
- 测试图片加载
- 调整格式细节

## 🚀 进阶用法

### 结合搜索引擎

```bash
# 1. 搜索资料
# 2. 生成文章框架
bun topic-to-article.ts --topic "主题"
# 3. 根据搜索结果补充内容
```

### 结合 AI 写作

```bash
# 1. 生成框架
bun topic-to-article.ts --topic "主题"
# 2. 用 ChatGPT/Claude 扩写每个章节
# 3. 整合到文章中
```

### 自动化发布

```bash
# 创建自动化脚本
#!/bin/bash
bun topic-to-article.ts --topic "$1" --style "$2"
cd "articles/$1"
# 自动编辑（可接入 AI API）
bash publish.sh
```

## 📊 效率对比

| 传统方式 | 使用本工具 | 提升 |
|---------|-----------|------|
| 选题构思: 30分钟 | 选题构思: 5分钟 | 6x |
| 文章撰写: 2小时 | 框架生成: 2分钟 | 60x |
| 配图制作: 1小时 | 自动生成: 3分钟 | 20x |
| 排版发布: 30分钟 | 一键发布: 1分钟 | 30x |
| **总计: 4小时** | **总计: 15分钟** | **16x** |

*注：实际时间包含内容编辑和优化*

## 🔗 相关资源

- [完整文档](./SKILL.md)
- [快速开始](./QUICKSTART.md)
- [提示词模板](./PROMPT-TEMPLATES.md)
- [README](./README.md)

---

**开始创作你的第一篇AI生成文章吧！🚀**
