# 上传到 skills.sh 指南

## 📦 准备工作

### 1. 确保文件结构完整

```
bananapro-image-gen/
├── skill.json              # Skill 元数据（必需）
├── README.md               # 快速开始文档（必需）
├── SKILL.md                # 详细文档（推荐）
├── requirements.txt        # Python 依赖（必需）
├── .gitignore             # Git 忽略文件
├── scripts/
│   └── generate_image.py  # 主脚本
└── test_output/           # 测试输出（可选）
```

### 2. 检查必需文件

- ✅ `skill.json` - Skill 元数据
- ✅ `README.md` - 快速开始
- ✅ `SKILL.md` - 详细文档
- ✅ `requirements.txt` - 依赖列表
- ✅ `scripts/generate_image.py` - 主脚本

## 🚀 上传步骤

### 方式1：通过 GitHub（推荐）

#### 步骤1：创建独立仓库

```bash
# 1. 在 GitHub 创建新仓库
# 仓库名：bananapro-image-gen-skill

# 2. 复制 skill 到新仓库
cd /path/to/new/repo
cp -r /path/to/.claude/.skills/bananapro-image-gen/* .

# 3. 初始化 Git
git init
git add .
git commit -m "Initial commit: Banana Pro Image Generation Skill"

# 4. 推送到 GitHub
git remote add origin https://github.com/xianyu110/bananapro-image-gen-skill.git
git branch -M main
git push -u origin main
```

#### 步骤2：在 skills.sh 提交

1. 访问 https://skills.sh/
2. 点击 "Submit a Skill" 或 "Add Skill"
3. 填写表单：
   - **Skill Name**: bananapro-image-gen
   - **Display Name**: Banana Pro Image Generation
   - **GitHub URL**: https://github.com/xianyu110/bananapro-image-gen-skill
   - **Description**: 使用 Gemini 3 Pro Image 生成图片的 OpenClaw Skill
   - **Category**: Creativity
   - **Tags**: ai, image, generation, gemini, creative

4. 提交审核

### 方式2：通过 CLI（如果支持）

```bash
# 安装 OpenClaw CLI（如果有）
npm install -g @openclaw/cli

# 登录
openclaw login

# 发布 Skill
cd .claude/.skills/bananapro-image-gen
openclaw publish
```

### 方式3：通过 Pull Request

如果 skills.sh 使用 GitHub 仓库管理：

```bash
# 1. Fork skills.sh 的仓库
# 2. 克隆你的 fork
git clone https://github.com/YOUR_USERNAME/skills-repo.git

# 3. 添加你的 skill
cd skills-repo/skills
cp -r /path/to/bananapro-image-gen .

# 4. 提交 PR
git add bananapro-image-gen
git commit -m "Add: Banana Pro Image Generation Skill"
git push origin main

# 5. 在 GitHub 创建 Pull Request
```

## 📝 提交信息模板

### Skill 描述

```
Banana Pro Image Generation - AI 图片生成 Skill

使用 Gemini 3 Pro Image 模型生成各种风格的图片，特别擅长：
- 📝 白板图：手写风格的概念图、流程图
- 🎨 创意设计：Logo、海报、社交媒体配图
- 📊 图表生成：对比表格、架构图、思维导图

特点：
✅ 支持中文提示词
✅ 多种分辨率（1K/2K/4K）
✅ 快速响应（10-30秒）
✅ 成本低廉（$0.04-0.16/张）

适用场景：
- 教程配图
- 产品设计
- 内容创作
- 知识可视化
```

### 标签建议

```
ai, image-generation, gemini, creative, whiteboard, logo-design, 
text-to-image, visualization, diagram, concept-art
```

## ✅ 发布前检查清单

- [ ] `skill.json` 信息完整准确
- [ ] `README.md` 包含快速开始示例
- [ ] `SKILL.md` 包含详细文档
- [ ] `requirements.txt` 列出所有依赖
- [ ] 代码中移除了敏感信息（API Key等）
- [ ] 测试脚本可以正常运行
- [ ] 添加了 `.gitignore` 文件
- [ ] 添加了 LICENSE 文件（MIT）
- [ ] 所有示例都经过测试
- [ ] 文档中的链接都有效

## 🔒 安全注意事项

### 移除敏感信息

在上传前，确保移除所有敏感信息：

```python
# ❌ 不要硬编码 API Key
API_KEY = "sk-YOUR_API_KEY_HERE"

# ✅ 使用环境变量
API_KEY = os.getenv("NEXTAI_API_KEY", "")
```

### 更新文档

在 README.md 中说明如何配置 API Key：

```markdown
## 配置

### 设置 API Key

```bash
export KEY=xxx
```

或在 `~/.openclaw/openclaw.json` 中配置：

```json
{
  "skills": {
    "bananapro-image-gen": {
      "apiKey": "your-api-key-here"
    }
  }
}
```
```

## 📊 发布后

### 1. 监控反馈

- 关注 GitHub Issues
- 回复用户问题
- 收集改进建议

### 2. 持续更新

- 修复 Bug
- 添加新功能
- 更新文档
- 发布新版本

### 3. 推广

- 在社交媒体分享
- 写博客文章
- 录制演示视频
- 参与社区讨论

## 🔗 相关链接

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [Skills 开发指南](https://docs.openclaw.ai/skills)
- [Skills 市场](https://skills.sh)
- [示例 Skills](https://github.com/openclaw/skills)

## 💡 提示

1. **清晰的文档**：好的文档是 Skill 成功的关键
2. **实用的示例**：提供多个真实场景的示例
3. **及时的支持**：快速响应用户问题
4. **持续改进**：根据反馈不断优化

## 📮 需要帮助？

- GitHub Issues: https://github.com/xianyu110/awesome-openclaw-tutorial/issues
- 社区讨论: https://community.openclaw.ai
- 邮件: your-email@example.com

---

**祝你的 Skill 发布成功！** 🎉
