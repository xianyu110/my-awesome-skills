# 公众号文章改写去水印工具

一键将微信公众号文章改写并去除水印，生成全新原创内容。

## 快速开始

### 1. 安装 Node.js 依赖

```bash
cd .claude/skills/wechat-article-rewriter
npm install
```

### 2. 安装 Python 爬虫工具（可选，推荐）

如果需要使用强大的文章抓取功能：

```bash
# 克隆爬虫项目
git clone https://github.com/yeximm/Access_wechat_article.git python-crawler

# 进入目录并安装依赖
cd python-crawler
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

详细配置参考: [Access_wechat_article 文档](https://github.com/yeximm/Access_wechat_article)

### 3. 配置 API

复制配置文件并填入你的 API Key：

```bash
cp config.example.json config.json
```

编辑 `config.json`：

```json
{
  "fetchMethod": "python",  // "python" 或 "jina"
  "pythonCrawlerPath": "./python-crawler",  // Python 爬虫路径
  "jinaApiKey": "",  // 可选，Jina Reader API Key
  "aiProvider": "anthropic",  // 或 "openai"
  "apiKey": "your-api-key",  // Claude 或 OpenAI API Key
  "model": "claude-3-5-sonnet-20241022",
  "removeWatermarks": true,
  "watermarkKeywords": [...]  // 自定义水印关键词
}
```

### 3. 使用

```bash
# 基础用法
ts-node scripts/rewrite.ts --url "https://mp.weixin.qq.com/s/xxxxx"

# 深度改写
ts-node scripts/rewrite.ts --url "https://mp.weixin.qq.com/s/xxxxx" --mode deep

# 指定输出文件
ts-node scripts/rewrite.ts --url "https://mp.weixin.qq.com/s/xxxxx" --output "我的文章.md"
```

## API 说明

### 文章抓取方案

**方案一：Access_wechat_article（推荐）**

使用 Python 爬虫工具，功能最强大：
- GitHub: https://github.com/yeximm/Access_wechat_article
- 优势: 可获取文章完整信息（阅读量、点赞、评论等）
- 需要: 微信 PC 版 + Fiddler Classic
- 适合: 批量处理、需要详细数据

**方案二：Jina Reader API**

简单快速的在线抓取：
- 官网: https://jina.ai/reader
- 免费额度: 每月 1000 次请求
- 优势: 无需配置，开箱即用
- 适合: 快速单篇处理

### AI API

用于智能改写文章。

**Claude API (推荐)**
- 官网: https://console.anthropic.com/
- 模型: claude-3-5-sonnet-20241022
- 优势: 改写质量高，理解能力强

**OpenAI API**
- 官网: https://platform.openai.com/
- 模型: gpt-4-turbo 或 gpt-3.5-turbo
- 优势: 速度快，成本低

## 改写模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| light | 轻度润色，保持90%原文 | 仅需优化语句 |
| medium | 中度改写，调整表达方式 | 日常改写（默认） |
| deep | 深度改写，重组内容结构 | 需要高原创度 |
| style | 风格转换，改变写作风格 | 转换文章风格 |

## 工作原理

### 方案一：Python 爬虫（推荐）

```
公众号链接
    ↓
Python 爬虫抓取（通过微信 PC + Fiddler）
    ↓
获取完整文章内容 + 元数据
    ↓
清理水印和推广信息
    ↓
提取核心内容
    ↓
AI 智能改写
    ↓
输出 Markdown
```

### 方案二：Jina Reader

```
公众号链接
    ↓
Jina Reader API 抓取
    ↓
清理水印和推广信息
    ↓
提取核心内容
    ↓
AI 智能改写
    ↓
输出 Markdown
```

## 注意事项

⚠️ **重要提醒**

1. 本工具仅供学习和参考使用
2. 请尊重原创作者的版权
3. 改写后的内容建议人工审核
4. 不要用于商业用途或侵权行为
5. 建议在改写后注明参考来源

## 常见问题

**Q: 为什么抓取失败？**

A: 微信公众号有反爬虫机制，建议使用 Jina Reader API。如果还是失败，可以手动复制文章内容到文件，然后直接改写。

**Q: 改写质量不满意？**

A: 可以尝试：
- 切换改写模式（deep 模式质量更高）
- 使用 Claude API（比 GPT 更擅长中文改写）
- 在 prompt 中添加更具体的要求

**Q: 如何降低成本？**

A: 
- 使用 GPT-3.5-turbo（成本低）
- 先用 light 模式测试
- Jina Reader 免费额度足够日常使用

## 扩展功能

可以基于此工具扩展：

- 批量改写多篇文章
- 自动提取文章配图
- 生成文章摘要
- 转换为其他格式（HTML、PDF）
- 集成到自动化工作流

## 技术栈

- TypeScript / Node.js
- Jina Reader API - 文章抓取
- Claude API / OpenAI API - AI 改写
- 正则表达式 - 水印清理

## License

MIT
