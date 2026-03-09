---
name: efficient-git-workflow
title: 高效代码提交工作流
description: 自动化 Git 提交流程，支持批量提交、智能分组、快速验收。灵感来自 OpenClaw 作者 Peter 的高效开发模式。
version: 1.0.0
author: Jarvis
tags: [git, automation, workflow, productivity]
---

# 高效代码提交工作流 Skill

## 功能概述

自动化 Git 提交流程，支持：
- 批量提交多个文件变更
- 智能分组相关改动
- 自动生成提交信息
- 快速验收和推送
- 提交统计和分析

## 使用场景

- 大规模重构项目时快速提交
- 多个独立改动需要分别提交
- 自动化 CI/CD 流程中的代码提交
- 开发效率监控和统计

## 命令用法

### 1. 批量提交
```bash
efficient-git-workflow batch --files "src/**/*.js" --message "refactor: optimize performance"
```

### 2. 智能分组提交
```bash
efficient-git-workflow group --auto --message-template "feat: {category}"
```

### 3. 快速提交
```bash
efficient-git-workflow quick --staged --push
```

### 4. 提交统计
```bash
efficient-git-workflow stats --author "Peter" --since "2026-02-22" --until "2026-02-23"
```

## 配置

创建 `.efficient-git-config.json`：
```json
{
  "autoGroup": true,
  "groupBy": "directory",
  "messageTemplate": "{type}({scope}): {description}",
  "autoVerify": true,
  "autoPush": false,
  "batchSize": 50
}
```

## 工作原理

1. **检测变更** — 扫描工作区和暂存区的文件变更
2. **智能分组** — 按目录、类型或自定义规则分组
3. **生成提交信息** — 基于模板和变更内容自动生成
4. **验收** — 运行测试或自定义验收脚本
5. **提交和推送** — 执行 git commit 和 push

## 高级用法

### 自定义分组规则
```bash
efficient-git-workflow group --rule "src/components/**" --message "refactor(components): optimize"
```

### 条件提交
```bash
efficient-git-workflow batch --files "*.test.js" --condition "test-pass" --message "test: add coverage"
```

### 提交链接到 Issue
```bash
efficient-git-workflow quick --link-issue "#123" --message "fix: resolve issue"
```

## 性能指标

- 平均提交时间：< 2 秒/次
- 支持批量：100+ 文件/次
- 提交频率：可达每分钟 30+ 次

## 注意事项

- 确保工作区干净或所有变更已暂存
- 验收脚本应快速完成（< 1 秒）
- 推送前确认分支权限
- 大量提交时建议使用 `--dry-run` 预览

## 示例工作流

```bash
# 1. 检查变更
efficient-git-workflow status

# 2. 预览分组
efficient-git-workflow group --dry-run

# 3. 执行提交
efficient-git-workflow group --auto --verify

# 4. 查看统计
efficient-git-workflow stats --today
```

## 相关技能

- `parallel-task-manager` — 并行管理多个开发任务
- `ai-code-generator` — AI 辅助代码生成
- `dev-efficiency-monitor` — 开发效率监控
