#!/bin/bash

# AI Mirror Publisher 整合测试脚本

echo "========================================="
echo "  AI Mirror Publisher 整合测试"
echo "========================================="
echo ""

# 检查依赖
echo "检查依赖..."

if ! command -v bun &> /dev/null; then
    echo "❌ 错误: 未安装 bun"
    echo "   安装: curl -fsSL https://bun.sh/install | bash"
    exit 1
fi
echo "✓ bun 已安装"

if ! command -v git &> /dev/null; then
    echo "❌ 错误: 未安装 git"
    exit 1
fi
echo "✓ git 已安装"

if ! command -v curl &> /dev/null; then
    echo "❌ 错误: 未安装 curl"
    exit 1
fi
echo "✓ curl 已安装"

echo ""
echo "========================================="
echo "  依赖检查完成！"
echo "========================================="
echo ""

# 检查配置文件
if [ ! -f ".claude/skills/ai-mirror-publisher/examples/config.json" ]; then
    echo "❌ 错误: 配置文件不存在"
    exit 1
fi
echo "✓ 配置文件存在"

# 检查脚本文件
if [ ! -f ".claude/skills/ai-mirror-publisher/scripts/publish.ts" ]; then
    echo "❌ 错误: 发布脚本不存在"
    exit 1
fi
echo "✓ 发布脚本存在"

echo ""
echo "========================================="
echo "  准备就绪！"
echo "========================================="
echo ""
echo "使用方法："
echo ""
echo "1. 基础用法："
echo "   bun .claude/skills/ai-mirror-publisher/scripts/publish.ts \\"
echo "     --tools \"chatgpt-gpt5.2,claude-opus-4.5\" \\"
echo "     --github-user \"your-username\" \\"
echo "     --github-token \"ghp_xxx\" \\"
echo "     --main-url \"https://geminiai.asia/list/#/home\" \\"
echo "     --nav-url \"https://chatgpt-plus.top/\""
echo ""
echo "2. 使用配置文件："
echo "   bun .claude/skills/ai-mirror-publisher/scripts/publish.ts \\"
echo "     --config config.json"
echo ""
echo "3. 查看帮助："
echo "   bun .claude/skills/ai-mirror-publisher/scripts/publish.ts --help"
echo ""
echo "========================================="
