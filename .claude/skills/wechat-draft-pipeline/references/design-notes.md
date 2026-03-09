# design-notes

这份说明把文章《OpenClaw是如何全自动帮我排版并发布到公众号的》里的关键思路，映射成 Skill 设计。

## 原文章里的核心能力拆解

### 1. 两层架构

原文强调两层：

- `article-writer`：信息采集、写作、配图、产出 Markdown 与素材
- `wechat-article-publisher`：读取产物并发布到公众号草稿箱

### 对 Skill 的启发

Skill 不应该负责写文章，也不应该把写作与发布绑死。
因此这里把 Skill 定位为：

> **“发布层统一入口”**

输入是文章目录或 Markdown；输出是公众号草稿。

---

### 2. 文章目录作为标准输入

原文里的整个发布流程，都围绕“文章目录”展开：

- Markdown 正文
- 图片素材
- meta.json
- 封面图

### 对 Skill 的启发

Skill 最稳的输入不是一堆散参数，而是一个目录。
因此当前 Skill 采用：

```text
article-dir/
├── article.md
├── meta.json
├── images/
└── assets/
```

这样后续要扩展缓存、草稿更新、标签渲染，都有地方落状态。

---

### 3. 图文与文章必须分流

原文明确提到：

- 长文“文章”与“图文笔记”不是同一个内容类型
- 微信接口与编辑器行为不同
- 如果混用，会导致格式错乱

### 对 Skill 的启发

Skill 层必须强制区分：

- `article`
- `image-text`

默认 `article`，但允许显式指定。

---

### 4. 图片处理是发布链路的核心

原文中最费时的不是写作，而是：

- 上传图片
- 替换链接
- 处理微信自己的素材地址

### 对 Skill 的启发

V1 先复用现有浏览器自动化脚本插图；
V2 再补 API 级图片上传缓存。

建议的 V2 状态结构：

```json
{
  "mode": "article",
  "draft_media_id": "...",
  "cover_media_id": "...",
  "wechat_image_map": {
    "images/001.png": "https://mmbiz.qpic.cn/..."
  },
  "updated_at": "2026-03-08T16:00:00+08:00"
}
```

---

### 5. 隐藏标签系统很值得保留

原文中的一个高价值设计是：

```html
<!-- wechat head -->
```

这类 HTML 注释在普通 Markdown 渲染器里不可见，但发布到微信前可以被渲染器识别成定制样式块。

### 对 Skill 的启发

这非常适合做成 V2 / V3：

- `<!-- wechat head -->` → 蓝色导读框
- `<!-- wechat tip -->` → 提示块
- `<!-- wechat summary -->` → 总结块
- `<!-- wechat follow -->` → 关注引导区

建议单独拆成：

- `renderers/wechat-markdown-renderer.ts`
- `themes/default.css`
- `tag-presets.json`

---

### 6. 草稿更新能力很重要

原文里提到：

- 首次发布：创建草稿
- 后续更新：基于 `media_id` 更新草稿
- 不重复产生草稿

### 对 Skill 的启发

这比“能发一次”更有价值。
建议 V2 实现：

1. 首次创建草稿
2. 将 `media_id` 写回 `meta.json`
3. 二次运行时自动走更新接口
4. 提供 `--force-new` 参数强制新建

---

## 当前 Skill 的定位

当前 `wechat-draft-pipeline` 是：

- **V1 可用 Skill**
- **统一入口**
- **先包装已有能力**
- **为后续产品级版本留接口**

## 建议的 V2 开发路线

### Phase 1：状态文件
- 读取 / 写入 `meta.json`
- 保存 mode、draft_media_id、image_map

### Phase 2：Markdown 渲染增强
- 增加隐藏标签解析
- 自动 header/footer
- 样式主题配置

### Phase 3：API 化
- 微信图片上传接口
- 草稿创建接口
- 草稿更新接口
- 封面素材接口

### Phase 4：OpenClaw 深度集成
- 允许用户一句话触发：
  - “把昨天那篇文章发到公众号草稿箱”
- 自动从文章目录、封面图、meta.json 中完成所有参数推断

## 结论

这篇文章最值得保留的，不只是“自动发公众号”，而是它背后的三件事：

1. **目录化输入**
2. **文章 / 图文 分流**
3. **状态化发布（可更新）**

当前 Skill 已先把第 1、2 点落地为可执行入口；
第 3 点建议作为下一轮开发重点。
