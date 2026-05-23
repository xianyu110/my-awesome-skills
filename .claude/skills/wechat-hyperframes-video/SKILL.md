---
name: wechat-hyperframes-video
description: 把微信公众号文章、口播稿、逐字稿、本地图片素材制作成可发布视频，通常是竖屏 HyperFrames 字幕视频，并使用 MiniMax 已有音色生成旁白、烘录字幕、合成最终 MP4；也可配套生成爆款标题和横屏/竖屏封面。当用户说“把公众号链接做成视频”“用相同音色”“配字幕”“逐字稿做视频”“做成字幕视频”“做好封面”“爆款标题”“MiniMax 音色”“HyperFrames 视频”时使用。
---

# WeChat HyperFrames Video

用于把公众号文章、口播稿、逐字稿或本地图片素材做成可发布视频。默认目标是：完整保留用户素材，使用用户已有 MiniMax 音色，生成旁白，做字幕烘录，必要时配套爆款标题和横竖封面，并交付最终 MP4。

## 触发场景

当用户提出这些需求时使用：

- 把 `mp.weixin.qq.com` 文章做成视频
- 把一段中文口播稿整理成视频脚本
- 把用户给出的逐字稿直接做成字幕视频
- 本地图片要全部放进视频里，不能省略
- 使用 MiniMax 里已经做过的音色或同一个 voice id
- 需要字幕版视频、字幕烘录、最终 mp4 校验
- 需要 10 个爆款标题、横屏封面、竖屏封面或首帧图
- 点名 `HyperFrames`、`MiniMax`、`相同音色`、`配字幕`

## 输入

常见输入包括：

- 公众号文章 URL
- 口播稿或文章正文
- 本地图片路径
- 已有项目目录或希望新建的输出目录
- MiniMax 相关环境变量或已有 `.env`
- 用户指定的 voice id，或从上次项目的 `assets/narration.meta.json` 复用
- 是否需要标题和封面；如果用户后续说“做封面/爆款标题”，在同一项目目录继续交付

不要打印 `.env`、API key、group id、token 或任何密钥值。如果缺少密钥，只提示用户通过环境变量或 `.env` 提供。

## 工作流

### 1. 准备项目

如果用户给的是公众号链接，优先结合 `wechat-link-extractor` 提取标题、正文、图片和视频。不要只用原始 HTML 猜测正文图片。

新建或复用 HyperFrames 项目时，先确认：

- `DESIGN.md` 或现有视觉风格
- `index.html`
- `package.json`
- `assets/`
- `renders/`
- `script.txt`

如果项目不存在，用 `npx hyperframes init` 初始化；如果已存在，先读现有结构再改。

项目目录建议使用主题 slug，例如：

```text
codex-plugins-subtitle-video/
```

产物目录建议固定：

```text
assets/
renders/
scripts/
snapshots/
covers/
```

### 2. 整理口播脚本

把文章或用户口播整理成适合视频旁白的 `script.txt`：

- 保留核心观点和顺序
- 删除网页噪音、菜单、二维码提示等
- 中文口播要自然，短句优先
- 每段尽量对应一个画面或素材
- 如果用户强调“图片不要省略”，脚本和分镜都要覆盖全部图片
- 如果用户给的是“视频内容逐字稿”，默认尽量保留原意和顺序，只做轻微口播化断句；不要擅自删掉编号、star 数、插件名、关键卖点
- 对清单类内容，按条目生成章节：开场、每个条目、总结

### 3. 准备素材

把本地图片或公众号图片放入 `assets/`，文件名使用稳定编号，例如：

```text
assets/article-01.jpg
assets/article-02.jpg
assets/article-03.jpg
```

不要跳过用户给出的图片。图片无法读取时，要明确列出失败路径。

### 4. MiniMax TTS

优先复用项目里的 TTS 脚本，例如：

```bash
node scripts/minimax-tts.mjs
```

推荐产物：

```text
assets/narration.mp3
assets/narration.meta.json
```

`narration.meta.json` 应记录非敏感元数据，例如 voice id、模型名、音频时长。可以读 voice id，但不要输出任何密钥。

如果用户要求“相同音色”，优先从这些位置找：

- 当前项目 `assets/narration.meta.json`
- 之前项目的 `assets/narration.meta.json`
- 用户明确提供的 voice id
- MiniMax 控制台或本地配置中非密钥的 voice id

如果历史项目的 `narration.meta.json` 使用 `voice_id` 而不是 `voiceId`，也要识别。若旧脚本里有稳定默认值，例如 `DEFAULT_VOICE_ID`，可以复用该非敏感 voice id，但不要输出或复制密钥。

生成音频后立刻确认时长：

```bash
ffprobe -v error -show_entries format=duration,size -of json assets/narration.mp3
```

### 5. 制作 HyperFrames 画面

竖屏默认使用 `1080x1920`。画面节奏必须跟随旁白时长：先生成旁白，再用 `ffprobe` 确认音频时长，最后设置 composition duration 和每个章节的 `data-start` / `data-duration`。不要先按猜测时长渲染长视频。

推荐检查：

```bash
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 assets/narration.mp3
```

`index.html` 里应包含：

- 清晰的封面标题
- 每张图片或截图的独立呈现
- 和口播同步的段落重点
- 顶部或底部稳定信息栏
- 进度条或章节提示
- 清单类视频应使用章节卡片/矩阵卡片，避免整屏堆大段正文
- 正文卡片与字幕底部安全区要分离，避免字幕遮挡关键信息

如果没有用户指定视觉风格，先写一个短 `DESIGN.md`，明确画面基调、颜色、字体、动效和不要做什么。

### 6. 生成字幕

如果没有精确转录时间戳，可以先从 `script.txt` 按中文标点拆句，按旁白总时长估算生成 `subtitles.srt` 和 `subtitles.js`。

推荐 DOM 字幕路线，因为某些机器的 ffmpeg 可能没有 `subtitles` / `ass` 滤镜：

```html
<script src="subtitles.js"></script>
<div id="subtitle" class="burned-subtitle" data-layout-ignore></div>
```

在 GSAP timeline 中按字幕时间设置文本：

```js
(window.SUBTITLES || []).forEach(function (item) {
  tl.set("#subtitle", { textContent: item.text, opacity: 1 }, item.start);
  tl.set("#subtitle", { opacity: 0 }, item.end);
});
```

字幕样式建议：

- 放在底部安全区
- 使用白字、描边或阴影
- 单条不宜太长
- 避免挡住正文图片关键内容
- 生成 `subtitles.srt` 后同步生成 `subtitles.js`，让字幕可在 HyperFrames DOM 内烘录
- 把 `subtitles.js` 初始化为空数组也可以，但最终渲染前必须重新生成真实字幕

### 7. 快照检查

渲染前先用快照检查字幕和画面：

```bash
npx hyperframes snapshot --at 5,40,118 --timeout 30000 > subtitle-snapshot.log 2>&1
```

查看：

```text
snapshots/contact-sheet.jpg
snapshots/frame-*.png
```

确认字幕没有出界、没有盖住关键信息、图片没有空白或丢失。

如果 `npx hyperframes validate` 或 `inspect` 卡住，不要无限等待。改跑更小的校验：

```bash
npx hyperframes validate > validate.log 2>&1
tail -c 4000 validate.log
```

若只有淡入动画瞬间引发的 WCAG 对比度提示，可以记录为非阻塞；若有布局、空元素、JS 报错或素材缺失，先修正再渲染。

### 8. 渲染视频

长视频渲染不要把输出 pipe 到 `head`，否则可能中断渲染。把日志重定向到文件：

```bash
npx hyperframes render -o renders/video-only.mp4 --fps 30 --quality standard --workers 1 > render.log 2>&1
```

如果渲染失败，先看日志尾部：

```bash
tail -c 4000 render.log
```

渲染中如果终端没有持续输出，另开只读命令看 `render.log` 或输出目录，确认进度，不要轻易中断：

```bash
tail -c 2000 render.log
ls -lh renders
```

### 9. 合并音频

把渲染出的无声视频和 MiniMax 旁白合并：

```bash
ffmpeg -y \
  -i renders/video-only.mp4 \
  -i assets/narration.mp3 \
  -map 0:v:0 -map 1:a:0 \
  -c:v copy -c:a aac -b:a 192k -shortest \
  renders/final.mp4
```

### 10. 最终校验

必须校验最终文件：

```bash
ffprobe -v error \
  -show_entries stream=index,codec_type,codec_name,width,height,duration,sample_rate,channels \
  -show_entries format=duration,size \
  -of json \
  renders/final.mp4
```

再抽帧检查字幕已经进入最终 MP4：

```bash
mkdir -p snapshots/final-check
ffmpeg -y -v error -ss 40 -i renders/final.mp4 -frames:v 1 snapshots/final-check/subtitled-40s.png
```

最终回复要包含：

- 最终 MP4 的绝对路径
- 分辨率、时长、视频编码、音频编码
- 是否已抽帧确认字幕
- 使用的非敏感 voice id（如果能确认）
- 如果有未完成项，明确说清楚

### 11. 爆款标题和封面

如果用户要求“爆款标题”“做封面”“横屏和竖屏”，在视频项目目录继续交付：

- `titles.md`：给 10 个可直接发布的标题
- `cover.html`：封面源文件，使用真实 HTML/CSS 中文文本，避免 AI 生图错字
- `covers/*-wide.png`：横屏封面，默认 `1280x720`
- `covers/*-portrait.png`：竖屏封面，默认 `1080x1920`

标题建议：

- 前 3 个直接指出痛点和误区
- 中间 4 个强调收益、顺序、免费、效率
- 后 3 个适合短视频平台的悬念和清单感
- 保留关键可搜索词，例如 `Codex`、插件名、`GitHub`、`免费`

封面建议：

- 中文大标题使用真实网页文本渲染，不把中文交给生成式图片模型
- 核心主标题 8-14 个汉字左右；副标题只保留一个强卖点
- 横屏突出主标题和一行插件标签；竖屏保留大标题、卖点和 3-6 个标签
- 颜色可以沿用视频 `DESIGN.md`，但注意平台缩略图上也要一眼可读

优先用 Chrome 或 Playwright 截图导出封面：

```bash
mkdir -p covers
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --headless=new --disable-gpu \
  --screenshot="$PWD/covers/cover-wide.png" \
  --window-size=1280,720 \
  "file://$PWD/cover.html?mode=wide"

/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --headless=new --disable-gpu \
  --screenshot="$PWD/covers/cover-portrait.png" \
  --window-size=1080,1920 \
  "file://$PWD/cover.html?mode=portrait"
```

如果 Playwright CLI 报浏览器缺失，不要卡住；先尝试系统 Chrome headless。导出后用 `sips` 校验尺寸：

```bash
sips -g pixelWidth -g pixelHeight covers/*.png
```

## 常见坑

- ffmpeg 可能没有 `subtitles` 或 `ass` 滤镜；这时不要卡住，改用 HyperFrames DOM 字幕烘录。
- 长视频渲染时不要用 `| head` 截断命令输出；用 `> render.log 2>&1`。
- 不要把 API key、MiniMax secret、`.env` 内容贴到回复或日志摘要里。
- 如果旁白比视频长，延长 HyperFrames timeline；如果视频比旁白长，检查是否 `-shortest` 截断了尾部。
- 用户说“图片不要省略”时，最终至少要用清单或画面检查确认所有素材都进过分镜。
- `npx playwright install chromium | head -c 4000` 可能因为 pipe 或下载源问题卡住/失败；需要截图时优先检查系统 Chrome 是否可用。
- 命令输出未知或可能很大时，用日志文件和 `tail -c 4000`，但不要把会持续写入的渲染命令 pipe 到 `head`。
- 如果用户后续补一句“继续”“再做封面”“再想标题”，默认在上一个视频项目目录继续工作，不要重建一套孤立目录。
