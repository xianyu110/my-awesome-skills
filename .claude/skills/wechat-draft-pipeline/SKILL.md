---
name: wechat-draft-pipeline
description: 将本地 Markdown 文章目录发布到微信公众号草稿箱的工作流技能。支持文章（长文）与图文两种模式，统一目录约定，复用现有 WeChat 发布脚本。
---

# wechat-draft-pipeline

把“文章写完后再手动排版、传图、进后台发草稿”的流程，收敛成一个可复用 Skill。

## 功能

当前版本（V1）提供：

- 识别文章目录 / Markdown 文件
- 区分 **文章（长文）** 与 **图文（多图笔记）** 两种发布模式
- 统一调用现有发布脚本：
  - `../baoyu-post-to-wechat/scripts/wechat-article.ts`
  - `../baoyu-post-to-wechat/scripts/wechat-browser.ts`
- 支持从文章目录自动寻找 Markdown 与图片目录
- 支持“预览模式”与“保存草稿模式”

> 说明：
> 本 Skill 当前是 **可用的统一入口版**，先把已有能力封装起来。
> 文章里提到的 `meta.json` 图片缓存、草稿 `media_id` 更新、隐藏标签渲染、自动 header/footer 注入，属于 V2 增强项，见 `references/design-notes.md`。

## 适用场景

当用户说以下意思时启用：

- “把这篇文章发到微信公众号草稿箱”
- “按文章目录发布公众号草稿”
- “这个目录帮我走微信公众号发布流程”
- “把 Markdown + 图片做成公众号文章”
- “发成微信图文 / 图文笔记”

## 目录约定

推荐文章目录结构：

```text
article-dir/
├── article.md         # 主文章（推荐）
├── meta.json          # 可选，给后续 V2 扩展用
├── images/            # 推荐图片目录
│   ├── 001.png
│   └── 002.jpg
└── assets/            # 也可用 assets/ 或 img/
```

兼容的 Markdown 文件名优先级：

1. `article.md`
2. `index.md`
3. 当前目录下找到的第一个 `.md`

兼容的图片目录优先级：

1. `images/`
2. `assets/`
3. `img/`

## 使用方式

用户说：

- `用 wechat-draft-pipeline 发布这个文章目录：/path/to/article-dir`
- `用 wechat-draft-pipeline 把这篇 Markdown 发到公众号草稿箱`
- `用 wechat-draft-pipeline 以图文模式发布 /path/to/article-dir`

## 执行步骤

### Step 1: 识别输入

优先识别以下输入：

- 文章目录路径
- 单个 Markdown 文件路径
- 发布模式：`article` 或 `image-text`
- 是否要求直接保存草稿（`--submit`）

模式判断规则：

- 用户说“文章、长文、公众号正文、排版文章” → `article`
- 用户说“图文、笔记、多图、图片为主” → `image-text`
- 未说明时默认 `article`

### Step 2: 校验内容

如果用户给的是目录：

- 查找主 Markdown 文件
- 查找图片目录（图文模式必须有）

如果用户给的是 Markdown 文件：

- `article` 模式可直接发布
- `image-text` 模式仍需额外图片目录

### Step 3: 选择执行入口

统一用本 Skill 自带脚本：

```bash
bash scripts/publish-from-dir.sh --article-dir /path/to/article-dir --mode article --submit
```

或：

```bash
bash scripts/publish-from-dir.sh --article-dir /path/to/article-dir --mode image-text --submit
```

脚本内部会自动转调：

- `baoyu-post-to-wechat/scripts/wechat-article.ts`（文章）
- `baoyu-post-to-wechat/scripts/wechat-browser.ts`（图文）

### Step 4: 返回执行结果

返回时应明确说明：

- 识别出的模式
- 使用的 Markdown 文件
- 使用的图片目录（如有）
- 是否已保存为草稿
- 如失败，给出最小可执行修复建议

## 输出格式

```markdown
已处理完成：
- 模式：article
- Markdown：/path/to/article.md
- 图片目录：/path/to/images
- 执行动作：已保存到公众号草稿箱

下一步建议：
1. 去公众号后台检查排版
2. 确认封面、摘要、图片位置
3. 无误后再正式发布
```

## 边界条件

- **没有 Markdown 文件**：提示用户提供文章目录或 Markdown 路径
- **image-text 模式没有图片目录**：要求补充 `images/` / `assets/` / `img/`
- **未登录微信公众号后台**：提示先扫码登录 `mp.weixin.qq.com`
- **Chrome 未安装**：提示检查本机 Chrome，或设置 `WECHAT_BROWSER_CHROME_PATH`
- **bun / npx 不可用**：提示检查 Node / npx 环境
- **图文标题超过 20 字**：底层脚本会自动压缩；如果语义损失明显，再让用户人工确认
- **图文内容超过 1000 字**：底层脚本会自动压缩；必要时改为文章模式

## 当前限制（V1）

当前 Skill **还没有** 直接实现以下能力：

- `meta.json` 图片 CDN 缓存
- 已发布草稿的自动更新（`media_id` 复用）
- 隐藏标签渲染（如 `<!-- wechat head -->`）
- header / footer 自动注入
- 微信 API 直连发布链路

这些属于下一版增强，可按 `references/design-notes.md` 继续开发。

## 示例

### 输入

```text
用 wechat-draft-pipeline 发布这个目录：/Users/chinamanor/articles/2026-03-08/openclaw-wechat
```

### 输出

```markdown
已开始执行公众号草稿发布：
- 模式：article
- Markdown：/Users/chinamanor/articles/2026-03-08/openclaw-wechat/article.md
- 图片目录：/Users/chinamanor/articles/2026-03-08/openclaw-wechat/images
- 动作：保存为草稿
```

## 参考文件

- `README.md`
- `references/design-notes.md`
- `scripts/publish-from-dir.sh`
- `examples/example-input.md`
- `examples/example-output.md`
