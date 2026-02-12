#!/bin/bash

# 公众号文章改写工具 - Python 爬虫安装脚本

echo "🚀 开始安装 Python 爬虫工具..."

# 检查是否在正确的目录
if [ ! -f "package.json" ]; then
    echo "❌ 请在 wechat-article-rewriter 目录下运行此脚本"
    exit 1
fi

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 未检测到 Python 3，请先安装 Python"
    exit 1
fi

echo "✅ Python 版本: $(python3 --version)"

# 克隆爬虫项目
if [ -d "python-crawler" ]; then
    echo "⚠️  python-crawler 目录已存在，跳过克隆"
else
    echo "📥 克隆 Access_wechat_article 项目..."
    git clone https://github.com/yeximm/Access_wechat_article.git python-crawler
    
    if [ $? -ne 0 ]; then
        echo "❌ 克隆失败，请检查网络连接"
        exit 1
    fi
    echo "✅ 克隆成功"
fi

# 进入爬虫目录
cd python-crawler

# 创建虚拟环境
if [ -d "venv" ]; then
    echo "⚠️  虚拟环境已存在，跳过创建"
else
    echo "🔧 创建 Python 虚拟环境..."
    python3 -m venv venv
    echo "✅ 虚拟环境创建成功"
fi

# 激活虚拟环境并安装依赖
echo "📦 安装 Python 依赖包..."
source venv/bin/activate

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败"
        exit 1
    fi
    echo "✅ 依赖安装成功"
else
    echo "❌ 未找到 requirements.txt 文件"
    exit 1
fi

deactivate

cd ..

echo ""
echo "✅ Python 爬虫工具安装完成！"
echo ""
echo "📋 下一步操作："
echo "1. 安装并配置微信 PC 版（推荐版本：4.1.5.16）"
echo "2. 安装并配置 Fiddler Classic（推荐版本：v5.0.20253.3311）"
echo "3. 配置微信代理：127.0.0.1:8888"
echo "4. 查看详细配置指南：cat PYTHON-CRAWLER-SETUP.md"
echo ""
echo "🧪 测试抓取："
echo "cd python-crawler"
echo "source venv/bin/activate"
echo "python main.py"
echo ""
