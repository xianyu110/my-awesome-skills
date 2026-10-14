---
name: post-launch-backlinks
description: 新站或新产品上线后做外链推广时用：按顺序发 V2EX/社区、GitHub README、导航站目录、CSDN，并补 GSC/sitemap 与页脚徽章策略。
---
# 上线后发外链清单

适用：视频梗站、AI 工具站等新产品刚上线或换正式域名后。免费路径优先；付费加速须用户明确同意。联系邮箱用站点对外公开的运营邮箱（勿写入私密个人邮箱到公开仓库）。

## 0. 上线前备齐

- 正式域名可访问、HTTPS 正常；定价与免责声明（独立粉丝工具、不蹭版权方）写清
- 素材：logo、OG 图、一句话 tagline、长简介、示例图/视频链接
- 独立 GitHub 仓（如需）：README 写清产品、演示、入口链接；可开 Pages
- **页脚外链策略**：不要把首页外链随便送出去，也不要在全站 footer 铺满目录徽章。新站权重低时可在首页页脚留少量（优先必须反链的，如 Twelve Tools / Fazier，约 ≤3–5 个）；权重起来后把徽章挪到独立 **合作伙伴 /partners** 页，首页底部只留入口

## 1. 社区帖

1. **V2EX**「分享创造」：标题偏英文时可带正式域名；正文讲清做什么、价格、独立工具定位；先出草稿给用户确认，未明确要求不代发
2. **Linux.do**（常一起做、易漏）：资源/开发类分区；同样先草稿再发

## 2. GitHub README

- 推送/更新产品 README：功能、演示、定价入口、免责声明
- 有合适 awesome 列表再开 PR，不要硬塞；仓太新、无 star 时注意列表门槛
- **合集类站**（如 Skill 合集）在 CSDN 等文章平台：**只放 GitHub 仓链接，不放站址**；普通产品站文章一般放正式域名

## 3. 导航站 / 目录外链

### 3a. 免密免费优先（可批量）

典型一批：Twelve Tools、AICPB、Insidr.ai、The Next AI、Phygital+、AISO Tools、MarsX、Launching Next、aitools.inc、MeshKore、theweekly、Agentlaunch、SaaSHub 免费队列、NavTools Basic、AIFastSeek、Paperform 等。

规则：
- 遇密码、Google 登录、付费墙 → **跳过**，记入「需登录」清单
- 一律免费档，不勾 Fast-Track / Priority
- 表单若预填了别的产品文案，提交前必须全部改成当前站
- 已提交过的不要重复交；已 listed 但前台未出页的多半在审核

### 3b. 需登录（另开一轮）

Fazier、ToolPilot、PromoteProject、Product Hunt、TinyLaunch、Uneed、VibeCafé 等。在用户已登录的会话里做；仍只走免费档。

### 3c. 徽章回链

目录要求首页反链时：新站可短暂挂首页；之后统一收到 `/partners`，首页只留「合作伙伴」入口。

## 4. CSDN

- 原创公开；配图 + 站链（合集站例外只放 GitHub）
- 发完盯审核状态；驳回则改标题/正文后重发，不要同一篇反复硬刷
- 勿在公开 skill 里写具体博客账号名或密码

## 5. 索引与站内（四条之外常漏）

- Google Search Console：加域名资源 + 提交 sitemap
- 站内：`llms.txt`、博客 1～2 篇、sitemap 含 `/partners`
- 邮件/媒体外链（如有）：先出草稿卡，用户确认后再发

## 推荐顺序

备素材 → V2EX（+ Linux.do 草稿）→ GitHub README → 免密目录 → CSDN → 登录类目录 → GSC / sitemap →（可选）awesome PR / 邮件

## 每站交付物

给用户一份简表：渠道 | 状态（已交/跳过/失败）| 确认链接或原因。跳过须写明原因（要登录 / 要反链 / 要付费 / 找不到入口）。

## 公开仓库注意

- 不要写入 API Key、Webhook、Stripe/支付密钥、登录密码、Cookie、私密邮箱、个人手机号
- 联系方式用「站点运营邮箱」占位，由执行时从站点配置读取
