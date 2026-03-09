# 示例输入

## 场景1：创建周报生成 Skill

**用户输入**：
```
用 skill-generator 创建一个周报生成 Skill
```

**AI 会询问**：
- Skill 名称：weekly-report-generator
- 核心功能：自动整理本周工作内容，生成结构化周报
- 目标用户：需要定期写周报的职场人
- 输入格式：本周工作内容（任务、问题、计划）
- 输出格式：Markdown 格式的周报

---

## 场景2：创建代码审查 Skill

**用户输入**：
```
用 skill-generator 创建一个代码审查 Skill，
要求：
- 检查代码规范
- 发现性能问题
- 识别安全漏洞
- 输出问题列表和修改建议
```

**AI 会确认**：
- Skill 名称：code-reviewer
- 核心功能：自动审查代码，发现问题并提供建议
- 检查项：代码规范、性能、安全
- 输出格式：问题列表 + 修改建议

---

## 场景3：审查已有 Skill

**用户输入**：
```
用 skill-generator 审查 weekly-report-generator
```

**AI 会检查**：
- YAML 格式是否正确
- 指令是否清晰
- 是否有边界条件处理
- 是否有完整示例
- 提供改进建议

---

## 场景4：优化已有 Skill

**用户输入**：
```
用 skill-generator 优化 weekly-report-generator，
增加数据统计功能（工作时长、任务数量）
```

**AI 会**：
- 读取现有 Skill
- 添加数据统计功能
- 更新示例
- 说明改动内容
