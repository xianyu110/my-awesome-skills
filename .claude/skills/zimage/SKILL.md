---
name: zimage
description: 使用ModelScope Z-Image-Turbo模型生成图片。支持通过Prompt描述生成图片。
---

# Z-Image-Turbo 图片生成

此技能允许用户通过提供文本描述（Prompt）来使用ModelScope的Z-Image-Turbo模型生成图片。

## 功能概述

- **文生图**：根据用户提供的文本描述生成图片。
- **异步处理**：ModelScope API支持异步图片生成，技能将轮询任务状态直至完成或失败。

## 使用指引

### API Key 配置

为了使用此技能，您需要一个有效的ModelScope API Key。请将其设置为环境变量 `MODELSCOPE_API_KEY`。

**设置环境变量（推荐）：**
```bash
# Linux/Mac
export KEY=xxx

# Windows CMD
set MODELSCOPE_API_KEY=ms-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Windows PowerShell
$env:MODELSCOPE_API_KEY="ms-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

**您提供的API Key：** `ms-0e3fbffc-fe5f-408b-86c0-3e02b030088f`

### 命令行使用

本技能通过 `scripts/generate_zimage.py` 脚本执行。

**文生图命令模板：**
```bash
python scripts/generate_zimage.py --prompt "你的图片描述" [--filename "输出文件名.jpg"]
```

**参数说明：**

| 参数       | 必填 | 说明                                    |
|------------|------|-----------------------------------------|
| `--prompt` | 是   | 用于生成图片的文本描述。                |
| `--filename` | 否   | 生成图片的保存路径和文件名，默认为 `result_image.jpg`。 |

## 使用示例

### 生成一张金猫的图片
```bash
python skills/zimage/scripts/generate_zimage.py --prompt "A golden cat"
```
图片将保存为 `result_image.jpg`。

### 生成一张日落风景的图片，并指定文件名
```bash
python skills/zimage/scripts/generate_zimage.py --prompt "A beautiful sunset landscape" --filename "sunset_view.jpg"
```
图片将保存为 `sunset_view.jpg`。

## 注意事项

- 图片生成过程可能需要一定时间，技能会轮询API直到生成完成。
- 确保您的 `MODELSCOPE_API_KEY` 是有效的，否则会返回认证错误。
- 确保工作目录有写入权限，以便保存生成的图片。