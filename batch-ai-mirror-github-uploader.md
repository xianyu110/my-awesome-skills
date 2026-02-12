# Batch AI Mirror Site Generator & GitHub Uploader Skill

## Skill Name
批量生成AI镜像站介绍并上传到GitHub

## Skill Description
自动批量为多个AI工具（ChatGPT、Claude、Gemini、Grok、DeepSeek等）生成镜像站使用指南，并自动创建独立的GitHub仓库上传。

## Skill Category
- 内容生成
- 自动化部署
- GitHub仓库管理

## Prerequisites
- GitHub 账号和访问令牌（Personal Access Token）
- 本地已安装 git
- curl 命令可用
- AI镜像站链接（主入口 + 导航入口）

## Input Parameters

### Required
1. **ai_tools_list**: AI工具名称列表
   - 示例：`["chatgpt-gpt4o", "claude-35-sonnet", "gemini-25-pro", "grok-3", "deepseek-v3"]`

2. **github_token**: GitHub Personal Access Token
   - 格式：`ghp_xxxxxxxxxxxxxxxxxxxx`

3. **github_username**: GitHub 用户名
   - 示例：`glpfive25-cyber`

4. **mirror_main_url**: 主镜像站入口
   - 示例：`https://claudeapp.asia/list/#/home`

5. **mirror_nav_url**: 镜像导航入口
   - 示例：`https://chatgpt-plus.top/`

### Optional
6. **base_directory**: 本地工作目录
   - 默认：`/Users/username/Downloads/cursor编程`

7. **content_language**: 内容语言
   - 默认：`zh-CN`（中文）

## Output
- 为每个AI工具创建独立目录
- 生成 README.md（使用指南）
- 生成 index.html（网页版本）
- 创建 GitHub 仓库并推送代码
- 返回所有仓库的 URL 列表

## Step-by-Step Process

### Step 1: 准备工作目录
```bash
cd {base_directory}
mkdir -p ai-mirror-repos
cd ai-mirror-repos
```

### Step 2: 批量生成内容
对每个 AI 工具：
1. 创建 `{tool_name}-mirror` 目录
2. 根据 AI 工具特点生成定制化的 README.md
3. 生成对应的 index.html

### Step 3: Git 初始化
对每个目录：
```bash
git init
git add .
git commit -m "Initial commit: AI mirror site guide"
git branch -M main
```

### Step 4: 创建 GitHub 仓库
使用 GitHub API：
```bash
curl -X POST \
  -H "Authorization: token {github_token}" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos \
  -d '{"name":"{repo_name}","private":false}'
```

### Step 5: 推送到 GitHub
```bash
git remote add origin "https://{github_token}@github.com/{github_username}/{repo_name}.git"
git push -u origin main
```

### Step 6: 返回结果
返回所有创建的仓库 URL 列表

## AI Tools Template Structure

### ChatGPT 系列 (OpenAI)
**已发布：**
- chatgpt-gpt5.2-mirror (2025年12月最新)
- chatgpt-gpt5.1-mirror (2025年11月)
- chatgpt-gpt4o-mirror
- chatgpt-o1-preview-mirror

**预测未发布：**
- chatgpt-gpt6-mirror (预计2026年Q2)
- chatgpt-gpt5.3-turbo-mirror (预计2025年Q1)
- chatgpt-o5-mirror (预计2025年Q2，超级推理模型)
- chatgpt-gpt5-vision-pro-mirror (预计2025年Q2)

**核心特点：** GPT-5.2编码能力突破、多模态、o3/o4-mini推理模型

### Claude 系列 (Anthropic)
**已发布：**
- claude-opus-4.5-mirror (2025年11月最新，编码最强)
- claude-4-opus-mirror
- claude-4-sonnet-mirror
- claude-35-sonnet-mirror

**预测未发布：**
- claude-5-opus-mirror (预计2025年Q3)
- claude-5-sonnet-mirror (预计2025年Q2)
- claude-4.7-haiku-mirror (预计2025年Q1，超快速版)
- claude-opus-5-extended-mirror (预计2025年Q4，500K上下文)

**核心特点：** SWE-bench编码80.9%第一、200K上下文、混合架构即时响应

### Gemini 系列 (Google)
**已发布：**
- gemini-3-pro-mirror (2025年11月最新)
- gemini-3-flash-mirror (新默认模型)
- gemini-3-deep-think-mirror (高级推理)
- gemini-25-pro-mirror
- gemini-20-flash-mirror

**预测未发布：**
- gemini-4-ultra-mirror (预计2026年Q1)
- gemini-3.5-pro-mirror (预计2025年Q2)
- gemini-3-nano-mirror (预计2025年Q1，端侧模型)
- gemini-3-code-mirror (预计2025年Q2，专注编程)

**核心特点：** 100万token上下文、数学AIME 95%、多模态、中文优化

### Grok 系列 (xAI)
**已发布：**
- grok-4.1-mirror (2025年最新)
- grok-3-mirror
- grok-4-standard-mirror

**预测未发布：**
- grok-5-mirror (预计2025年Q3)
- grok-4.5-turbo-mirror (预计2025年Q2)
- grok-vision-pro-mirror (预计2025年Q2，视觉增强)
- grok-realtime-plus-mirror (预计2025年Q1，实时增强)

**核心特点：** 实时信息、X平台集成、Think推理模式、幽默风格

### DeepSeek 系列 (国产)
**已发布：**
- deepseek-v3.2-mirror (2025年最新)
- deepseek-v3-mirror

**预测未发布：**
- deepseek-v4-mirror (预计2025年Q2)
- deepseek-coder-v3-mirror (预计2025年Q1，专注编程)
- deepseek-math-pro-mirror (预计2025年Q2，数学专精)
- deepseek-v3.5-lite-mirror (预计2025年Q1，轻量版)

**核心特点：** 开源、性价比最高、数学推理、代码能力强

### Meta Llama 系列 (开源)
**已发布：**
- llama-4-mirror (2025年)
- llama-3.3-mirror

**预测未发布：**
- llama-5-mirror (预计2025年Q4)
- llama-4.5-vision-mirror (预计2025年Q3)
- llama-4-code-mirror (预计2025年Q2)

**核心特点：** 完全开源、社区驱动、本地部署友好

### Mistral 系列 (欧洲)
**已发布：**
- mistral-large-2-mirror
- mistral-medium-mirror

**预测未发布：**
- mistral-ultra-mirror (预计2025年Q3)
- mistral-large-3-mirror (预计2025年Q2)
- mistral-code-pro-mirror (预计2025年Q2)

**核心特点：** 欧洲隐私标准、多语言、企业级

## Content Template Structure

每个 README.md 包含：

```markdown
# {AI工具名称}官网镜像站使用指南（国内直连）

## ✅ 精选入口
- 主入口：{mirror_main_url}
- 镜像导航：{mirror_nav_url}

## 📋 目录导航
- 什么是 {AI工具}？
- 为什么选择镜像网站？
- 精选镜像站推荐
- 核心优势与功能
- 快速开始使用
- 官网与镜像站对比
- 核心功能详解
- 常见问题FAQ
- 隐私安全建议
- 总结与行动建议

## {AI工具特定内容}
- 核心优势（3-5点）
- 使用场景
- 技术特点
- 版本对比

## 安全建议
- ❌ 不建议输入的信息
- ✅ 适合的使用场景
- 实用安全习惯
```

## Error Handling

### 网络错误
- 重试机制（最多3次）
- 超时设置（60秒）

### GitHub API 错误
- 仓库已存在：跳过创建，直接推送
- 认证失败：提示检查 token
- 限流：等待后重试

### Git 错误
- 远程已存在：先删除后添加
- 推送失败：检查认证和网络

## Success Criteria
- ✅ 所有目录创建成功
- ✅ 内容生成完整且准确
- ✅ GitHub 仓库全部创建
- ✅ 代码全部推送成功
- ✅ 返回完整的 URL 列表

## Usage Example

### 命令示例
```
批量生成以下AI工具的镜像站指南并上传到GitHub（2025年最新版本）：
- chatgpt-gpt5.2-mirror
- claude-opus-4.5-mirror
- gemini-3-pro-mirror
- grok-4.1-mirror
- deepseek-v3.2-mirror

GitHub用户名：glpfive25-cyber
GitHub Token：ghp_YOUR_GITHUB_TOKEN_HERE
主入口：https://geminiai.asia/list/#/home
副入口：https://claudeapp.asia/list/#/home
导航入口：https://chatgpt-plus.top/
```

### 预期输出
```
✅ 已创建 5 个仓库（2025最新模型）：

1. https://github.com/glpfive25-cyber/chatgpt-gpt5.2-mirror
2. https://github.com/glpfive25-cyber/claude-opus-4.5-mirror
3. https://github.com/glpfive25-cyber/gemini-3-pro-mirror
4. https://github.com/glpfive25-cyber/grok-4.1-mirror
5. https://github.com/glpfive25-cyber/deepseek-v3.2-mirror

所有内容已生成并推送成功！
```

## Advanced Features

### 1. 内容定制化
- 根据AI工具类型自动调整内容重点
- 突出各工具的独特优势
- 生成针对性的使用示例

### 2. 批量操作优化
- 并行创建仓库（API调用）
- 串行推送代码（避免冲突）
- 进度显示

### 3. 版本控制
- 自动生成 .gitignore
- 标准化的 commit message
- 分支管理（默认 main）

### 4. 内容验证
- 检查链接有效性
- 验证 Markdown 格式
- HTML 语法检查

## Maintenance & Updates

### 定期更新
- AI工具版本更新
- 镜像链接更新
- 功能特性更新

### 扩展性
- 支持添加新的AI工具
- 支持自定义模板
- 支持多语言版本

## Security Notes

### Token 安全
- ⚠️ 不要在代码中硬编码 token
- ⚠️ 不要提交 token 到版本控制
- ⚠️ 定期轮换 token
- ✅ 使用环境变量存储

### 内容安全
- 避免包含敏感信息
- 遵守各平台使用条款
- 尊重知识产权

## Performance Metrics

### 预期性能
- 单个仓库创建：5-10秒
- 10个仓库总时间：约2-3分钟
- 成功率：>95%

### 优化建议
- 使用 GitHub API 批量创建
- 复用内容模板
- 缓存已生成内容

## Troubleshooting

### 常见问题

**Q: 仓库已存在怎么办？**
A: 跳过创建步骤，直接推送更新

**Q: Push 失败怎么办？**
A: 检查 token 权限、仓库可见性、网络连接

**Q: 内容重复怎么办？**
A: 为每个工具定制化内容，突出差异点

**Q: 批量操作中断怎么办？**
A: 记录已完成的仓库，从中断点继续

## Related Skills
- GitHub 仓库管理
- 内容批量生成
- API 自动化调用
- Markdown 文档生成

## Tags
`github-automation` `batch-processing` `ai-tools` `content-generation` `mirror-sites` `devops` `repository-management`
