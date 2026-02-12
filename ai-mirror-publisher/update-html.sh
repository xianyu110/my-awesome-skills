#!/bin/bash

# 更新已有仓库的 HTML 文件

echo "========================================="
echo "  更新 HTML 文件"
echo "  添加图片展示和视觉优化"
echo "========================================="
echo ""

# 检查参数
if [ $# -eq 0 ]; then
    echo "用法: bash update-html.sh <仓库目录>"
    echo ""
    echo "示例:"
    echo "  bash update-html.sh ai-mirror-repos/chatgpt-gpt5.2-mirror"
    echo "  bash update-html.sh ai-mirror-batch-upload/claude-opus-4.5-mirror"
    echo ""
    echo "或批量更新所有仓库:"
    echo "  bash update-html.sh ai-mirror-repos/*-mirror"
    exit 1
fi

# 更新函数
update_repo() {
    local repo_dir=$1
    
    if [ ! -d "$repo_dir" ]; then
        echo "❌ 目录不存在: $repo_dir"
        return 1
    fi
    
    echo "处理: $repo_dir"
    
    # 检查是否有 index.html
    if [ ! -f "$repo_dir/index.html" ]; then
        echo "  ⚠️  未找到 index.html，跳过"
        return 0
    fi
    
    # 检查是否有 images 目录
    if [ ! -d "$repo_dir/images" ]; then
        echo "  ⚠️  未找到 images 目录，跳过"
        return 0
    fi
    
    # 进入目录
    cd "$repo_dir" || return 1
    
    # 检查是否是 git 仓库
    if [ ! -d ".git" ]; then
        echo "  ⚠️  不是 Git 仓库，跳过推送"
        cd - > /dev/null
        return 0
    fi
    
    # 提示用户
    echo "  ✓ 找到 index.html 和 images 目录"
    echo "  ℹ️  需要手动重新生成 index.html"
    echo "  ℹ️  或使用新脚本重新生成整个仓库"
    
    cd - > /dev/null
    echo ""
}

# 处理所有参数
for repo in "$@"; do
    update_repo "$repo"
done

echo "========================================="
echo "  完成！"
echo "========================================="
echo ""
echo "建议操作："
echo "1. 使用新脚本重新生成所有仓库（推荐）"
echo "   bun .claude/skills/ai-mirror-publisher/scripts/publish.ts \\"
echo "     --config .claude/skills/ai-mirror-publisher/test-config.json"
echo ""
echo "2. 或手动更新单个仓库的 index.html"
echo "   然后推送到 GitHub"
echo ""
