#!/usr/bin/env python3
"""
生成口播稿和视频脚本 V2
基于用户的写作风格模板
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


def generate_narration_v2(markdown_content: str, target_words: int = 500) -> str:
    """
    生成口播稿 V2
    严格按照用户的风格模板：
    1. 开场白（引入问题）
    2. 技巧1（简洁说明）
    3. 技巧2（简洁说明）
    4. 为什么选择（3个原因）
    5. 使用建议
    6. 总结 + 行动号召
    """
    text = clean_text(markdown_content)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip() and len(p.strip()) > 5]
    
    # 提取各部分内容
    opening = []
    tech1_content = []
    tech2_content = []
    reasons = []
    suggestions = []
    closing = []
    
    in_tech1 = False
    in_tech2 = False
    in_reasons = False
    in_suggestions = False
    
    for p in paragraphs:
        # 开场白
        if any(kw in p for kw in ['你有没有', '想象一下', '大家好', '今天分享']) and not opening:
            opening.append(p)
        elif len(opening) > 0 and len(opening) < 4 and not in_tech1:
            opening.append(p)
        
        # 技巧1
        if '技巧1' in p or '一键提取' in p:
            in_tech1 = True
            in_tech2 = False
        elif in_tech1 and ('技巧2' in p or '个性化输出' in p):
            in_tech1 = False
            in_tech2 = True
        elif in_tech1 and len(tech1_content) < 4:
            if len(p) < 150 and ('不需要' in p or '只需' in p or '操作' in p or '效果' in p or '实测' in p):
                tech1_content.append(p)
        
        # 技巧2
        elif in_tech2 and len(tech2_content) < 4:
            if len(p) < 150 and ('面对' in p or '希望' in p or '输出' in p or '可以' in p):
                tech2_content.append(p)
        
        # 为什么选择
        if '为什么选Gemini' in p or '为什么不用ChatGPT' in p:
            in_reasons = True
            in_tech2 = False
        elif in_reasons and len(reasons) < 4:
            if '优势' in p or '原因' in p or '支持' in p or '上下文' in p or '免费' in p:
                reasons.append(p)
        
        # 使用建议
        if '使用建议' in p or '我的建议' in p:
            in_suggestions = True
            in_reasons = False
        elif in_suggestions and len(suggestions) < 3:
            if len(p) < 120:
                suggestions.append(p)
        
        # 结尾
        if any(kw in p for kw in ['总结', '好了', '点赞', '转发', '信息爆炸']):
            closing.append(p)
    
    # 组装口播稿（严格按照模板）
    narration_parts = []
    
    # 0. 开头引导（固定）
    narration_parts.append("如需网址，关注后查看后台私信即可！")
    
    # 1. 开场白
    if opening:
        narration_parts.append("大家好！今天分享两个我藏了半年的技巧，用Gemini看YouTube，效率直接提升10倍。")
        narration_parts.extend(opening[:3])
    
    # 2. 技巧1
    narration_parts.append("**第一个技巧：一键提取完整字幕**")
    if tech1_content:
        narration_parts.extend(tech1_content[:3])
    else:
        narration_parts.append("不需要下载视频，也不需要安装插件。打开Gemini，直接把YouTube链接粘贴进去，输入提示词，就能看到完整字幕。")
    
    # 3. 技巧2
    narration_parts.append("**第二个技巧：个性化输出核心内容**")
    if tech2_content:
        narration_parts.extend(tech2_content[:3])
    else:
        narration_parts.append("面对2小时的长视频，可以用更强大的提示词，让Gemini像课代表一样帮你划重点。")
    
    # 4. 为什么选Gemini
    narration_parts.append("**为什么选Gemini？**")
    if reasons:
        # 提取3个原因
        reason_texts = []
        for r in reasons:
            if '原生支持' in r or '视频分析' in r:
                reason_texts.append("第一，原生支持视频分析，不用下载转录")
            elif 'Token' in r or '上下文' in r or '超长' in r:
                reason_texts.append("第二，100万Token上下文，可以处理超长视频")
            elif '免费' in r or '国内' in r or '魔法' in r:
                reason_texts.append("第三，国内免费可用，无需魔法")
        
        if reason_texts:
            narration_parts.append("；".join(reason_texts[:3]) + "。")
        else:
            narration_parts.append("三个原因：原生支持视频分析、100万Token上下文、国内免费可用。")
    else:
        narration_parts.append("三个原因：原生支持视频分析、100万Token上下文、国内免费可用。")
    
    # 5. 使用建议（可选）
    if suggestions:
        narration_parts.append("**我的使用建议**")
        narration_parts.extend(suggestions[:2])
    
    # 6. 总结
    if closing:
        # 只添加总结部分，不包含"点赞转发"
        summary = [c for c in closing if '点赞' not in c and '转发' not in c]
        if summary:
            narration_parts.extend(summary[-1:])
        else:
            narration_parts.append("在信息爆炸的时代，我们缺的不是信息，而是有效筛选和吸收信息的方法。善用AI，可以把我们从低效的信息处理中解放出来。")
    else:
        narration_parts.append("在信息爆炸的时代，我们缺的不是信息，而是有效筛选和吸收信息的方法。善用AI，可以把我们从低效的信息处理中解放出来。")
    
    # 7. 引导行动（固定结尾，总是添加）
    narration_parts.append("好了，今天的分享就到这里。如需网址，三连关注UP，查看后台私信即可！")
    
    # 组合
    narration = '\n\n'.join(narration_parts)
    
    # 统计字数并调整
    word_count = len(narration.replace('\n', '').replace(' ', '').replace('*', ''))
    
    # 如果超出太多，压缩
    if word_count > target_words * 1.3:
        compressed = []
        compressed.append("如需网址，关注后查看后台私信即可！")
        compressed.append("大家好！今天分享两个技巧，用Gemini看YouTube，效率提升10倍。")
        compressed.extend(opening[:2])
        compressed.append("**第一个技巧：一键提取完整字幕**")
        compressed.extend(tech1_content[:2])
        compressed.append("**第二个技巧：个性化输出核心内容**")
        compressed.extend(tech2_content[:2])
        compressed.append("**为什么选Gemini？**")
        compressed.append("三个原因：原生支持视频分析、100万Token上下文、国内免费可用。")
        compressed.extend(closing[-2:])
        compressed.append("好了，今天的分享就到这里。如需网址，三连关注UP，查看后台私信即可！")
        narration = '\n\n'.join(compressed)
    
    return narration


def generate_timeline(narration: str, images: List[Dict]) -> List[Dict]:
    """生成视频时间轴"""
    paragraphs = [p.strip() for p in narration.split('\n\n') if p.strip()]
    
    timeline = []
    current_time = 0
    
    for idx, paragraph in enumerate(paragraphs):
        # 估算停留时长（每个字约 0.3 秒）
        char_count = len(paragraph.replace(' ', '').replace('*', ''))
        duration = max(3, min(10, char_count * 0.3))
        
        # 匹配配图
        image_id = min(idx + 1, len(images)) if images else None
        
        timeline.append({
            'start': round(current_time, 2),
            'end': round(current_time + duration, 2),
            'duration': round(duration, 2),
            'text': paragraph.replace('**', ''),
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
    narration = generate_narration_v2(content)
    word_count = len(narration.replace('\n', '').replace(' ', '').replace('*', ''))
    
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
        print("用法: python generate_script_v2.py <markdown_file> [output_dir]")
        sys.exit(1)
    
    markdown_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else './output'
    
    generate_script(markdown_file, output_dir)
