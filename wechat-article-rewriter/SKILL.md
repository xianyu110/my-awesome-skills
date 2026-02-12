# 公众号文章改写去水印工具

一键抓取微信公众号文章，智能改写并去除水印，生成全新原创内容。

## 功能特性

- 🔗 **一键抓取** - 输入公众号文章链接，自动获取完整内容
- ✍️ **智能改写** - 保持核心观点，重新组织语言和结构
- 🧹 **去除水印** - 自动清理文章中的推广信息、二维码引导等
- 📝 **保留格式** - 保持标题层级、列表、引用等格式
- 🎯 **多种模式** - 轻度润色、深度改写、风格转换

## 使用方法

### 基础用法

```bash
# 改写公众号文章
ts-node scripts/rewrite.ts --url "https://mp.weixin.qq.com/s/xxxxx"

# 指定改写强度
ts-node scripts/rewrite.ts --url "https://mp.weixin.qq.com/s/xxxxx" --mode deep

# 输出到指定文件
ts-node scripts/rewrite.ts --url "https://mp.weixin.qq.com/s/xxxxx" --output "改写后文章.md"
```

### 改写模式

- `light` - 轻度润色，保持90%原文结构
- `medium` - 中度改写，调整表达方式（默认）
- `deep` - 深度改写，重新组织内容结构
- `style` - 风格转换，改变写作风格

## 配置说明

在 `config.json` 中配置：

```json
{
  "jinaApiKey": "your-jina-api-key",
  "aiProvider": "anthropic",
  "apiKey": "your-api-key",
  "model": "claude-3-5-sonnet-20241022",
  "removeWatermarks": true,
  "watermarkKeywords": [
    "扫码关注",
    "长按二维码",
    "点击阅读原文",
    "推荐阅读",
    "往期精彩"
  ]
}
```

## 工作流程

1. 使用 Jina Reader API 抓取公众号文章内容
2. 清理水印和推广信息
3. 提取核心内容和结构
4. AI 智能改写
5. 格式化输出 Markdown

## 注意事项

- 仅用于学习和参考，请尊重原创
- 改写后的内容建议人工审核
- 不要用于商业用途或侵权行为
