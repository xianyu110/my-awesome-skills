# geo-audit

GEO 体检与分批收录：让搜索引擎和 AI 爬虫读得懂网站，再分批提交索引，并按规则接入站长平台与规范目录。

## 何时使用

- 新站或改版后做一次 GEO / SEO 体检
- 需要补齐 robots.txt、sitemap、hreflang、结构化数据、llms.txt
- 要把首页 FAQ 第一条写成可引用的产品定义
- 准备向 Google、Bing、百度、头条、搜狗提交网站，但不要一次提交全部详情页
- 把真实的 MCP、NPM 包或开源项目提交到官方 MCP Registry、Smithery、远程 MCP awesome 列表、HelloGitHub、开源周刊（私有仓库、未发布的包不要交）

## 不要用它做

- 批量写专题或 Q&A 内容页 → 用 `geo`
- 发社区帖、导航站目录、页脚徽章 → 用 `post-launch-backlinks`

## 安装

与仓库其它 skills 相同，复制到 OpenClaw skills 目录：

```bash
cp -r .claude/skills/geo-audit ~/.openclaw/extensions/skills/
```
