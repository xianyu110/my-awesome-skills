#!/usr/bin/env python3
"""
调用 TTS API 生成语音
"""
import json
import sys
import requests
from pathlib import Path
from typing import Dict


def load_config(config_file: str = '../config.json') -> Dict:
    """加载配置文件"""
    config_path = Path(__file__).parent.parent / 'config.json'
    
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # 默认配置
    return {
        'tts': {
            'api_url': 'http://localhost:8000/api/tts',
            'voice': 'default',
            'speed': 1.0,
            'pitch': 1.0
        }
    }


def generate_tts(script_file: str, output_dir: str = './output') -> str:
    """生成 TTS 语音"""
    # 加载脚本
    with open(script_file, 'r', encoding='utf-8') as f:
        script = json.load(f)
    
    narration = script['narration']
    
    # 加载配置
    config = load_config()
    tts_config = config['tts']
    
    print(f"🎙️  正在生成语音...")
    print(f"📝 文本长度：{len(narration)} 字")
    
    # 调用 TTS API
    try:
        response = requests.post(
            tts_config['api_url'],
            json={'text': narration},
            timeout=300
        )
        response.raise_for_status()
        
        result = response.json()
        
        if result.get('success'):
            audio_url = result['url']
            print(f"✅ 语音生成成功")
            print(f"🔗 音频链接：{audio_url}")
            
            # 下载音频文件
            audio_response = requests.get(audio_url)
            audio_response.raise_for_status()
            
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            audio_file = output_path / 'audio.mp3'
            with open(audio_file, 'wb') as f:
                f.write(audio_response.content)
            
            print(f"💾 音频已保存：{audio_file.absolute()}")
            
            # 更新脚本文件
            script['audio_file'] = str(audio_file)
            script['audio_url'] = audio_url
            
            with open(script_file, 'w', encoding='utf-8') as f:
                json.dump(script, f, ensure_ascii=False, indent=2)
            
            return str(audio_file)
        else:
            raise Exception(result.get('message', '语音生成失败'))
    
    except Exception as e:
        print(f"❌ 错误：{e}")
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python generate_tts.py <script_file> [output_dir]")
        sys.exit(1)
    
    script_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else './output'
    
    generate_tts(script_file, output_dir)
