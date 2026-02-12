# 示例输出

## 场景1：创建周报生成 Skill

**AI 输出**：
```
✅ Skill 已创建：~/.claude/skills/weekly-report-generator/

文件清单：
- SKILL.md（核心指令文件）
- README.md（使用说明）
- examples/example-input.md
- examples/example-output.md

Skill 内容预览：
---
name: weekly-report-generator
description: 自动整理本周工作内容，生成结构化周报，包含完成任务、遇到问题、下周计划和数据统计
---

# 周报生成器

## 功能
自动整理本周工作内容，生成结构化周报

## 使用方式
用户说："用 weekly-report-generator 生成本周周报"

## 执行步骤
[详细步骤...]

使用方式：
"用 weekly-report-generator 生成本周周报"

下一步：
1. 重启 Claude Code 或刷新网页
2. 测试：说"用 weekly-report-generator 生成本周周报"
3. 根据实际使用调整优化
```

---

## 场景2：创建代码审查 Skill

**AI 输出**：
```
✅ Skill 已创建：~/.claude/skills/code-reviewer/

文件清单：
- SKILL.md（核心指令文件）
- README.md（使用说明）
- examples/example-input.md（示例代码）
- examples/example-output.md（审查报告示例）

Skill 内容预览：
---
name: code-reviewer
description: 自动审查代码，检查代码规范、性能问题、安全漏洞，输出问题列表和修改建议
---

# 代码审查助手

## 功能
自动审查代码，发现问题并提供修改建议

## 检查项
- 代码规范
- 性能问题
- 安全漏洞

[详细内容...]

使用方式：
"用 code-reviewer 审查这段代码"

下一步：
1. 重启 Claude Code 或刷新网页
2. 测试：提供一段代码，说"用 code-reviewer 审查这段代码"
3. 根据实际使用调整优化
```

---

## 场景3：审查已有 Skill

**AI 输出**：
```
正在审查 weekly-report-generator...

【审查结果】

✅ 通过的检查：
- YAML 格式正确
  - name: weekly-report-generator ✓
  - description: 完整且清晰 ✓
- 有清晰的执行步骤（5个步骤）
- 包含示例文件

⚠️ 需要改进的地方：

1. 边界条件处理不完整
   当前：只处理了"用户没有提供工作内容"的情况
   建议：添加以下边界条件
   - 如果工作内容格式不规范
   - 如果任务数量为0
   - 如果时间跨度不是一周

2. 输出格式可以更明确
   当前：只说明"Markdown 格式"
   建议：提供详细的输出模板，包括：
   - 标题格式
   - 各部分的顺序
   - 数据统计的展示方式

3. 缺少数据验证
   建议：添加输入数据验证步骤
   - 验证日期格式
   - 验证必填字段
   - 验证数据类型

【改进建议优先级】
🔴 高优先级：边界条件处理（影响稳定性）
🟡 中优先级：输出格式明确（影响用户体验）
🟢 低优先级：数据验证（锦上添花）

是否需要我自动优化？
回复"是"我会生成优化后的版本。
```

---

## 场景4：优化已有 Skill

**AI 输出**：
```
正在优化 weekly-report-generator...

【优化内容】

1. 添加数据统计功能
   - 总工作时长统计
   - 完成任务数量统计
   - 问题解决数量统计

2. 改进的部分：
   ✅ 在 Step 4 添加数据统计步骤
   ✅ 更新输出格式，包含统计信息
   ✅ 更新示例，展示统计数据

3. 新增内容预览：
```markdown
## 数据统计
- 总工作时长：17小时
- 完成任务数：4个
- 解决问题数：1个
- 平均每任务耗时：4.25小时
```

【文件变更】
- SKILL.md：添加数据统计步骤
- examples/example-output.md：更新示例

✅ 优化完成！

使用方式：
"用 weekly-report-generator 生成本周周报"

新功能会自动包含数据统计。
```

---

## 总结

使用 skill-generator 可以：
- ✅ 2-5分钟创建完整 Skill
- ✅ 自动生成规范的文件结构
- ✅ 审查和优化已有 Skills
- ✅ 遵循最佳实践

**效率提升：10倍起步！**
