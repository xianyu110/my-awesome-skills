# example-input

## 场景

用户已经写好一篇公众号文章，目录如下：

```text
/Users/chinamanor/articles/2026-03-08/openclaw-wechat/
├── article.md
├── meta.json
└── images/
    ├── arch.png
    ├── cover.png
    └── flow.png
```

## article.md 示例

```markdown
---
title: OpenClaw是如何全自动帮我排版并发布到公众号的
author: 石臻
---

# OpenClaw是如何全自动帮我排版并发布到公众号的

写完文章，还要手动排版、传图、调样式——这步每次都要花半小时以上。

## 整体架构：两层分工

![整体架构](./images/arch.png)

article-writer 负责内容生产。
wechat-article-publisher 负责发布。
```

## 调用示例

### 文章模式

```bash
bash /Users/chinamanor/clawd/skills/wechat-draft-pipeline/scripts/publish-from-dir.sh \
  --article-dir /Users/chinamanor/articles/2026-03-08/openclaw-wechat \
  --mode article \
  --submit
```

### 图文模式

```bash
bash /Users/chinamanor/clawd/skills/wechat-draft-pipeline/scripts/publish-from-dir.sh \
  --article-dir /Users/chinamanor/articles/2026-03-08/openclaw-wechat \
  --mode image-text \
  --submit
```
