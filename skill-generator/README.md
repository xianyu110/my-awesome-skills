# Skill Generator - Meta-skill

一个专门用来创建、优化、审查其他 Claude Skills 的 Meta-skill。

## 特点

- ✅ **快速创建**：2-5分钟生成完整 Skill
- ✅ **自动化**：自动生成文件结构、YAML、示例
- ✅ **高质量**：遵循最佳实践和规范
- ✅ **可审查**：可以审查和优化已有 Skills

## 安装

这个 Skill 已经在你的 `~/.claude/skills/skill-generator/` 目录中。

重启 Claude Code 或刷新网页即可使用。

## 使用方式

### 创建新 Skill

```
用 skill-generator 创建一个 [功能描述] Skill
```

**示例**：
```
用 skill-generator 创建一个周报生成 Skill
用 skill-generator 创建一个代码审查 Skill
用 skill-generator 创建一个会议纪要整理 Skill
```

### 审查已有 Skill

```
用 skill-generator 审查 [skill-name]
```

**示例**：
```
用 skill-generator 审查 weekly-report-generator
```

### 优化已有 Skill

```
用 skill-generator 优化 [skill-name]
```

**示例**：
```
用 skill-generator 优化 weekly-report-generator
```

## 生成的文件结构

```
~/.claude/skills/[skill-name]/
├── SKILL.md          # 核心指令文件
├── README.md         # 使用说明
└── examples/         # 示例文件夹
    ├── example-input.md
    └── example-output.md
```

## 质量保证

生成的 Skill 会自动包含：
- ✅ 正确的 YAML frontmatter
- ✅ 清晰的执行步骤
- ✅ 边界条件处理
- ✅ 完整的示例
- ✅ 明确的输出格式

## 常见问题

### Q: 生成的 Skill 可以直接使用吗？
A: 可以！生成后重启 Claude Code 或刷新网页即可使用。建议先测试，根据实际使用调整。

### Q: 可以修改生成的 Skill 吗？
A: 当然可以！生成的文件都是 Markdown 格式，可以直接编辑。

### Q: 如何删除不需要的 Skill？
A: 直接删除 `~/.claude/skills/[skill-name]/` 文件夹即可。

### Q: 可以创建多少个 Skills？
A: 没有限制！想创建多少就创建多少。

### Q: 生成的 Skill 质量如何？
A: 遵循 Anthropic 官方最佳实践，质量有保证。但建议根据实际使用调整优化。

## 最佳实践

### 1. 保持功能单一
- 一个 Skill 只做一件事
- 如果功能太复杂，拆分成多个 Skills

### 2. 提供清晰的示例
- 示例要完整、真实
- 覆盖常见使用场景

### 3. 处理边界条件
- 考虑各种异常情况
- 提供友好的错误提示

### 4. 定期优化
- 根据实际使用调整
- 收集用户反馈
- 持续改进

## 效率对比

| 方式 | 耗时 | 质量 |
|------|------|------|
| 手动创建 | 30-60分钟 | 看个人水平 |
| 用 skill-generator | 2-5分钟 | 遵循最佳实践 |

**效率提升：10倍起步！**

## 相关资源

- [Claude Skills 官方文档](https://docs.anthropic.com/skills)
- [Skills Marketplace](https://skillsmp.com/)
- [Anthropic 工程博客](https://www.anthropic.com/engineering)

## 许可

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
