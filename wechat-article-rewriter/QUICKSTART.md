# 快速开始

一键改写公众号文章，3 分钟上手！

## 方案选择

### 🚀 方案一：快速体验（Jina Reader）

适合：快速测试、单篇文章处理

优势：无需配置，开箱即用

```bash
# 1. 安装依赖
cd .claude/skills/wechat-article-rewriter
npm install

# 2. 配置 API
cp config.example.json config.json
# 编辑 config.json，填入 Claude API Key

# 3. 使用
ts-node scripts/rewrite.ts --url "https://mp.weixin.qq.com/s/xxxxx"
```

### 💪 方案二：专业版（Python 爬虫）

适合：批量处理、需要完整数据

优势：功能强大、数据完整、无限制

```bash
# 1. 一键安装 Python 爬虫
bash scripts/setup-python-crawler.sh

# 2. 配置微信 + Fiddler（详见 PYTHON-CRAWLER-SETUP.md）

# 3. 配置 API
cp config.example.json config.json
# 编辑 config.json:
# - fetchMethod: "python"
# - pythonCrawlerPath: "./python-crawler"
# - 填入 Claude API Key

# 4. 使用
ts-node scripts/rewrite.ts --url "https://mp.weixin.qq.com/s/xxxxx"
```

## 配置说明

### config.json 示例

```json
{
  "fetchMethod": "jina",  // 或 "python"
  "pythonCrawlerPath": "./python-crawler",
  "jinaApiKey": "",  // 可选
  "aiProvider": "anthropic",
  "apiKey": "sk-ant-xxx",  // 你的 Claude API Key
  "model": "claude-3-5-sonnet-20241022",
  "removeWatermarks": true,
  "watermarkKeywords": [
    "扫码关注",
    "长按二维码",
    "点击阅读原文"
  ]
}
```

## 使用示例

### 基础改写

```bash
ts-node scripts/rewrite.ts --url "https://mp.weixin.qq.com/s/xxxxx"
```

### 深度改写

```bash
ts-node scripts/rewrite.ts \
  --url "https://mp.weixin.qq.com/s/xxxxx" \
  --mode deep
```

### 指定输出文件

```bash
ts-node scripts/rewrite.ts \
  --url "https://mp.weixin.qq.com/s/xxxxx" \
  --output "我的文章.md"
```

### 风格转换

```bash
ts-node scripts/rewrite.ts \
  --url "https://mp.weixin.qq.com/s/xxxxx" \
  --mode style
```

## 改写模式对比

| 模式 | 原创度 | 速度 | 适用场景 |
|------|--------|------|----------|
| light | 30% | 快 | 仅需润色 |
| medium | 60% | 中 | 日常改写（默认） |
| deep | 90% | 慢 | 需要高原创度 |
| style | 80% | 中 | 转换写作风格 |

## 获取 API Key

### Claude API

1. 访问: https://console.anthropic.com/
2. 注册/登录账号
3. 进入 API Keys 页面
4. 创建新的 API Key
5. 复制 Key（格式：sk-ant-xxx）

### Jina Reader API（可选）

1. 访问: https://jina.ai/reader
2. 注册账号
3. 获取 API Key
4. 免费额度：1000 次/月

## 常见问题

**Q: 抓取失败怎么办？**

A: 
- 方案一：切换到 Python 爬虫方案
- 方案二：检查微信 + Fiddler 配置

**Q: 改写质量不满意？**

A: 
- 使用 `--mode deep` 深度改写
- 使用 Claude API（比 GPT 更擅长中文）

**Q: 如何降低成本？**

A: 
- 使用 GPT-3.5-turbo（成本低）
- 先用 light 模式测试

**Q: 可以批量处理吗？**

A: 可以，使用 Python 爬虫方案，参考 `PYTHON-CRAWLER-SETUP.md`

## 下一步

- 查看完整文档: `README.md`
- Python 爬虫配置: `PYTHON-CRAWLER-SETUP.md`
- 技术细节: `SKILL.md`

## 注意事项

⚠️ 本工具仅供学习研究使用，请遵守以下原则：

1. 尊重原创作者的版权
2. 改写后的内容建议人工审核
3. 不要用于商业用途或侵权行为
4. 建议在改写后注明参考来源
5. 不要频繁抓取，避免被限制
