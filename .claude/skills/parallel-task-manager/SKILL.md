---
name: parallel-task-manager
title: 并行任务管理器
description: 管理多个开发任务的并行执行，支持任务队列、优先级调度、资源限制、实时监控。
version: 1.0.0
author: Jarvis
tags: [task-management, parallelization, workflow, productivity]
---

# 并行任务管理器 Skill

## 功能概述

高效管理多个并行开发任务：
- 任务队列和优先级调度
- 资源限制和负载均衡
- 实时进度监控
- 任务依赖管理
- 失败重试和恢复

## 使用场景

- 同时处理 30+ 个开发窗口
- 大规模代码重构和测试
- 多分支并行开发
- CI/CD 流程优化
- 分布式任务执行

## 命令用法

### 1. 创建任务队列
```bash
parallel-task-manager create --name "refactor-sprint" --max-parallel 8
```

### 2. 添加任务
```bash
parallel-task-manager add --queue "refactor-sprint" --task "refactor src/components" --priority high
```

### 3. 启动执行
```bash
parallel-task-manager start --queue "refactor-sprint" --monitor
```

### 4. 监控进度
```bash
parallel-task-manager monitor --queue "refactor-sprint" --live
```

### 5. 查看统计
```bash
parallel-task-manager stats --queue "refactor-sprint"
```

## 配置

创建 `.parallel-task-config.json`：
```json
{
  "maxParallel": 8,
  "taskTimeout": 300,
  "retryAttempts": 3,
  "retryDelay": 5000,
  "resourceLimits": {
    "cpu": 80,
    "memory": 4096,
    "disk": 10240
  },
  "scheduling": "priority-fifo",
  "monitoring": true
}
```

## 工作原理

1. **任务入队** — 添加任务到队列，设置优先级和依赖
2. **调度** — 根据优先级和资源可用性调度任务
3. **执行** — 并行执行多个任务，监控资源使用
4. **监控** — 实时跟踪进度、错误和性能指标
5. **恢复** — 失败任务自动重试或手动干预

## 高级用法

### 任务依赖
```bash
parallel-task-manager add --queue "build" --task "compile" --id "compile-1"
parallel-task-manager add --queue "build" --task "test" --depends-on "compile-1"
```

### 动态调整并行度
```bash
parallel-task-manager adjust --queue "refactor-sprint" --max-parallel 12
```

### 任务分组
```bash
parallel-task-manager group --queue "refactor-sprint" --by "module" --parallel-per-group 2
```

### 条件执行
```bash
parallel-task-manager add --queue "ci" --task "deploy" --condition "all-tests-pass"
```

## 性能指标

- 支持并行任务：100+ 个
- 最大并行度：32+
- 任务切换开销：< 100ms
- 监控延迟：< 1s

## 监控指标

- **吞吐量** — 每分钟完成任务数
- **延迟** — 任务从入队到完成的时间
- **资源使用** — CPU、内存、磁盘占用
- **成功率** — 成功/失败/重试统计
- **瓶颈分析** — 识别慢任务和资源竞争

## 示例工作流

```bash
# 1. 创建队列
parallel-task-manager create --name "sprint" --max-parallel 8

# 2. 批量添加任务
for i in {1..50}; do
  parallel-task-manager add --queue "sprint" --task "refactor-module-$i"
done

# 3. 启动执行
parallel-task-manager start --queue "sprint" --monitor

# 4. 实时监控
parallel-task-manager monitor --queue "sprint" --live

# 5. 查看结果
parallel-task-manager stats --queue "sprint"
```

## 相关技能

- `efficient-git-workflow` — 高效代码提交
- `ai-code-generator` — AI 辅助代码生成
- `dev-efficiency-monitor` — 开发效率监控
