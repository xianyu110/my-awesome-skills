# Markdown 自动转视频

将 Markdown 文章自动转换成完整视频，支持从脚本生成到视频合成的全流程自动化。

## 快速开始

### 1. 安装依赖

```bash
# Python 依赖
pip install requests

# 系统依赖（FFmpeg）
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg
```

### 2. 启动 TTS 服务

```bash
# 克隆 TTS 项目
git clone https://github.com/chen20250312/tts.git
cd tts

# 启动服务
docker-compose up -d

# 验证服务
curl http://localhost:8000/docs
```

### 3. 生成视频

```bash
cd .claude/skills/markdown-to-video-script/scripts

# 自动生成完整视频
python3 auto_generate.py ../../../../你的文章.md

# 或分步执行
python3 generate_script.py ../../../../你的文章.md
python3 generate_tts.py ./output/script.json
python3 compose_video.py ./output/script.json
```

## 使用示例

### 示例 1：自动生成

```bash
python3 scripts/auto_generate.py "用Gemini看YouTube效率提升10倍这2个技巧我藏了半年.md"
```

输出：
```
📝 步骤 1/3：生成脚本...
✅ 脚本生成完成
📝 口播稿：498 字
🖼️  配图数：6 张
⏱️  预计时长：150.5 秒

🎙️  步骤 2/3：生成语音...
✅ 语音生成成功
💾 音频已保存

🎬 步骤 3/3：合成视频...
✅ 视频合成完成！
📹 视频文件：./output/final_video.mp4
```

### 示例 2：仅生成脚本

```bash
python3 scripts/generate_script.py "你的文章.md"
```

生成文件：
- `output/script.json` - 完整脚本数据
- `output/narration.txt` - 口播稿文本

### 示例 3：自定义输出目录

```bash
python3 scripts/auto_generate.py "文章.md" "./my_videos/video_001"
```

## 配置说明

编辑 `config.json` 自定义参数：

```json
{
  "tts": {
    "api_url": "http://localhost:8000/api/tts",
    "speed": 1.0,
    "pitch": 1.0
  },
  "ffmpeg": {
    "resolution": "1920x1080",
    "fps": 60
  }
}
```

## 输出文件

```
output/
├── script.json          # 脚本数据
├── narration.txt        # 口播稿
├── audio.mp3            # 语音文件
├── subtitles.srt        # 字幕文件
├── images/              # 下载的配图
│   ├── image_1.jpg
│   └── image_2.jpg
├── clips/               # 视频片段
│   ├── clip_001.mp4
│   └── clip_002.mp4
└── final_video.mp4      # 最终视频
```

## 技术栈

- **TTS**：TTSMaker API（支持声音克隆）
- **视频合成**：FFmpeg
- **字幕生成**：SRT 格式
- **图片处理**：FFmpeg scale + pad

## 常见问题

### Q: TTS 服务连接失败？
A: 确保 TTS 服务已启动：`docker ps | grep tts`

### Q: FFmpeg 命令找不到？
A: 安装 FFmpeg：`brew install ffmpeg`（macOS）

### Q: 视频时长和音频不匹配？
A: 脚本会自动调整，使用 `-shortest` 参数

### Q: 如何自定义视频分辨率？
A: 修改 `config.json` 中的 `ffmpeg.resolution`

## 进阶功能

### 声音克隆

1. 准备 10 秒音频样本
2. 上传到 TTS 服务
3. 修改 `config.json` 中的 `tts.voice`

### 批量生成

```bash
for file in *.md; do
  python3 scripts/auto_generate.py "$file" "./output/${file%.md}"
done
```

### 添加背景音乐

```bash
ffmpeg -i final_video.mp4 -i bgm.mp3 -filter_complex "[1:a]volume=0.2[a1];[0:a][a1]amix=inputs=2[a]" -map 0:v -map "[a]" -c:v copy output_with_bgm.mp4
```

## 许可证

MIT License
