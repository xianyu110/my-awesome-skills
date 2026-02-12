# AI Mirror Site Publisher - 一键生成图文并茂的镜像站指南并发布到GitHub

## 技能名称
AI镜像站图文指南一键发布器

## 技能描述
整合配图生成和内容创作，一键批量为多个AI工具（ChatGPT、Claude、Gemini、Grok、DeepSeek等）生成图文并茂的镜像站使用指南，并自动创建GitHub仓库发布。

## 核心特性
- ✅ **图文并茂**：自动生成6张专业配图（封面/概念/流程/对比/场景/FAQ）
- ✅ **批量处理**：一次命令处理多个AI工具
- ✅ **内容定制**：根据AI工具特点自动调整内容重点
- ✅ **自动部署**：创建GitHub仓库并推送代码
- ✅ **最新版本**：支持2025年最新AI模型版本

## 技能分类
- 内容生成
- 图片生成
- 自动化部署
- GitHub仓库管理

## 前置条件
- GitHub 账号和 Personal Access Token
- 本地已安装 git
- curl 命令可用
- bun 运行环境
- Z-Image API Key（可选，有默认值）

## 输入参数

### 必需参数
1. **ai_tools**: AI工具列表
   - 格式：逗号分隔的字符串
   - 示例：`"chatgpt-gpt5.2,claude-opus-4.5,gemini-3-pro"`

2. **github_username**: GitHub 用户名
   - 示例：`glpfive25-cyber`

3. **github_token**: GitHub Personal Access Token
   - 格式：`ghp_xxxxxxxxxxxxxxxxxxxx`

4. **mirror_main_url**: 主镜像站入口
   - 示例：`https://geminiai.asia/list/#/home`

5. **mirror_nav_url**: 镜像导航入口
   - 示例：`https://chatgpt-plus.top/`

### 可选参数
6. **mirror_secondary_url**: 备用镜像站入口
   - 示例：`https://claudeapp.asia/list/#/home`

7. **image_count**: 每个工具生成的图片数量
   - 默认：`6`

8. **image_style**: 配图风格
   - 可选：`notion`, `tech`, `minimal`, `warm`, `playful`
   - 默认：`notion`

9. **base_directory**: 本地工作目录
   - 默认：`./ai-mirror-repos`

10. **zimage_api_key**: Z-Image API Key
    - 默认：使用内置key

## 输出结果
- 为每个AI工具创建独立目录
- 生成 6 张专业配图
- 生成 README.md（图文并茂的使用指南）
- 生成 index.html（网页版本）
- 创建 GitHub 仓库并推送
- 返回所有仓库的 URL 列表

## 支持的AI工具

### ChatGPT 系列 (OpenAI)
**已发布：**
- `chatgpt-gpt5.2` - GPT-5.2 (2025年12月最新)
- `chatgpt-gpt5.1` - GPT-5.1 (2025年11月)
- `chatgpt-gpt4o` - GPT-4o
- `chatgpt-o1-preview` - O1 Preview

**预测未发布：**
- `chatgpt-gpt6` - GPT-6 (预计2026年Q2)
- `chatgpt-o5` - O5 超级推理模型 (预计2025年Q2)

### Claude 系列 (Anthropic)
**已发布：**
- `claude-opus-4.5` - Opus 4.5 (2025年11月，编码最强)
- `claude-4-opus` - Claude 4 Opus
- `claude-35-sonnet` - Claude 3.5 Sonnet

**预测未发布：**
- `claude-5-opus` - Claude 5 Opus (预计2025年Q3)
- `claude-5-sonnet` - Claude 5 Sonnet (预计2025年Q2)

### Gemini 系列 (Google)
**已发布：**
- `gemini-3-pro` - Gemini 3 Pro (2025年11月最新)
- `gemini-3-flash` - Gemini 3 Flash
- `gemini-3-deep-think` - Gemini 3 Deep Think
- `gemini-25-pro` - Gemini 2.5 Pro

**预测未发布：**
- `gemini-4-ultra` - Gemini 4 Ultra (预计2026年Q1)
- `gemini-3-code` - Gemini 3 Code (预计2025年Q2)

### Grok 系列 (xAI)
**已发布：**
- `grok-4.1` - Grok 4.1 (2025年最新)
- `grok-3` - Grok 3
- `grok-4-standard` - Grok 4 Standard

**预测未发布：**
- `grok-5` - Grok 5 (预计2025年Q3)
- `grok-vision-pro` - Grok Vision Pro (预计2025年Q2)

### DeepSeek 系列 (国产)
**已发布：**
- `deepseek-v3.2` - DeepSeek v3.2 (2025年最新)
- `deepseek-v3` - DeepSeek v3

**预测未发布：**
- `deepseek-v4` - DeepSeek v4 (预计2025年Q2)
- `deepseek-coder-v3` - DeepSeek Coder v3 (预计2025年Q1)

### 其他系列
- `llama-4` - Meta Llama 4
- `mistral-large-2` - Mistral Large 2

## 快速开始

### 基础用法

```bash
# 为3个AI工具生成指南并发布
bun .claude/skills/ai-mirror-publisher/scripts/publish.ts \
  --tools "chatgpt-gpt5.2,claude-opus-4.5,gemini-3-pro" \
  --github-user "glpfive25-cyber" \
  --github-token "ghp_xxx" \
  --main-url "https://geminiai.asia/list/#/home" \
  --nav-url "https://chatgpt-plus.top/"
```

### 完整参数示例

```bash
bun .claude/skills/ai-mirror-publisher/scripts/publish.ts \
  --tools "chatgpt-gpt5.2,claude-opus-4.5,gemini-3-pro,grok-4.1,deepseek-v3.2" \
  --github-user "glpfive25-cyber" \
  --github-token "ghp_YOUR_GITHUB_TOKEN_HERE" \
  --main-url "https://geminiai.asia/list/#/home" \
  --secondary-url "https://claudeapp.asia/list/#/home" \
  --nav-url "https://chatgpt-plus.top/" \
  --images 6 \
  --style notion \
  --output "./my-repos"
```

### 使用配置文件

```bash
# 创建配置文件
cat > config.json << 'EOF'
{
  "ai_tools": [
    "chatgpt-gpt5.2",
    "claude-opus-4.5",
    "gemini-3-pro",
    "grok-4.1",
    "deepseek-v3.2"
  ],
  "github_username": "glpfive25-cyber",
  "github_token": "ghp_YOUR_GITHUB_TOKEN_HERE",
  "mirror_urls": {
    "main": "https://geminiai.asia/list/#/home",
    "secondary": "https://claudeapp.asia/list/#/home",
    "nav": "https://chatgpt-plus.top/"
  },
  "image_count": 6,
  "image_style": "notion",
  "base_directory": "./ai-mirror-repos"
}
EOF

# 使用配置文件运行
bun .claude/skills/ai-mirror-publisher/scripts/publish.ts --config config.json
```

## 生成的配图类型

每个AI工具自动生成6张专业配图：

1. **封面图** - notion风格，品牌色点缀，清晰专业
2. **概念图** - tech风格，技术架构，镜像站原理
3. **流程图** - notion风格，注册登录步骤，1-2-3清晰
4. **对比图** - minimal风格，功能对比表，数据可视化
5. **场景图** - warm风格，实际应用场景，温馨友好
6. **FAQ图** - notion风格，常见问题解答，实用清晰

## 生成的内容结构

### README.md 包含：
```markdown
# {AI工具名称}官网镜像站使用指南（国内直连）

## ✅ 精选入口
- 主入口：{mirror_main_url}
- 备用入口：{mirror_secondary_url}
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

## 🎯 核心优势
[根据AI工具特点定制]

## 🚀 快速开始
[详细使用教程]

## 📊 功能对比
[与其他工具对比]

## ❓ 常见问题
[FAQ解答]

## 🔒 安全建议
[隐私保护指南]
```

### index.html 包含：
- 响应式网页设计
- 图片展示
- 内容排版
- 导航链接

## 工作流程

### 步骤1：准备工作目录
```bash
mkdir -p {base_directory}
cd {base_directory}
```

### 步骤2：批量生成内容
对每个 AI 工具：
1. 创建 `{tool_name}-mirror` 目录
2. 生成 6 张专业配图
3. 根据 AI 工具特点生成定制化的 README.md
4. 生成对应的 index.html

### 步骤3：Git 初始化
```bash
git init
git add .
git commit -m "Initial commit: {tool_name} mirror site guide with images"
git branch -M main
```

### 步骤4：创建 GitHub 仓库
```bash
curl -X POST \
  -H "Authorization: token {github_token}" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos \
  -d '{"name":"{repo_name}","private":false}'
```

### 步骤5：推送到 GitHub
```bash
git remote add origin "https://{github_token}@github.com/{github_username}/{repo_name}.git"
git push -u origin main
```

### 步骤6：返回结果
返回所有创建的仓库 URL 列表

## 配图提示词模板

### ChatGPT 封面图
```
ChatGPT镜像站访问指南，notion风格，极简手绘线条，黑色线条白色背景，绿色点缀，对话框图标，火柴人使用笔记本电脑，网络连接符号，浅蓝云朵，清晰明了，16:9横版
```

### Claude 封面图
```
Claude镜像站使用教程，notion风格，极简手绘线条，黑色线条白色背景，橙棕色点缀，智能助手图标，文档处理场景，服务器节点，专业简洁，16:9横版
```

### Gemini 封面图
```
Gemini镜像站完整指南，notion风格，极简手绘线条，黑色线条白色背景，蓝紫渐变点缀，星星图标，多模态交互界面，全球网络，现代科技感，16:9横版
```

### 技术原理图
```
AI镜像站概念图，tech科技风格，深蓝电光青色，深灰背景，中心服务器图标，周围多个镜像节点，网络连接线，全球地图轮廓，科技感强，16:9横版
```

### 流程图
```
镜像站注册登录流程，notion风格，极简手绘线条，黑色线条白色背景，浅蓝点缀，1-2-3-4步骤数字，箭头连接，邮箱图标密码图标，火柴人操作界面，流程清晰，16:9横版
```

### 对比图
```
AI工具核心功能对比表，notion风格，极简手绘线条，黑色线条白色背景，表格布局三列四行，ChatGPT绿Claude橙Gemini蓝标识，对勾叉号图标，功能名称清晰，专业对比，16:9横版
```

### 场景图
```
AI辅助办公协作，warm温暖风格，温暖橙金黄色，奶油背景，火柴人团队在办公桌前，笔记本电脑，对话气泡，咖啡杯，温馨高效，16:9横版
```

### FAQ图
```
AI镜像站常见问题，notion风格，极简手绘线条，黑色线条白色背景，浅黄点缀，问号图标，Q&A列表，FAQ标识，清晰明了，16:9横版
```

## 错误处理

### 网络错误
- 重试机制（最多3次）
- 超时设置（60秒）
- 失败后继续处理下一个

### GitHub API 错误
- 仓库已存在：跳过创建，直接推送
- 认证失败：提示检查 token
- 限流：等待后重试

### 图片生成错误
- 单张失败不影响整体
- 记录失败的图片
- 继续生成其他图片

### Git 错误
- 远程已存在：先删除后添加
- 推送失败：检查认证和网络
- 冲突处理：强制推送

## 成功标准
- ✅ 所有目录创建成功
- ✅ 图片生成完整（每个工具6张）
- ✅ 内容生成准确且定制化
- ✅ GitHub 仓库全部创建
- ✅ 代码和图片全部推送成功
- ✅ 返回完整的 URL 列表

## 使用示例

### 示例1：生成3个最新AI工具指南

```bash
bun .claude/skills/ai-mirror-publisher/scripts/publish.ts \
  --tools "chatgpt-gpt5.2,claude-opus-4.5,gemini-3-pro" \
  --github-user "glpfive25-cyber" \
  --github-token "ghp_xxx" \
  --main-url "https://geminiai.asia/list/#/home" \
  --nav-url "https://chatgpt-plus.top/"
```

**预期输出：**
```
🚀 开始批量生成AI镜像站指南...
========================================

[1/3] 处理 chatgpt-gpt5.2...
  ✓ 创建目录
  ✓ 生成配图 (6/6)
  ✓ 生成内容
  ✓ 创建GitHub仓库
  ✓ 推送代码
  📦 https://github.com/glpfive25-cyber/chatgpt-gpt5.2-mirror

[2/3] 处理 claude-opus-4.5...
  ✓ 创建目录
  ✓ 生成配图 (6/6)
  ✓ 生成内容
  ✓ 创建GitHub仓库
  ✓ 推送代码
  📦 https://github.com/glpfive25-cyber/claude-opus-4.5-mirror

[3/3] 处理 gemini-3-pro...
  ✓ 创建目录
  ✓ 生成配图 (6/6)
  ✓ 生成内容
  ✓ 创建GitHub仓库
  ✓ 推送代码
  📦 https://github.com/glpfive25-cyber/gemini-3-pro-mirror

========================================
✅ 完成！共创建 3 个图文并茂的仓库

📦 仓库列表：
1. https://github.com/glpfive25-cyber/chatgpt-gpt5.2-mirror
2. https://github.com/glpfive25-cyber/claude-opus-4.5-mirror
3. https://github.com/glpfive25-cyber/gemini-3-pro-mirror

⏱️  总耗时：约 8-10 分钟
📊 成功率：100%
========================================
```

### 示例2：生成5个AI工具完整指南

```bash
bun .claude/skills/ai-mirror-publisher/scripts/publish.ts \
  --tools "chatgpt-gpt5.2,claude-opus-4.5,gemini-3-pro,grok-4.1,deepseek-v3.2" \
  --github-user "glpfive25-cyber" \
  --github-token "ghp_xxx" \
  --main-url "https://geminiai.asia/list/#/home" \
  --secondary-url "https://claudeapp.asia/list/#/home" \
  --nav-url "https://chatgpt-plus.top/" \
  --images 6 \
  --style notion
```

## 性能指标

### 预期性能
- 单个工具处理时间：2-3分钟
  - 图片生成：1.5-2分钟（6张）
  - 内容生成：10-20秒
  - GitHub操作：20-30秒
- 5个工具总时间：约10-15分钟
- 成功率：>95%

### 优化建议
- 图片生成可并行处理
- GitHub API 批量创建
- 复用内容模板
- 缓存已生成内容

## 高级功能

### 1. 内容定制化
- 根据AI工具类型自动调整内容重点
- 突出各工具的独特优势
- 生成针对性的使用示例
- 品牌色自动适配

### 2. 批量操作优化
- 并行生成图片（提速50%）
- 串行推送代码（避免冲突）
- 进度实时显示
- 失败自动重试

### 3. 版本控制
- 自动生成 .gitignore
- 标准化的 commit message
- 分支管理（默认 main）
- Tag 标记版本

### 4. 内容验证
- 检查链接有效性
- 验证 Markdown 格式
- HTML 语法检查
- 图片完整性验证

## 维护与更新

### 定期更新
- AI工具版本更新
- 镜像链接更新
- 功能特性更新
- 配图风格优化

### 扩展性
- 支持添加新的AI工具
- 支持自定义模板
- 支持多语言版本
- 支持自定义配图风格

## 安全注意事项

### Token 安全
- ⚠️ 不要在代码中硬编码 token
- ⚠️ 不要提交 token 到版本控制
- ⚠️ 定期轮换 token
- ✅ 使用环境变量存储
- ✅ 使用配置文件（添加到 .gitignore）

### 内容安全
- 避免包含敏感信息
- 遵守各平台使用条款
- 尊重知识产权
- 合理使用品牌色

## 故障排查

### 常见问题

**Q: 图片生成失败怎么办？**
A: 检查 Z-Image API Key，查看网络连接，单张失败不影响整体

**Q: 仓库已存在怎么办？**
A: 自动跳过创建步骤，直接推送更新

**Q: Push 失败怎么办？**
A: 检查 token 权限、仓库可见性、网络连接

**Q: 批量操作中断怎么办？**
A: 记录已完成的仓库，从中断点继续

**Q: 如何自定义内容？**
A: 修改内容模板文件，或使用自定义配置

## 相关技能
- `wechat-zimage-generator` - 配图生成器（本技能依赖）
- `batch-ai-mirror-github-uploader` - 批量上传器（本技能整合）
- `baoyu-post-to-wechat` - 微信公众号发布

## 技术栈
- **运行环境**: Bun
- **图片生成**: Z-Image Turbo API
- **版本控制**: Git
- **代码托管**: GitHub API
- **内容格式**: Markdown + HTML

## 标签
`github-automation` `batch-processing` `ai-tools` `content-generation` `image-generation` `mirror-sites` `devops` `repository-management` `markdown` `html`

---

## 快速命令参考

```bash
# 基础用法
bun scripts/publish.ts --tools "tool1,tool2" --github-user "user" --github-token "token" --main-url "url" --nav-url "url"

# 使用配置文件
bun scripts/publish.ts --config config.json

# 查看帮助
bun scripts/publish.ts --help

# 测试单个工具
bun scripts/publish.ts --tools "chatgpt-gpt5.2" --github-user "user" --github-token "token" --main-url "url" --nav-url "url"
```

---

**开始一键生成图文并茂的AI镜像站指南吧！🚀**
