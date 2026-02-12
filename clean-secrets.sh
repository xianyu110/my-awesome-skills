#!/bin/bash
# 清理敏感信息脚本

echo "🔒 开始清理敏感信息..."

# 1. 清理 GitHub tokens
echo "清理 GitHub tokens..."
find . -type f \( -name "*.md" -o -name "*.json" -o -name "*.sh" -o -name "*.ts" \) -exec sed -i '' 's/ghp_[A-Za-z0-9]\{36\}/ghp_YOUR_GITHUB_TOKEN_HERE/g' {} \;

# 2. 清理 API keys (sk- 开头的)
echo "清理 API keys..."
find . -type f \( -name "*.md" -o -name "*.json" -o -name "*.py" -o -name "*.sh" \) -exec sed -i '' 's/sk-[A-Za-z0-9]\{48\}/sk-YOUR_API_KEY_HERE/g' {} \;

# 3. 清理 ModelScope API keys
echo "清理 ModelScope API keys..."
find . -type f \( -name "*.ts" -o -name "*.json" -o -name "*.md" \) -exec sed -i '' 's/ms-[a-f0-9-]\{36\}/ms-YOUR_MODELSCOPE_KEY_HERE/g' {} \;

# 4. 清理特定的敏感配置文件
echo "清理配置文件..."
if [ -f "ai-mirror-publisher/test-config.json" ]; then
    rm "ai-mirror-publisher/test-config.json"
    echo "  已删除 test-config.json"
fi

echo "✅ 清理完成！"
echo ""
echo "请检查以下文件是否还有敏感信息："
echo "  - batch-ai-mirror-github-uploader.md"
echo "  - ai-mirror-publisher/完成通知.md"
echo "  - ai-mirror-publisher/运行指南.md"
