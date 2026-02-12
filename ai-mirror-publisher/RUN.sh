#!/bin/bash

# AI Mirror Publisher - 快速运行脚本

echo "========================================="
echo "  AI Mirror Publisher"
echo "  一键生成图文并茂的AI镜像站指南"
echo "========================================="
echo ""

# 检查 bun
if ! command -v bun &> /dev/null; then
    echo "❌ 错误: 未安装 bun"
    echo "   安装: curl -fsSL https://bun.sh/install | bash"
    exit 1
fi

# 检查配置文件
if [ ! -f ".claude/skills/ai-mirror-publisher/test-config.json" ]; then
    echo "❌ 错误: 配置文件不存在"
    exit 1
fi

echo "✓ 环境检查通过"
echo ""
echo "开始运行..."
echo ""

# 运行脚本
bun .claude/skills/ai-mirror-publisher/scripts/publish.ts \
  --config .claude/skills/ai-mirror-publisher/test-config.json

echo ""
echo "========================================="
echo "  完成！"
echo "========================================="
