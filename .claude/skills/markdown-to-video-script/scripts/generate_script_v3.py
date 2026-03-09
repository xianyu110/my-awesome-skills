#!/usr/bin/env python3
"""
生成口播稿和视频脚本 V3
短视频风格：节奏快、口语化、有煽动性
"""
import re
import json
import sys
from pathlib import Path
from typing import List, Dict


def extract_images(markdown_content: str) -> List[Dict[str, str]]:
    """提取 Markdown 中的所有图片"""
    pattern = r'!\[(.*?)\]\((.*?)\)'
    matches = re.findall(pattern, markdown_content)
    
    images = []
    for idx, (alt_text, url) in enumerate(matches, 1):
        images.append({
            'id': idx,
            'url': url,
            'alt': alt_text,
            'description': alt_text or f'配图 {idx}'
        })
    
    return images


def clean_text(text: str) -> str:
    """清理 Markdown 标记"""
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    text = re.sub(r'```[\s\S]*?```', '', text)
    text = re.sub(r'#+\s+', '', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'[_`]', '', text)
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    text = re.sub(r'^---+$', '', text, flags=re.MULTILINE)
    return text


def generate_narration_v3(markdown_content: str, target_words: int = 400) -> str:
    """
    生成口播稿 V3 - 短视频风格
    参考：节奏快、口语化、有煽动性
    """
    text = clean_text(markdown_content)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip() and len(p.strip()) > 5]
    
    # 提取核心内容
    opening_lines = []
    tech_lines = []
    reason_lines = []
    
    for p in paragraphs:
        # 开场痛点
        if any(kw in p for kw in ['你有没有', '想象', '遇到']) and len(opening_lines) < 2:
            opening_lines.append(p)
        
        # 技巧内容
        if any(kw in p for kw in ['不需要', '只需', '操作', '简单', '粘贴', '输入', '点击']) and len(p) < 100:
            tech_lines.append(p)
        
        # 原因/优势
        if any(kw in p for kw in ['原生', '支持', 'Token', '上下文', '免费', '国内']) and len(p) < 100:
            reason_lines.append(p)
    
    # 组装口播稿（短视频风格）
    parts = []
    
    # 1. 开头引导
    parts.append("如需网址，关注后查看后台私信即可！")
    
    # 2. 热点引入
    parts.append("今天给大家分享两个技巧，用Gemini看YouTube，效率直接提升10倍！")
    
    # 3. 痛点共鸣（1-2句）
    if opening_lines:
        parts.extend(opening_lines[:2])
    else:
        parts.append("YouTube上看到好视频，2小时长，全英文，没字幕，想看但没时间，直接放弃。")
    
    # 4. 技巧1
    parts.append("第一个技巧：一键提取完整字幕。")
    if tech_lines:
        parts.append(tech_lines[0])
    else:
        parts.append("不需要下载，不需要插件。打开Gemini，粘贴YouTube链接，输入提示词，完整字幕就出来了。")
    
    # 5. 技巧2
    parts.append("第二个技巧：个性化输出核心内容。")
    parts.append("面对2小时长视频，用一段提示词，让Gemini像课代表一样帮你划重点。输出目录、摘要、关键要点，一目了然。")
    
    # 6. 为什么选择
    parts.append("为什么选Gemini？三个原因：")
    parts.append("原生支持视频分析，不用下载转录；100万Token上下文，处理超长视频；国内免费可用，无需魔法。")
    
    # 7. 行动号召
    parts.append("话不多说，想要用这个免费AI工具的小伙伴，视频下方一键三连，评论区见！")
    
    narration = '\n\n'.join(parts)
    
    # 统计字数
    word_count = len(narration.replace('\n', '').replace(' ', ''))
    
    # 如果超出，进一步压缩
    if word_count > target_words * 1.3:
        compressed = []
        compressed.append("如需网址，关注后查看后台私信即可！")
        compressed.append("今天分享两个技巧，用Gemini看YouTube，效率提升10倍！")
        compressed.append("YouTube好视频，2小时长，全英文，没字幕，想看没时间。")
        compressed.append("第一个技巧：一键提取字幕。打开Gemini，粘贴链接，输入提示词，字幕就出来了。")
        compressed.append("第二个技巧：个性化输出。用提示词让Gemini划重点，输出目录和摘要。")
        compressed.append("为什么选Gemini？原生支持视频、100万Token上下文、国内免费。")
        compressed.append("想要用的小伙伴，一键三连，评论区见！")
        narration = '\n\n'.join(compressed)
    
    return narration


def generate_timeline(narration: str, images: List[Dict]) -> List[Dict]:
    """生成视频时间轴"""
    paragraphs = [p.strip() for p in narration.split('\n\n') if p.strip()]
    
    timeline = []
    current_time = 0
    
    for idx, paragraph in enumerate(paragraphs):
        # 估算停留时长（短视频节奏更快，每个字约 0.25 秒）
        char_count = len(paragraph.replace(' ', ''))
        duration = max(2, min(8, char_count * 0.25))
        
        # 匹配配图
        image_id = min(idx + 1, len(images)) if images else None
        
        timeline.append({
            'start': round(current_time, 2),
            'end': round(current_time + duration, 2),
            'duration': round(duration, 2),
            'text': paragraph,
            'image_id': image_id
        })
        
        current_time += duration
    
    return timeline


def generate_script(markdown_file: str, output_dir: str = './output') -> Dict:
    """生成完整视频脚本"""
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取标题
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else Path(markdown_file).stem
    
    # 生成口播稿
    narration = generate_narration_v3(content)
    word_count = len(narration.replace('\n', '').replace(' ', ''))
    
    # 提取配图
    images = extract_images(content)
    
    # 生成时间轴
    timeline = generate_timeline(narration, images)
    
    # 组装脚本
    script = {
        'title': title,
        'source_file': markdown_file,
        'narration': narration,
        'word_count': word_count,
        'images': images,
        'timeline': timeline,
        'total_duration': timeline[-1]['end'] if timeline else 0
    }
    
    # 保存脚本
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    script_file = output_path / 'script.json'
    with open(script_file, 'w', encoding='utf-8') as f:
        json.dump(script, f, ensure_ascii=False, indent=2)
    
    # 保存口播稿
    narration_file = output_path / 'narration.txt'
    with open(narration_file, 'w', encoding='utf-8') as f:
        f.write(narration)
    
    print(f"✅ 脚本生成完成")
    print(f"📝 口播稿：{word_count} 字")
    print(f"🖼️  配图数：{len(images)} 张")
    print(f"⏱️  预计时长：{script['total_duration']:.1f} 秒")
    print(f"📁 输出目录：{output_path.absolute()}")
    
    return script


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python generate_script_v3.py <markdown_file> [output_dir]")
        sys.exit(1)
    
    markdown_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else './output'
    
    generate_script(markdown_file, output_dir)
