---
name: skill-generator
description: 专门用来创建、优化、审查其他 Claude Skills 的 Meta-skill。自动生成完整的 Skill 文件结构，包括 YAML frontmatter、指令、示例等。
---

# Skill Generator - Meta-skill

## 功能
帮助用户快速创建高质量的 Claude Skills，自动生成完整的文件结构和内容。

## 使用方式
用户说："用 skill-generator 创建一个 [功能描述] Skill"

## 执行步骤

### Step 1: 理解需求
询问用户以下信息（如果用户已提供则跳过）：
- **Skill 名称**：kebab-case 格式（如 weekly-report-generator）
- **核心功能**：这个 Skill 要做什么
- **目标用户**：谁会使用这个 Skill
- **输入输出**：需要什么输入，产出什么输出
- **特殊要求**：是否有特定的格式、规范、边界条件

### Step 2: 生成 Skill 文件结构
创建以下文件结构：
```
~/.claude/skills/[skill-name]/
├── SKILL.md          # 核心指令文件
├── README.md         # 使用说明
└── examples/         # 示例文件夹
    ├── example-input.md
    └── example-output.md
```

### Step 3: 生成 SKILL.md 内容

**必须包含的部分**：

#### 3.1 YAML Frontmatter
```yaml
---
name: [skill-name]
description: [简短描述，说明功能和使用场景，最多1024字符]
---
```

#### 3.2 功能说明
```markdown
# [Skill 标题]

## 功能
[详细说明这个 Skill 的功能]

## 使用方式
用户说："用 [skill-name] [具体任务]"
```

#### 3.3 执行步骤
```markdown
## 执行步骤

### Step 1: [步骤名称]
[详细说明]
- 输入要求
- 处理逻辑
- 输出格式

### Step 2: [步骤名称]
[详细说明]

[继续添加步骤...]
```

#### 3.4 输出格式
```markdown
## 输出格式
[明确说明输出的格式、结构、示例]
```

#### 3.5 边界条件处理
```markdown
## 边界条件
- 如果 [情况A]，则 [处理方式]
- 如果 [情况B]，则 [处理方式]
```

#### 3.6 示例
```markdown
## 示例

### 输入
[示例输入]

### 输出
[示例输出]
```

### Step 4: 生成 README.md
包含：
- Skill 简介
- 安装方式
- 使用示例
- 常见问题

### Step 5: 生成示例文件
在 `examples/` 文件夹中创建：
- `example-input.md`：示例输入
- `example-output.md`：示例输出

### Step 6: 验证和优化
检查：
- ✅ YAML 格式正确（name 和 description 必填）
- ✅ 指令清晰明确，分步骤执行
- ✅ 包含边界条件处理
- ✅ 有完整的示例
- ✅ 输出格式明确

### Step 7: 输出结果
生成完成后，输出：
```
✅ Skill 已创建：~/.claude/skills/[skill-name]/

文件清单：
- SKILL.md（核心指令文件）
- README.md（使用说明）
- examples/example-input.md
- examples/example-output.md

使用方式：
"用 [skill-name] [具体任务]"

下一步：
1. 重启 Claude Code 或刷新网页
2. 测试 Skill 是否正常工作
3. 根据实际使用调整优化
```

## 质量标准

### YAML Frontmatter 规范
- `name`：必填，kebab-case 格式，最多64字符
- `description`：必填，说明功能和使用场景，最多1024字符

### 指令编写规范
- **清晰性**：每个步骤都要说明输入、处理、输出
- **完整性**：包含所有必要的边界条件处理
- **可测试性**：提供完整的示例，方便测试
- **可维护性**：结构清晰，易于后续修改

### 常见模式

#### 模式1：数据处理类 Skill
```markdown
## 执行步骤
### Step 1: 验证输入
- 检查数据格式
- 验证必填字段

### Step 2: 数据处理
- 清洗数据
- 转换格式

### Step 3: 输出结果
- 按指定格式输出
- 添加统计信息
```

#### 模式2：内容生成类 Skill
```markdown
## 执行步骤
### Step 1: 理解需求
- 询问必要信息
- 确认输出格式

### Step 2: 生成内容
- 按模板生成
- 保持风格一致

### Step 3: 审校优化
- 检查格式
- 优化表达
```

#### 模式3：代码审查类 Skill
```markdown
## 执行步骤
### Step 1: 读取代码
- 理解代码结构
- 识别关键部分

### Step 2: 检查问题
- 代码规范
- 性能问题
- 安全漏洞

### Step 3: 输出报告
- 问题列表
- 修改建议
```

## 边界条件

### 如果用户提供的信息不完整
- 主动询问缺失的信息
- 不要假设或猜测

### 如果 Skill 名称不符合规范
- 提示用户使用 kebab-case 格式
- 建议合适的名称

### 如果功能描述过于复杂
- 建议拆分成多个 Skills
- 或者创建一个 Agent（包含多个子 Skills）

### 如果需要外部依赖
- 在 README.md 中说明依赖
- 提供安装指南

## 高级功能

### 审查已有 Skill
用户说："用 skill-generator 审查 [skill-name]"

执行：
1. 读取现有 Skill 文件
2. 检查是否符合质量标准
3. 提供改进建议
4. 可选：自动优化

### 优化已有 Skill
用户说："用 skill-generator 优化 [skill-name]"

执行：
1. 读取现有 Skill 文件
2. 识别可优化的地方
3. 生成优化后的版本
4. 说明改动内容

## 示例

### 示例1：创建周报生成 Skill

**用户输入**：
```
用 skill-generator 创建一个周报生成 Skill
```

**AI 响应**：
```
收到！让我了解一下需求。

【需要确认的信息】
1. Skill 名称建议：weekly-report-generator
2. 核心功能：自动整理本周工作内容，生成结构化周报
3. 目标用户：需要定期写周报的职场人
4. 输入：本周工作内容（任务、问题、计划）
5. 输出：Markdown 格式的周报

这样可以吗？或者有其他要求？
```

**用户确认后**：
```
好的！开始生成...

✅ Skill 已创建：~/.claude/skills/weekly-report-generator/

文件清单：
- SKILL.md（核心指令文件）
- README.md（使用说明）
- examples/example-input.md
- examples/example-output.md

使用方式：
"用 weekly-report-generator 生成本周周报"

下一步：
1. 重启 Claude Code 或刷新网页
2. 测试：说"用 weekly-report-generator 生成本周周报"
3. 根据实际使用调整优化
```

### 示例2：审查已有 Skill

**用户输入**：
```
用 skill-generator 审查 weekly-report-generator
```

**AI 响应**：
```
正在审查 weekly-report-generator...

【审查结果】

✅ 通过的检查：
- YAML 格式正确
- 有清晰的执行步骤
- 包含示例

⚠️ 需要改进：
1. 缺少边界条件处理
   - 建议：添加"如果用户没有提供工作内容"的处理
2. 输出格式不够明确
   - 建议：提供更详细的输出模板
3. 缺少数据统计功能
   - 建议：添加工作时长、任务数量统计

是否需要我自动优化？
```

## 注意事项

### 不要过度复杂化
- 保持 Skill 功能单一、清晰
- 如果功能太复杂，建议拆分

### 遵循最佳实践
- 使用 kebab-case 命名
- YAML frontmatter 必须正确
- 提供完整的示例

### 测试很重要
- 生成后一定要测试
- 根据实际使用调整
- 迭代优化

## 总结

这个 Meta-skill 可以帮你：
- ✅ 快速创建高质量 Skills（2-5分钟）
- ✅ 自动生成完整文件结构
- ✅ 遵循最佳实践和规范
- ✅ 审查和优化已有 Skills

**效率提升：10倍起步！**
