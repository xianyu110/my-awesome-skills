#!/usr/bin/env python3
"""
使用 FFmpeg 合成最终视频
"""
import json
import sys
import subprocess
from pathlib import Path
from typing import Dict, List


def load_config(config_file: str = '../config.json') -> Dict:
    """加载配置文件"""
    config_path = Path(__file__).parent.parent / 'config.json'
    
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    return {
        'ffmpeg': {
            'video_codec': 'libx264',
            'audio_codec': 'aac',
            'resolution': '1920x1080',
            'fps': 60
        }
    }


def download_image(url: str, output_path: Path) -> Path:
    """下载图片"""
    import requests
    
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
    """合成最终视频"""
    # 加载脚本
    with open(script_file, 'r', encoding='utf-8') as f:
        script = json.load(f)
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    config = load_config()
    ffmpeg_config = config['ffmpeg']
    
    print(f"🎬 开始合成视频...")
    
    # 下载图片
    images_dir = output_path / 'images'
    images_dir.mkdir(exist_ok=True)
    
    print(f"📥 下载配图...")
    image_files = []
    for img in script['images']:
        img_file = images_dir / f"image_{img['id']}.jpg"
        if not img_file.exists():
            download_image(img['url'], img_file)
        image_files.append(img_file)
    
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
            
            create_image_clip(
                image_file,
                segment['duration'],
                clip_file,
                ffmpeg_config['resolution']
            )
            clip_files.append(clip_file)
    
    # 合并视频片段
    print(f"🔗 合并视频片段...")
    concat_file = output_path / 'concat.txt'
    with open(concat_file, 'w') as f:
        for clip in clip_files:
            f.write(f"file '{clip.absolute()}'\n")
    
    video_no_audio = output_path / 'video_no_audio.mp4'
    cmd = [
        'ffmpeg', '-y',
        '-f', 'concat',
        '-safe', '0',
        '-i', str(concat_file),
        '-c', 'copy',
        str(video_no_audio)
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    
    # 添加音频
    print(f"🎵 添加音频...")
    audio_file = output_path / 'audio.mp3'
    
    if not audio_file.exists():
        print(f"⚠️  警告：音频文件不存在，跳过音频合成")
        final_video = video_no_audio
    else:
        final_video = output_path / 'final_video.mp4'
        cmd = [
            'ffmpeg', '-y',
            '-i', str(video_no_audio),
            '-i', str(audio_file),
            '-c:v', 'copy',
            '-c:a', ffmpeg_config['audio_codec'],
            '-shortest',
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
    
    return str(final_video)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python compose_video.py <script_file> [output_dir]")
        sys.exit(1)
    
    script_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else './output'
    
    compose_video(script_file, output_dir)
