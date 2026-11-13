---
name: geo-audit
description: >-
  在网站要让搜索引擎和 AI 爬虫读得懂、做 GEO/SEO 体检、分批提交收录，
  或接入 Google/Bing/百度/头条/搜狗站长平台，以及 MCP/NPM/awesome/开源周刊等规范目录时使用。
  不用于写专题内容页（用 geo），也不用于导航站/社区外链（用 post-launch-backlinks）。
---

# GEO 体检与分批收录

新站或改版后，先让搜索引擎和 AI 爬虫读得懂，再分批提交收录，最后按规则把真实产物交到站长平台和规范目录。本技能管「机器是否读得懂、怎么提交、提交多少」。

和仓库里其它技能的分工：

- `geo`：挖真实问法、写枢纽/Q&A、用收录和收入做归因
- `post-launch-backlinks`：社区帖、导航站目录、页脚徽章
- 本技能：robots / sitemap / hreflang / 结构化数据 / llms.txt、首页定义型 FAQ、分批索引、站长平台、MCP/NPM/awesome/周刊

不要一次提交全部详情页。不要虚构尚不存在的 MCP、NPM 包或公开 API。

## 0. 先体检，再改，再提交

先输出一份差距清单，再动手。不要一上来就往站长平台甩全站 URL。

对每个检查项写清：现状、差距、建议。

- 无 JS 抓取能否读到正文：用 HTTP 请求看原始 HTML，不要只看浏览器水合后的页面
- `robots.txt` 是否明确允许主流搜索和 AI 爬虫；线上返回的是否就是你要发布的那一份（CDN 或静态资源可能绕过应用）
- sitemap 是否精而准，有没有把不该先收的详情页全塞进去
- 多语言页面是否用 hreflang 互相关联，`x-default` 是否合理
- 结构化数据是否与页面可见文案一致
- 是否提供给 AI 读的 `llms.txt`（可选 `llms-full.txt`）
- 首页 FAQ 第一条是否是「{产品名} 是什么」的可引用定义
- 计划提交的 URL 范围是否过大

## 1. 让爬虫和模型读得懂

### robots.txt

按爬虫分别写清楚 `Allow`，避免只靠一条 `User-agent: *`，又把关键路径 `Disallow` 掉。执行时对照各家官方文档核对名称（会变）。常见需要明确放行的包括：

- 搜索：Googlebot、Bingbot、Baiduspider、Sogou、360Spider、YandexBot、DuckDuckBot、Bytespider
- OpenAI：GPTBot、ChatGPT-User、OAI-SearchBot
- Anthropic：ClaudeBot、Claude-User、Claude-SearchBot、Anthropic-AI
- Google AI：Google-Extended、Google-CloudVertexBot
- 其它常见 AI/答案引擎：Applebot、Applebot-Extended、PerplexityBot、meta-externalagent、FacebookBot、Amazonbot、CCBot、YouBot

写完必须核对线上：`curl -sS https://{host}/robots.txt` 返回的就是预期内容。若静态资源优先于应用路由，把 `/robots.txt` 交回应用处理，或直接改那份会被发出去的静态文件。

### sitemap

只放当前阶段希望被收录的 URL。新站第一批只要：首页、分类或枢纽页、至多几百个优质话题页。不要一次性放入全部详情页。多语言站点为每种语言列出对应 URL，并与 hreflang 一致。

### hreflang

每个语言版都列出全部语言互链，并设 `x-default`（通常指向默认语言首页）。互链 URL 必须真实可访问；路径换成了中文或其它语言时，正文也必须是对应语言，不要只换 URL 不换文案。

### 结构化数据

按产品类型选用 `WebSite`、`WebApplication` 或 `SoftwareApplication`、`FAQPage`、`Organization` 等。标记内容必须和页面上能看见的文案一致，不要写页面没有的价格、评分或功能。

在 React 或其它 SSR/水合站点上，不要只往 HTML 里插入 FAQ 节点或改 JSON-LD，却不改前端源码：这会造成服务端 HTML 与客户端渲染不一致，页面在浏览器里直接报错。要改首页 FAQ，必须同时改服务端渲染和客户端文案，两边保持一致。

### llms.txt

按 [llmstxt.org](https://llmstxt.org/) 提供一份给模型读的说明：产品一句话定义、核心能力和边界、关键页面链接。需要更长说明时再加 `llms-full.txt`。多语言站点可提供 `/{locale}/llms.txt`。发布后同样用 HTTP 请求确认线上内容。

### 首页 FAQ 第一条

第一条必须是「{产品名} 是什么？」，并给出可直接引用的定义：一两段话说清做什么、不做什么、面向谁。后面再跟价格、用法、版权等常见问题。这是给 AI 引用的锚点，不要写成广告口号，也不要套用其它产品的定义。

## 2. 分批提交，不要一次倒进全站

新站一次性提交几十万个页面，很容易被判定为低质量。第一批只提交：

1. 首页
2. 分类页或枢纽页
3. 几百个优质话题页

等这批被收录、有了基本排名，再分批放出详情页。sitemap 也按这个节奏扩展，不要先生成一份含全部详情的巨型地图再指望搜索引擎自己挑选。

向站长平台提交时，交的就是这份精简 sitemap（或与之对应的 URL 列表），而不是全站抓取。

## 3. 接入站长平台

不同 AI 的联网搜索依赖不同索引，所以在目标市场里把这些平台都接上：

- [Google Search Console](https://search.google.com/search-console)：通用搜索
- [Bing Webmaster Tools](https://www.bing.com/webmasters)：ChatGPT 等的联网检索常用 Bing 索引
- [百度搜索资源平台](https://ziyuan.baidu.com/)
- [头条站长平台](https://zhanzhang.toutiao.com/)：豆包更偏向头条和抖音的内容生态
- [搜狗站长平台](https://zhanzhang.sogou.com/)：部分国内助手更偏向公众号和搜狗

执行规则：

- 需要登录、验证网站所有权的步骤由用户自己完成（验证码、域名 TXT、验证文件、扫码等）。不要替用户绕过验证，也不要要用户把密码发到聊天里。
- 用户登录之后，其余操作在浏览器里代做：添加资源、提交精简 sitemap、查看抓取和索引报告。
- 只提交第一批范围，不要把全部详情页一次性送出。
- 做完给用户一份表：平台、资源、已提交的 sitemap 或 URL 范围、还需要用户确认的事项。

## 4. 规范目录与生态收录

在站点本身可读、第一批页面可访问之后，再考虑目录。只提交真实存在的产物。没有公开 MCP、没有已发布的 NPM 包，就不要编一个去交；应先做出真实可安装的包，或在报告里写明跳过原因。

按产品实际情况选用（没有对应产物就跳过）：

- 官方 MCP 注册中心或目录（只有真正可安装、可运行的 MCP 才交）
- [Smithery](https://smithery.ai/)（同上）
- NPM（只有已经发布的真实包）
- GitHub 上相关的 awesome 列表
- [HelloGitHub](https://hellogithub.com/)
- 阮一峰[《科技爱好者周刊》](https://github.com/ruanyf/weekly)等开源周刊（按其当期投稿要求）

执行规则：

- 先读该列表的 CONTRIBUTING 或提交说明。不满足门槛（例如要求 star、完整文档、不收未发布项目）就不要硬提。
- 自动提交时：fork 仓库 → 按格式只改需要的一行或一篇文档 → 开 PR，不要改无关文件。
- 合集类仓库的介绍优先放 GitHub 仓库链接；普通产品介绍放正式域名。
- 需要登录的投稿页：用户登录，其余代填；提交前让用户看草稿或明确确认再发出。
- 导航站、产品目录、社区帖交给 `post-launch-backlinks`，不要在这里重复做一遍。

## 交付

给用户一份报告，包含：

1. 体检结果：通过、缺失、已修复
2. 第一批将提交的 URL 范围和这样切分的理由
3. 各站长平台的状态
4. 目录或周刊：已交的 PR / 表单链接，或跳过原因

不要把密钥、Cookie、登录密码或私密邮箱写进公开仓库或本技能文件。
