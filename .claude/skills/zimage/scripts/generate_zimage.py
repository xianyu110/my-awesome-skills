import requests
import time
import json
import os
from PIL import Image
from io import BytesIO
import argparse

# --- 配置参数 ---
BASE_URL = 'https://api-inference.modelscope.cn/'
MODEL_ID = "Tongyi-MAI/Z-Image-Turbo" # ModelScope Model-Id, required

# 从环境变量获取 API Key
# 优先使用命令行参数指定的 API Key，否则从环境变量 MODELSCOPE_API_KEY 中获取
API_KEY = os.getenv('MODELSCOPE_API_KEY')

# --- 请求头 ---
COMMON_HEADERS = {
    "Content-Type": "application/json",
}

def generate_zimage(prompt, filename="result_image.jpg", api_key_override=None):
    """
    使用ModelScope Z-Image-Turbo模型生成图片。

    Args:
        prompt (str): 图片描述。
        filename (str): 输出图片的文件名。
        api_key_override (str, optional): 覆盖环境变量中的API Key。默认为None。
    """
    current_api_key = api_key_override if api_key_override else API_KEY

    if not current_api_key:
        print("错误: 未设置 MODELSCOPE_API_KEY 环境变量或未通过参数传入API Key。")
        print("请设置环境变量或使用 --api-key 参数。")
        exit(1)

    headers_with_auth = {
        **COMMON_HEADERS,
        "Authorization": f"Bearer {current_api_key}",
    }

    print(f"🎨 图片生成已启动！\n⏱️ 预计时间: 30-180秒 (取决于队列和图片复杂度)")
    print(f"正在使用 ModelScope Z-Image-Turbo 模型生成图片...")
    print(f"提示词: {prompt}")
    print(f"输出文件: {filename}")

    # 发送图片生成请求（异步模式）
    response = requests.post(
        f"{BASE_URL}v1/images/generations",
        headers={**headers_with_auth, "X-ModelScope-Async-Mode": "true"},
        data=json.dumps({
            "model": MODEL_ID,
            "prompt": prompt
        }, ensure_ascii=False).encode('utf-8')
    )
    response.raise_for_status() # 检查HTTP错误

    task_id = response.json()["task_id"]
    print(f"任务ID: {task_id}")
    print("正在查询生成任务状态...")

    start_time = time.time()
    while True:
        elapsed_time = int(time.time() - start_time)
        print(f"🔄 已进行 {elapsed_time}秒...")

        result = requests.get(
            f"{BASE_URL}v1/tasks/{task_id}",
            headers={**headers_with_auth, "X-ModelScope-Task-Type": "image_generation"},
        )
        result.raise_for_status()
        data = result.json()

        if data["task_status"] == "SUCCEED":
            print(f"✓ 图片已成功生成！")
            image_url = data["output_images"][0]
            print(f"图片URL: {image_url}")

            # 下载图片
            image_content = requests.get(image_url).content
            image = Image.open(BytesIO(image_content))
            image.save(filename)
            print(f"✅ 图片已保存到: {filename}")
            break
        elif data["task_status"] == "FAILED":
            print("❌ 图片生成失败。")
            if "message" in data:
                print(f"错误信息: {data['message']}")
            break
        elif data["task_status"] == "RUNNING":
            pass # 继续等待
        elif data["task_status"] == "WAITING":
            pass # 继续等待
        else:
            print(f"未知任务状态: {data['task_status']}")
            break

        time.sleep(5) # 每5秒轮询一次

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='使用ModelScope Z-Image-Turbo模型生成图片。')
    parser.add_argument('--prompt', type=str, required=True, help='用于生成图片的文本描述。')
    parser.add_argument('--filename', type=str, default='result_image.jpg', help='生成的图片保存路径和文件名。')
    parser.add_argument('--api-key', type=str, help='ModelScope API Key (可选，将覆盖环境变量)。')

    args = parser.parse_args()

    generate_zimage(args.prompt, args.filename, args.api_key)