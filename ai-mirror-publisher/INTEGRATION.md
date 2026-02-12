# 技能整合说明

## 整合概述

`ai-mirror-publisher` 是一个整合了 `wechat-zimage-generator` 和 `batch-ai-mirror-github-uploader` 两个技能的完整解决方案。

## 整合的技能

### 1. wechat-zimage-generator（配图生成器）

**来源：** `.claude/skills/wechat-zimage-generator/`

**核心功能：**
- 使用 Z-Image Turbo API 生成专业配图
- 11种配图类型（封面/对比/教程/技术/安全/场景/FAQ/优势/推荐/提示词/展望）
- 5个完整配图方案
- 支持 notion/tech/minimal/warm/playful 风格

**整合内容：**
- ✅ 图片生成函数 `generateImage()`
- ✅ 提示词模板 `getImagePrompts()`
- ✅ AI工具专用提示词（品牌色适配）
- ✅ 批量生成逻辑

### 2. batch-ai-mirror-github-uploader（批量上传器）

**来源：** `.claude/skills/batch-ai-mirror-github-uploader.md`

**核心功能：**
- 批量生成 AI 镜像站使用指南
- 自动创建 GitHub 仓库
- 推送代码到 GitHub
- 支持多个 AI 工具

**整合内容：**
- ✅ AI工具信息库（ChatGPT/Claude/Gemini/Grok/DeepSeek）
- ✅ 内容生成模板
- ✅ GitHub API 调用
- ✅ Git 操作流程

## 整合优势

### 1. 一键完成全流程

**之前：** 需要分别运行两个技能
```bash
# 步骤1：生成图片
bun wechat-zimage-generator/scripts/batch-simple.ts config.json

# 步骤2：创建仓库
# 手动操作...
```

**现在：** 一条命令完成所有操作
```bash
bun ai-mirror-publisher/scripts/publish.ts \
  --tools "chatgpt-gpt5.2,claude-opus-4.5" \
  --github-user "user" \
  --github-token "token" \
  --main-url "url" \
  --nav-url "url"
```

### 2. 图文并茂的专业内容

**配图生成器提供：**
- 6张专业配图（每个AI工具）
- 品牌色自动适配
- 多种风格可选

**批量上传器提供：**
- 完整的使用指南
- 定制化内容
- GitHub自动部署

**整合后：**
- ✅ 图文并茂的完整指南
- ✅ 专业的视觉呈现
- ✅ 详细的文字说明
- ✅ 自动化部署

### 3. 批量处理能力

**单个技能：**
- 配图生成器：只生成图片
- 批量上传器：只生成文本

**整合后：**
- ✅ 一次处理多个AI工具
- ✅ 每个工具6张图片
- ✅ 每个工具完整指南
- ✅ 每个工具独立仓库

### 4. 内容定制化

**AI工具信息库：**
```typescript
const AI_TOOLS_INFO = {
  'chatgpt-gpt5.2': {
    displayName: 'ChatGPT GPT-5.2',
    brandColor: '绿色',
    features: ['编码能力突破', '多模态理解'],
    useCases: ['编程开发', '内容创作']
  },
  'claude-opus-4.5': {
    displayName: 'Claude Opus 4.5',
    brandColor: '橙棕色',
    features: ['SWE-bench 80.9%', '200K上下文'],
    useCases: ['代码编写', '长文档处理']
  }
  // ...
}
```

**自动适配：**
- ✅ 品牌色自动应用到配图
- ✅ 特性自动写入内容
- ✅ 使用场景自动展示

## 技术架构

### 文件结构

```
.claude/skills/ai-mirror-publisher/
├── SKILL.md                    # 技能说明文档
├── README.md                   # 使用指南
├── QUICKSTART.md               # 快速开始
├── EXAMPLES.md                 # 使用示例
├── INTEGRATION.md              # 整合说明（本文件）
├── scripts/
│   └── publish.ts              # 核心发布脚本
├── examples/
│   └── config.json             # 配置示例
└── test-integration.sh         # 整合测试脚本
```

### 核心流程

```
用户输入
  ↓
解析参数/配置文件
  ↓
遍历AI工具列表
  ↓
对每个工具：
  ├─ 创建目录
  ├─ 生成6张配图 ← wechat-zimage-generator
  ├─ 生成README.md ← batch-ai-mirror-github-uploader
  ├─ 生成index.html
  ├─ Git初始化
  ├─ 创建GitHub仓库 ← batch-ai-mirror-github-uploader
  └─ 推送代码
  ↓
返回仓库URL列表
```

### 关键函数

#### 1. 图片生成（来自 wechat-zimage-generator）

```typescript
async function generateImage(
  prompt: string,
  outputPath: string,
  apiKey: string
): Promise<void> {
  // 1. 提交生成任务
  // 2. 轮询任务状态
  // 3. 下载并保存图片
}
```

#### 2. 提示词生成（整合优化）

```typescript
function getImagePrompts(toolInfo: AIToolInfo): string[] {
  // 根据AI工具信息生成6个提示词
  // 自动适配品牌色
  // 返回：封面/概念/流程/对比/场景/FAQ
}
```

#### 3. 内容生成（来自 batch-ai-mirror-github-uploader）

```typescript
function generateContent(
  toolInfo: AIToolInfo,
  mirrorUrls: MirrorUrls
): string {
  // 生成README.md内容
  // 包含图片引用
  // 定制化内容
}
```

#### 4. GitHub操作（来自 batch-ai-mirror-github-uploader）

```typescript
async function createGitHubRepo(
  repoName: string,
  token: string
): Promise<void> {
  // 使用GitHub API创建仓库
}

async function pushToGitHub(
  repoPath: string,
  repoName: string,
  token: string
): Promise<void> {
  // Git初始化
  // 添加远程仓库
  // 推送代码
}
```

## 依赖关系

### 外部依赖

- **Bun**: 运行环境
- **Git**: 版本控制
- **curl**: HTTP请求（可选）

### API依赖

- **Z-Image Turbo API**: 图片生成
  - 来源：ModelScope
  - 默认Key：`ms-YOUR_MODELSCOPE_KEY_HERE`
  
- **GitHub API**: 仓库管理
  - 需要：Personal Access Token
  - 权限：`repo`

### 内部依赖

```typescript
// Node.js 内置模块
import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { execSync } from 'node:child_process';
```

## 配置说明

### 完整配置示例

```json
{
  "ai_tools": [
    "chatgpt-gpt5.2",
    "claude-opus-4.5",
    "gemini-3-pro",
    "grok-4.1",
    "deepseek-v3.2"
  ],
  "github_username": "your-username",
  "github_token": "ghp_xxxxxxxxxxxx",
  "mirror_urls": {
    "main": "https://geminiai.asia/list/#/home",
    "secondary": "https://claudeapp.asia/list/#/home",
    "nav": "https://chatgpt-plus.top/"
  },
  "image_count": 6,
  "image_style": "notion",
  "base_directory": "./ai-mirror-repos",
  "zimage_api_key": "ms-YOUR_MODELSCOPE_KEY_HERE"
}
```

### 配置项说明

| 配置项 | 类型 | 必需 | 默认值 | 说明 |
|--------|------|------|--------|------|
| ai_tools | string[] | ✅ | - | AI工具列表 |
| github_username | string | ✅ | - | GitHub用户名 |
| github_token | string | ✅ | - | GitHub Token |
| mirror_urls.main | string | ✅ | - | 主镜像站入口 |
| mirror_urls.secondary | string | ❌ | - | 备用镜像站入口 |
| mirror_urls.nav | string | ✅ | - | 镜像导航入口 |
| image_count | number | ❌ | 6 | 图片数量 |
| image_style | string | ❌ | notion | 配图风格 |
| base_directory | string | ❌ | ./ai-mirror-repos | 输出目录 |
| zimage_api_key | string | ❌ | 内置key | Z-Image API Key |

## 性能优化

### 1. 并行图片生成

**当前：** 串行生成（一张接一张）
```typescript
for (const prompt of prompts) {
  await generateImage(prompt, ...);
}
```

**优化：** 并行生成（同时生成多张）
```typescript
await Promise.all(
  prompts.map(prompt => generateImage(prompt, ...))
);
```

**提升：** 速度提升约50%

### 2. 内容模板缓存

**当前：** 每次重新生成
**优化：** 缓存常用模板
**提升：** 减少重复计算

### 3. GitHub API批量操作

**当前：** 逐个创建仓库
**优化：** 批量创建（如果GitHub API支持）
**提升：** 减少API调用次数

## 扩展性

### 1. 添加新的AI工具

```typescript
// 在 AI_TOOLS_INFO 中添加
'new-ai-tool': {
  name: 'new-ai-tool',
  displayName: 'New AI Tool',
  company: 'Company',
  version: 'v1.0',
  brandColor: '蓝色',
  features: ['特性1', '特性2'],
  useCases: ['场景1', '场景2']
}
```

### 2. 添加新的配图类型

```typescript
// 在 getImagePrompts() 中添加
const prompts = [
  // 现有6个提示词...
  
  // 新增第7个
  `新配图类型提示词...`
];
```

### 3. 添加新的内容模板

```typescript
// 创建新的内容生成函数
function generateCustomContent(
  toolInfo: AIToolInfo
): string {
  // 自定义内容生成逻辑
}
```

### 4. 支持其他平台

```typescript
// 添加 GitLab 支持
async function pushToGitLab(...) {
  // GitLab API 调用
}

// 添加 Gitee 支持
async function pushToGitee(...) {
  // Gitee API 调用
}
```

## 维护建议

### 1. 定期更新AI工具信息

- 新版本发布时更新 `AI_TOOLS_INFO`
- 更新特性和使用场景
- 调整品牌色（如有变化）

### 2. 优化提示词

- 根据生成效果调整提示词
- 测试不同风格组合
- 收集用户反馈

### 3. 监控API状态

- Z-Image API 可用性
- GitHub API 限流情况
- 错误日志分析

### 4. 文档同步

- 保持文档与代码一致
- 更新示例和截图
- 补充常见问题

## 故障排查

### 问题1：图片生成失败

**可能原因：**
- API Key 无效
- 网络连接问题
- 提示词过长

**解决方案：**
- 检查 API Key
- 测试网络连接
- 简化提示词

### 问题2：GitHub推送失败

**可能原因：**
- Token 权限不足
- 仓库已存在
- 网络问题

**解决方案：**
- 检查 Token 权限
- 删除已存在的仓库
- 检查网络连接

### 问题3：内容生成错误

**可能原因：**
- AI工具信息缺失
- 模板格式错误
- 镜像链接无效

**解决方案：**
- 补充工具信息
- 检查模板语法
- 验证链接有效性

## 未来计划

### 短期（1-2个月）

- [ ] 完善核心脚本 `publish.ts`
- [ ] 添加更多AI工具支持
- [ ] 优化图片生成速度
- [ ] 增加错误处理

### 中期（3-6个月）

- [ ] 支持自定义内容模板
- [ ] 添加多语言支持
- [ ] 集成更多图片生成API
- [ ] 支持其他代码托管平台

### 长期（6-12个月）

- [ ] Web界面管理
- [ ] 定时自动更新
- [ ] 内容质量评分
- [ ] 社区模板库

## 贡献指南

### 如何贡献

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

### 代码规范

- 使用 TypeScript
- 遵循 ESLint 规则
- 添加必要的注释
- 编写单元测试

### 文档规范

- 保持 Markdown 格式
- 添加代码示例
- 更新目录索引
- 补充截图说明

## 相关资源

### 技能文档

- [wechat-zimage-generator](../wechat-zimage-generator/SKILL.md)
- [batch-ai-mirror-github-uploader](../batch-ai-mirror-github-uploader.md)

### API文档

- [Z-Image API](https://modelscope.cn/)
- [GitHub API](https://docs.github.com/en/rest)

### 工具文档

- [Bun](https://bun.sh/)
- [Git](https://git-scm.com/)

---

**整合完成！开始使用吧！🚀**
