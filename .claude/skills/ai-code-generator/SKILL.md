---
name: ai-code-generator
title: AI 辅助代码生成器
description: 基于需求和上下文自动生成代码，支持多语言、代码审查、自动测试生成。
version: 1.0.0
author: Jarvis
tags: [ai, code-generation, automation, development]
---

# AI 辅助代码生成器 Skill

## 功能概述

AI 驱动的代码生成和优化：
- 从需求自动生成代码
- 多语言支持（JS、Python、Go、Rust 等）
- 自动代码审查和优化
- 测试用例自动生成
- 文档自动生成

## 使用场景

- 快速原型开发
- 大规模代码重构
- 测试覆盖率提升
- 代码质量改进
- 文档自动化

## 命令用法

### 1. 从需求生成代码
```bash
ai-code-generator generate --requirement "创建一个用户认证模块" --language javascript --output src/auth.js
```

### 2. 代码优化
```bash
ai-code-generator optimize --file src/slow-function.js --target "performance"
```

### 3. 生成测试
```bash
ai-code-generator test --file src/utils.js --coverage 80 --output tests/utils.test.js
```

### 4. 代码审查
```bash
ai-code-generator review --file src/main.js --strict
```

### 5. 生成文档
```bash
ai-code-generator docs --file src/api.js --format markdown --output docs/api.md
```

## 配置

创建 `.ai-code-config.json`：
```json
{
  "model": "claude-opus",
  "language": "javascript",
  "codeStyle": "airbnb",
  "testFramework": "jest",
  "docFormat": "jsdoc",
  "autoReview": true,
  "reviewStrict": false,
  "maxTokens": 4000,
  "temperature": 0.3
}
```

## 工作原理

1. **需求分析** — 解析需求和上下文
2. **代码生成** — 调用 AI 模型生成代码
3. **验证** — 语法检查和类型检查
4. **优化** — 性能和可读性优化
5. **测试** — 生成测试用例并验证

## 高级用法

### 批量生成
```bash
ai-code-generator batch --requirements requirements.json --output-dir src/generated
```

### 上下文感知生成
```bash
ai-code-generator generate --requirement "添加缓存层" --context "src/**/*.js" --analyze-patterns
```

### 增量生成
```bash
ai-code-generator generate --requirement "扩展功能" --base-file src/existing.js --merge
```

### 代码转换
```bash
ai-code-generator convert --file src/old.js --from javascript --to typescript
```

## 性能指标

- 代码生成速度：< 5s/函数
- 测试生成速度：< 10s/文件
- 代码审查速度：< 3s/文件
- 准确率：> 95%

## 质量指标

- **代码覆盖率** — 自动生成的测试覆盖率
- **代码复杂度** — 生成代码的圈复杂度
- **性能** — 生成代码的执行效率
- **可维护性** — 代码可读性和文档完整性

## 示例工作流

```bash
# 1. 从需求生成代码
ai-code-generator generate \
  --requirement "创建 REST API 端点" \
  --language javascript \
  --output src/api.js

# 2. 生成测试
ai-code-generator test \
  --file src/api.js \
  --coverage 80 \
  --output tests/api.test.js

# 3. 代码审查
ai-code-generator review \
  --file src/api.js \
  --strict

# 4. 生成文档
ai-code-generator docs \
  --file src/api.js \
  --format markdown \
  --output docs/api.md

# 5. 优化性能
ai-code-generator optimize \
  --file src/api.js \
  --target performance
```

## 最佳实践

- 提供清晰的需求描述
- 包含相关的代码上下文
- 指定代码风格和约定
- 验证生成的代码
- 定期审查和优化

## 相关技能

- `efficient-git-workflow` — 高效代码提交
- `parallel-task-manager` — 并行任务管理
- `dev-efficiency-monitor` — 开发效率监控
