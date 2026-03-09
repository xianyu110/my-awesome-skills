#!/bin/bash

# Grok News Tracker 测试脚本

set -e

echo "🧪 测试 Grok News Tracker"
echo "=========================="

# 检查环境变量
if [ -z "$GROK_API_KEY" ]; then
  echo "❌ 错误：未设置 GROK_API_KEY 环境变量"
  echo "请运行：export KEY=xxx
  exit 1
fi

echo "✅ 环境变量检查通过"
echo ""

# 测试 1: 基础追踪
echo "📝 测试 1: 基础追踪"
npx -y bun scripts/tracker.ts track --sources tech --output test-report.md
if [ -f "test-report.md" ]; then
  echo "✅ 测试 1 通过：报告已生成"
  echo "预览："
  head -n 10 test-report.md
  rm test-report.md
else
  echo "❌ 测试 1 失败：报告未生成"
  exit 1
fi
echo ""

# 测试 2: JSON 格式
echo "📝 测试 2: JSON 格式输出"
npx -y bun scripts/tracker.ts track --sources ai --format json --output test-report.json
if [ -f "test-report.json" ]; then
  echo "✅ 测试 2 通过：JSON 报告已生成"
  echo "预览："
  head -n 5 test-report.json
  rm test-report.json
else
  echo "❌ 测试 2 失败：JSON 报告未生成"
  exit 1
fi
echo ""

# 测试 3: HTML 格式
echo "📝 测试 3: HTML 格式输出"
npx -y bun scripts/tracker.ts track --sources startup --format html --output test-report.html
if [ -f "test-report.html" ]; then
  echo "✅ 测试 3 通过：HTML 报告已生成"
  rm test-report.html
else
  echo "❌ 测试 3 失败：HTML 报告未生成"
  exit 1
fi
echo ""

# 测试 4: 多个信息源
echo "📝 测试 4: 多个信息源"
npx -y bun scripts/tracker.ts track --sources tech,ai,startup --output test-multi.md
if [ -f "test-multi.md" ]; then
  echo "✅ 测试 4 通过：多源报告已生成"
  rm test-multi.md
else
  echo "❌ 测试 4 失败：多源报告未生成"
  exit 1
fi
echo ""

echo "🎉 所有测试通过！"
echo ""
echo "💡 提示：你可以运行以下命令开始使用："
echo "   npx -y bun scripts/tracker.ts track"
