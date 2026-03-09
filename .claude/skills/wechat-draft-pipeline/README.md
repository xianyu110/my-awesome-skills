# wechat-draft-pipeline

把微信公众号“文章发布”这件事做成一个统一入口 Skill。

## 这是什么

这个 Skill 来自一篇关于 **OpenClaw 自动排版并发布到公众号** 的工作流拆解。
当前先落地为 **V1 可用版**：

- 接受文章目录或 Markdown 路径
- 自动判断走 **文章** 还是 **图文** 模式
- 复用现有 `baoyu-post-to-wechat` 的浏览器自动化脚本
- 统一成一个 Skill 入口，避免每次手拼命令

## 当前能力（V1）

### 1) 文章模式（article）
适合：长文、公众号正文、Markdown 文章。

底层调用：
- `skills/baoyu-post-to-wechat/scripts/wechat-article.ts`

特点：
- 支持 Markdown 转公众号编辑器内容
- 支持正文图片插入
- 适合完整文章发布到公众号草稿箱

### 2) 图文模式（image-text）
适合：多图笔记、图片为主的帖子。

底层调用：
- `skills/baoyu-post-to-wechat/scripts/wechat-browser.ts`

特点：
- 自动导入图片
- 自动填标题与正文
- 适合图文型内容

## 推荐目录结构

```text
article-dir/
├── article.md
├── meta.json
├── images/
│   ├── 001.png
│   └── 002.jpg
└── assets/
```

说明：
- `article.md`：主文章
- `meta.json`：当前可选，预留给 V2 的缓存与草稿更新
- `images/`：推荐图片目录

## 用法

### 文章模式

```bash
bash /Users/chinamanor/clawd/skills/wechat-draft-pipeline/scripts/publish-from-dir.sh \
  --article-dir /path/to/article-dir \
  --mode article \
  --submit
```

### 图文模式

```bash
bash /Users/chinamanor/clawd/skills/wechat-draft-pipeline/scripts/publish-from-dir.sh \
  --article-dir /path/to/article-dir \
  --mode image-text \
  --submit
```

### 只预览，不保存草稿

```bash
bash /Users/chinamanor/clawd/skills/wechat-draft-pipeline/scripts/publish-from-dir.sh \
  --article-dir /path/to/article-dir \
  --mode article
```

## 参数

- `--article-dir <path>`：文章目录
- `--mode article|image-text`：发布模式，默认 `article`
- `--theme <name>`：文章模式主题，默认 `grace`
- `--submit`：实际保存到草稿箱；不带时只走编辑/预览流程
- `--profile <dir>`：指定 Chrome profile 目录

## 依赖

- Google Chrome
- `npx`
- `bun`（通过 `npx -y bun` 调起）
- 已安装的 `baoyu-post-to-wechat` Skill
- 首次运行需登录微信公众号后台

## 与原文章的关系

原文章里有几项很重要的设计思想，这个 Skill 已经吸收：

1. **两层分工**：写作与发布解耦
2. **目录驱动**：文章目录作为统一输入
3. **文章 / 图文 分流**：两种内容类型不同处理
4. **一键发布**：统一命令入口

## 暂未实现（建议 V2 做）

- `meta.json` 的图片上传缓存
- `media_id` 复用，自动更新草稿
- 隐藏标签系统（例如 `<!-- wechat head -->`）
- 自动 header/footer 注入
- 通过微信 API 直发草稿，而不只走浏览器自动化

## 下一步建议

如果你要把文章里的方案做成真正完整的产品级 Skill，建议按这个顺序继续：

1. 先保留当前 V1 入口，跑通日常使用
2. 再加 `meta.json` 状态管理
3. 再做隐藏标签渲染器
4. 最后补 API 级草稿创建 / 更新

## 相关文件

- `SKILL.md`：Skill 指令
- `scripts/publish-from-dir.sh`：统一入口脚本
- `references/design-notes.md`：设计拆解与 V2 路线
- `examples/`：输入输出示例
