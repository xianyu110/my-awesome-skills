#!/usr/bin/env python3
"""
使用 FFmpeg 合成视频（简化版 - 无语音）
"""
import json
import sys
import subprocess
import requests
from pathlib import Path
from typing import Dict, List


def download_image(url: str, output_path: Path) -> Path:
    """下载图片"""
    response = requests.get(url)
    response.raise_for_status()
    
    with open(output_path, 'wb') as f:
        f.write(response.content)
    
    return output_path


def create_image_clip(image_path: Path, duration: float, output_path: Path, resolution: str = '1920x1080'):
    """创建图片视频片段"""
    cmd = [
        'ffmpeg', '-y',
        '-loop', '1',
        '-i', str(image_path),
        '-t', str(duration),
        '-vf', f'scale={resolution}:force_original_aspect_ratio=decrease,pad={resolution}:(ow-iw)/2:(oh-ih)/2',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-r', '30',
        str(output_path)
    ]
    
    subprocess.run(cmd, check=True, capture_output=True)


def create_subtitle_file(timeline: List[Dict], output_path: Path):
    """创建 SRT 字幕文件"""
    with open(output_path, 'w', encoding='utf-8') as f:
        for idx, segment in enumerate(timeline, 1):
            start = segment['start']
            end = segment['end']
            text = segment['text']
            
            # 转换时间格式
            start_time = f"{int(start//3600):02d}:{int((start%3600)//60):02d}:{int(start%60):02d},{int((start%1)*1000):03d}"
            end_time = f"{int(end//3600):02d}:{int((end%3600)//60):02d}:{int(end%60):02d},{int((end%1)*1000):03d}"
            
            f.write(f"{idx}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{text}\n\n")


def compose_video(script_file: str, output_dir: str = './output') -> str:
    """合成最终视频（无语音版）"""
    # 加载脚本
    with open(script_file, 'r', encoding='utf-8') as f:
        script = json.load(f)
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"🎬 开始合成视频（无语音版）...")
    
    # 下载图片
    images_dir = output_path / 'images'
    images_dir.mkdir(exist_ok=True)
    
    print(f"📥 下载配图...")
    image_files = []
    for img in script['images']:
        img_file = images_dir / f"image_{img['id']}.jpg"
        if not img_file.exists():
            try:
                download_image(img['url'], img_file)
                print(f"  ✓ 下载图片 {img['id']}")
            except Exception as e:
                print(f"  ✗ 下载图片 {img['id']} 失败: {e}")
                continue
        image_files.append(img_file)
    
    if not image_files:
        print("❌ 没有可用的图片")
        sys.exit(1)
    
    # 创建图片视频片段
    print(f"🖼️  生成图片片段...")
    clips_dir = output_path / 'clips'
    clips_dir.mkdir(exist_ok=True)
    
    clip_files = []
    for segment in script['timeline']:
        image_id = segment.get('image_id', 1)
        if image_id and image_id <= len(image_files):
            image_file = image_files[image_id - 1]
            clip_file = clips_dir / f"clip_{len(clip_files):03d}.mp4"
            
            try:
                create_image_clip(
                    image_file,
                    segment['duration'],
                    clip_file,
                    '1920x1080'
                )
                clip_files.append(clip_file)
                print(f"  ✓ 生成片段 {len(clip_files)}")
            except Exception as e:
                print(f"  ✗ 生成片段失败: {e}")
    
    if not clip_files:
        print("❌ 没有生成任何视频片段")
        sys.exit(1)
    
    # 合并视频片段
    print(f"🔗 合并视频片段...")
    concat_file = output_path / 'concat.txt'
    with open(concat_file, 'w') as f:
        for clip in clip_files:
            f.write(f"file '{clip.absolute()}'\n")
    
    final_video = output_path / 'final_video_no_audio.mp4'
    cmd = [
        'ffmpeg', '-y',
        '-f', 'concat',
        '-safe', '0',
        '-i', str(concat_file),
        '-c', 'copy',
        str(final_video)
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    
    # 生成字幕文件
    print(f"📝 生成字幕...")
    subtitle_file = output_path / 'subtitles.srt'
    create_subtitle_file(script['timeline'], subtitle_file)
    
    print(f"\n✅ 视频合成完成！")
    print(f"📹 视频文件：{final_video.absolute()}")
    print(f"📝 字幕文件：{subtitle_file.absolute()}")
    print(f"⏱️  总时长：{script['total_duration']:.1f} 秒")
    print(f"\n💡 提示：这是无语音版本，你可以：")
    print(f"   1. 使用剪映等工具导入视频和字幕")
    print(f"   2. 手动录制语音或使用其他 TTS 工具")
    print(f"   3. 添加背景音乐")
    
    return str(final_video)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python compose_video_simple.py <script_file> [output_dir]")
        sys.exit(1)
    
    script_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else './output'
    
    compose_video(script_file, output_dir)
