#!/usr/bin/env python3
"""
自动执行完整视频生成流程
"""
import sys
import subprocess
from pathlib import Path


def run_step(script_name: str, *args):
    """运行单个步骤"""
    script_path = Path(__file__).parent / script_name
    cmd = ['python3', str(script_path)] + list(args)
    
    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        print(f"❌ 步骤失败：{script_name}")
        sys.exit(1)


def auto_generate(markdown_file: str, output_dir: str = './output'):
    """自动生成完整视频"""
    print("=" * 60)
    print("🚀 开始自动生成视频")
    print("=" * 60)
    
    output_path = Path(output_dir)
    script_file = output_path / 'script.json'
    
    # 步骤 1：生成脚本
    print("\n📝 步骤 1/3：生成脚本...")
    run_step('generate_script.py', markdown_file, output_dir)
    
    # 步骤 2：生成语音
    print("\n🎙️  步骤 2/3：生成语音...")
    run_step('generate_tts.py', str(script_file), output_dir)
    
    # 步骤 3：合成视频
    print("\n🎬 步骤 3/3：合成视频...")
    run_step('compose_video.py', str(script_file), output_dir)
    
    print("\n" + "=" * 60)
    print("🎉 视频生成完成！")
    print("=" * 60)
    print(f"\n📁 输出目录：{output_path.absolute()}")
    print(f"📹 视频文件：{output_path / 'final_video.mp4'}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python auto_generate.py <markdown_file> [output_dir]")
        print("\n示例:")
        print("  python auto_generate.py article.md")
        print("  python auto_generate.py article.md ./my_output")
        sys.exit(1)
    
    markdown_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else './output'
    
    auto_generate(markdown_file, output_dir)
