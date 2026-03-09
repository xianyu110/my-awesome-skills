---
name: dev-efficiency-monitor
title: 开发效率监控器
description: 统计和分析开发效率指标，包括代码提交频率、质量、时间分布、瓶颈识别。
version: 1.0.0
author: Jarvis
tags: [monitoring, analytics, productivity, metrics]
---

# 开发效率监控器 Skill

## 功能概述

全方位监控开发效率：
- 代码提交统计和分析
- 开发时间分布
- 质量指标追踪
- 瓶颈识别和优化建议
- 团队效率对比

## 使用场景

- 个人效率分析
- 团队绩效评估
- 工作流优化
- 项目进度跟踪
- 资源分配优化

## 命令用法

### 1. 实时监控
```bash
dev-efficiency-monitor watch --author "Peter" --live
```

### 2. 统计分析
```bash
dev-efficiency-monitor stats --since "2026-02-01" --until "2026-02-28" --author "Peter"
```

### 3. 生成报告
```bash
dev-efficiency-monitor report --period "last-week" --format html --output report.html
```

### 4. 对比分析
```bash
dev-efficiency-monitor compare --authors "Peter,John" --metric "commits-per-day"
```

### 5. 瓶颈分析
```bash
dev-efficiency-monitor bottleneck --project "openclaw" --analyze
```

## 配置

创建 `.dev-monitor-config.json`：
```json
{
  "trackMetrics": ["commits", "lines", "files", "time", "quality"],
  "updateInterval": 60,
  "alertThresholds": {
    "commitsPerDay": 100,
    "linesPerCommit": 500,
    "errorRate": 0.05
  },
  "reportFormat": "html",
  "exportPath": "./reports"
}
```

## 监控指标

### 提交指标
- 提交次数（日/周/月）
- 提交时间分布
- 提交消息质量
- 提交大小分布

### 代码指标
- 代码行数变化
- 文件修改数量
- 代码复杂度
- 测试覆盖率

### 时间指标
- 开发时间分布
- 高峰时段识别
- 任务完成时间
- 响应延迟

### 质量指标
- Bug 率
- 代码审查通过率
- 测试通过率
- 重构频率

## 工作原理

1. **数据采集** — 从 Git、CI/CD、IDE 等收集数据
2. **数据处理** — 清洗、聚合、计算指标
3. **分析** — 趋势分析、异常检测、瓶颈识别
4. **可视化** — 生成图表和报告
5. **告警** — 超过阈值时发送通知

## 高级用法

### 自定义指标
```bash
dev-efficiency-monitor custom --metric "refactor-ratio" --formula "refactor-commits / total-commits"
```

### 趋势预测
```bash
dev-efficiency-monitor predict --metric "commits-per-day" --horizon 7
```

### 团队对比
```bash
dev-efficiency-monitor team --compare --metric "productivity" --period "last-month"
```

### 导出数据
```bash
dev-efficiency-monitor export --format json --output metrics.json
```

## 报告示例

```
开发效率报告 - Peter Steinberger
时间范围：2026-02-22 - 2026-02-23

📊 提交统计
- 总提交次数：627 次
- 平均每小时：26.1 次
- 峰值时段：21:00-22:00 (65 次)

📈 代码变化
- 新增代码：12,450 行
- 删除代码：8,320 行
- 净增长：4,130 行
- 修改文件：234 个

⏱️ 时间分布
- 工作时长：24 小时
- 高效时段：08:00-12:00, 20:00-24:00
- 平均提交间隔：2.3 分钟

✅ 质量指标
- 测试通过率：98.5%
- 代码审查通过率：100%
- Bug 率：0.2%

💡 优化建议
- 提交频率已达极限，建议增加自动化
- 21:00-22:00 时段效率最高，可安排重要任务
- 代码质量优秀，保持当前工作流
```

## 可视化

支持多种图表类型：
- 折线图（趋势）
- 柱状图（对比）
- 热力图（时间分布）
- 饼图（占比）
- 散点图（相关性）

## 告警规则

```json
{
  "alerts": [
    {
      "name": "高频提交",
      "condition": "commits_per_hour > 30",
      "action": "notify",
      "channel": "feishu"
    },
    {
      "name": "质量下降",
      "condition": "test_pass_rate < 0.95",
      "action": "block",
      "severity": "high"
    }
  ]
}
```

## 示例工作流

```bash
# 1. 启动实时监控
dev-efficiency-monitor watch --live &

# 2. 查看今日统计
dev-efficiency-monitor stats --today

# 3. 生成周报
dev-efficiency-monitor report --period "last-week" --format html

# 4. 识别瓶颈
dev-efficiency-monitor bottleneck --analyze

# 5. 导出数据
dev-efficiency-monitor export --format json
```

## 集成

支持与以下工具集成：
- Git / GitHub / GitLab
- CI/CD (Jenkins, GitHub Actions)
- IDE (VS Code, IntelliJ)
- 项目管理 (Jira, Trello)
- 通知 (Slack, 飞书, 邮件)

## 相关技能

- `efficient-git-workflow` — 高效代码提交
- `parallel-task-manager` — 并行任务管理
- `ai-code-generator` — AI 辅助代码生成
