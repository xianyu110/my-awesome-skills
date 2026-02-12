#!/usr/bin/env bun
import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { execSync } from 'node:child_process';

const BASE_URL = 'https://api-inference.modelscope.cn/';
const DEFAULT_API_KEY = 'ms-YOUR_MODELSCOPE_KEY_HERE';

interface Config {
  ai_tools: string[];
  github_username: string;
  github_token: string;
  mirror_urls: {
    main: string;
    secondary?: string;
    nav: string;
  };
  image_count?: number;
  image_style?: string;
  base_directory?: string;
  zimage_api_key?: string;
}

interface AIToolInfo {
  name: string;
  displayName: string;
  company: string;
  version: string;
  brandColor: string;
  features: string[];
  useCases: string[];
}

const AI_TOOLS_INFO: Record<string, AIToolInfo> = {
  'chatgpt-gpt5.2': {
    name: 'chatgpt-gpt5.2',
    displayName: 'ChatGPT GPT-5.2',
    company: 'OpenAI',
    version: 'GPT-5.2 (2025年12月最新)',
    brandColor: '绿色',
    features: ['编码能力突破', '多模态理解', '推理能力增强', '上下文理解提升'],
    useCases: ['编程开发', '内容创作', '数据分析', '学习辅助']
  },
  'claude-opus-4.5': {
    name: 'claude-opus-4.5',
    displayName: 'Claude Opus 4.5',
    company: 'Anthropic',
    version: 'Opus 4.5 (2025年11月，编码最强)',
    brandColor: '橙棕色',
    features: ['SWE-bench 80.9%第一', '200K上下文', '混合架构', '即时响应'],
    useCases: ['代码编写', '长文档处理', '技术写作', '数据分析']
  },
  'gemini-3-pro': {
    name: 'gemini-3-pro',
    displayName: 'Gemini 3 Pro',
    company: 'Google',
    version: 'Gemini 3 Pro (2025年11月最新)',
    brandColor: '蓝紫渐变',
    features: ['100万token上下文', '数学AIME 95%', '多模态', '中文优化'],
    useCases: ['学术研究', '数学计算', '多模态分析', '中文处理']
  },
  'grok-4.1': {
    name: 'grok-4.1',
    displayName: 'Grok 4.1',
    company: 'xAI',
    version: 'Grok 4.1 (2025年最新)',
    brandColor: '黑白红',
    features: ['实时信息', 'X平台集成', 'Think推理模式', '幽默风格'],
    useCases: ['实时资讯', '社交媒体', '创意写作', '趋势分析']
  },
  'deepseek-v3.2': {
    name: 'deepseek-v3.2',
    displayName: 'DeepSeek v3.2',
    company: 'DeepSeek',
    version: 'DeepSeek v3.2 (2025年最新)',
    brandColor: '深蓝',
    features: ['开源', '性价比最高', '数学推理', '代码能力强'],
    useCases: ['编程开发', '数学计算', '本地部署', '成本优化']
  }
};

async function generateImage(prompt: string, outputPath: string, apiKey: string): Promise<void> {
  console.log(`  [图片] 生成中: ${path.basename(outputPath)}`);
  
  const submitResponse = await fetch(`${BASE_URL}v1/images/generations`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
      'X-ModelScope-Async-Mode': 'true',
    },
    body: JSON.stringify({
      model: 'Tongyi-MAI/Z-Image-Turbo',
      prompt,
    }),
  });

  if (!submitResponse.ok) {
    throw new Error(`提交失败: ${submitResponse.status}`);
  }

  const { task_id } = await submitResponse.json();

  let attempts = 0;
  while (attempts < 60) {
    await new Promise(resolve => setTimeout(resolve, 5000));
    attempts++;

    const statusResponse = await fetch(`${BASE_URL}v1/tasks/${task_id}`, {
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
        'X-ModelScope-Task-Type': 'image_generation',
      },
    });

    const data = await statusResponse.json();

    if (data.task_status === 'SUCCEED') {
      const imageUrl = data.output_images[0];
      const imageResponse = await fetch(imageUrl);
      const imageBuffer = Buffer.from(await imageResponse.arrayBuffer());
      fs.writeFileSync(outputPath, imageBuffer);
      console.log(`  [图片] ✓ 完成: ${path.basename(outputPath)}`);
      return;
    } else if (data.task_status === 'FAILED') {
      throw new Error('生成失败');
    }
  }

  throw new Error('超时');
}

function getImagePrompts(toolInfo: AIToolInfo): string[] {
  const brandColorMap: Record<string, string> = {
    '绿色': '绿色点缀',
    '橙棕色': '橙棕色点缀',
    '蓝紫渐变': '蓝紫渐变点缀',
    '黑白红': '黑白红点缀',
    '深蓝': '深蓝点缀'
  };
  
  const colorAccent = brandColorMap[toolInfo.brandColor] || '浅蓝点缀';
  
  return [
    // 1. 封面图
    `${toolInfo.displayName}镜像站访问指南，notion风格，极简手绘线条，黑色线条白色背景，${colorAccent}，对话框图标，火柴人使用笔记本电脑，网络连接符号，浅蓝云朵，清晰明了，16:9横版`,
    
    // 2. 概念图
    `AI镜像站概念图，tech科技风格，深蓝电光青色，深灰背景，中心服务器图标，周围多个镜像节点，网络连接线，全球地图轮廓，科技感强，16:9横版`,
    
    // 3. 流程图
    `镜像站注册登录流程，notion风格，极简手绘线条，黑色线条白色背景，浅蓝点缀，1-2-3-4步骤数字，箭头连接，邮箱图标密码图标，火柴人操作界面，流程清晰，16:9横版`,
    
    // 4. 对比图
    `AI工具核心功能对比表，notion风格，极简手绘线条，黑色线条白色背景，表格布局三列四行，${colorAccent}，对勾叉号图标，功能名称清晰，专业对比，16:9横版`,
    
    // 5. 场景图
    `AI辅助办公协作，warm温暖风格，温暖橙金黄色，奶油背景，火柴人团队在办公桌前，笔记本电脑，对话气泡，咖啡杯，温馨高效，16:9横版`,
    
    // 6. FAQ图
    `AI镜像站常见问题，notion风格，极简手绘线条，黑色线条白色背景，浅黄点缀，问号图标，Q&A列表，FAQ标识，清晰明了，16:9横版`
  ];
}

async function generateImages(toolInfo: AIToolInfo, outputDir: string, apiKey: string): Promise<void> {
  console.log(`  [图片] 开始生成配图...`);
  
  const imagesDir = path.join(outputDir, 'images');
  if (!fs.existsSync(imagesDir)) {
    fs.mkdirSync(imagesDir, { recursive: true });
  }
  
  const prompts = getImagePrompts(toolInfo);
  const imageNames = ['cover.jpg', 'concept.jpg', 'flow.jpg', 'comparison.jpg', 'scenario.jpg', 'faq.jpg'];
  
  let successCount = 0;
  for (let i = 0; i < prompts.length; i++) {
    const imagePath = path.join(imagesDir, imageNames[i]!);
    try {
      await generateImage(prompts[i]!, imagePath, apiKey);
      successCount++;
    } catch (err) {
      console.error(`  [图片] ✗ 失败: ${imageNames[i]} - ${err instanceof Error ? err.message : String(err)}`);
    }
  }
  
  console.log(`  [图片] ✓ 完成！成功生成 ${successCount}/${prompts.length} 张图片`);
}

function generateREADME(toolInfo: AIToolInfo, mirrorUrls: { main: string; secondary?: string; nav: string }): string {
  const { displayName, company, version, features, useCases } = toolInfo;
  
  return `# ${displayName}官网镜像站使用指南（国内直连）

![封面图](images/cover.jpg)

## ✅ 精选入口

- **主入口**：${mirrorUrls.main}
${mirrorUrls.secondary ? `- **备用入口**：${mirrorUrls.secondary}` : ''}
- **镜像导航**：${mirrorUrls.nav}

## 📋 目录导航

- [什么是 ${displayName}？](#什么是-${toolInfo.name.replace(/[^a-z0-9]/g, '-')})
- [为什么选择镜像网站？](#为什么选择镜像网站)
- [精选镜像站推荐](#精选镜像站推荐)
- [核心优势与功能](#核心优势与功能)
- [快速开始使用](#快速开始使用)
- [官网与镜像站对比](#官网与镜像站对比)
- [核心功能详解](#核心功能详解)
- [常见问题FAQ](#常见问题faq)
- [隐私安全建议](#隐私安全建议)
- [总结与行动建议](#总结与行动建议)

---

## 什么是 ${displayName}？

![概念图](images/concept.jpg)

${displayName} 是由 ${company} 开发的人工智能助手，${version}。

### 核心特点

${features.map((f, i) => `${i + 1}. **${f}**`).join('\n')}

### 主要应用场景

${useCases.map((u, i) => `- ${u}`).join('\n')}

---

## 为什么选择镜像网站？

### 国内访问优势

1. **无需翻墙**：直接访问，无需VPN
2. **速度更快**：国内CDN加速，响应迅速
3. **稳定可靠**：多节点部署，高可用性
4. **完全免费**：无需付费，功能完整

### 镜像站 vs 官网

| 对比项 | 官网 | 镜像站 |
|--------|------|--------|
| 访问方式 | 需要VPN | 直接访问 |
| 访问速度 | 较慢 | 快速 |
| 稳定性 | 一般 | 高 |
| 费用 | 需付费 | 免费 |
| 功能 | 完整 | 完整 |

---

## 精选镜像站推荐

![流程图](images/flow.jpg)

### 主入口（推荐）⭐

**链接**：${mirrorUrls.main}

**特点**：
- ✅ 速度快，稳定性高
- ✅ 界面友好，易于使用
- ✅ 功能完整，定期更新

### 使用步骤

1. **访问镜像站**
   - 点击上方主入口链接
   - 无需注册，直接使用

2. **开始对话**
   - 在输入框输入问题
   - 等待AI回复

3. **高级功能**
   - 上传文件（支持多种格式）
   - 多轮对话
   - 导出对话记录

${mirrorUrls.secondary ? `
### 备用入口

**链接**：${mirrorUrls.secondary}

**说明**：主入口无法访问时使用
` : ''}

### 镜像导航站

**链接**：${mirrorUrls.nav}

**说明**：汇总多个AI工具镜像站，一站式访问

---

## 核心优势与功能

![对比图](images/comparison.jpg)

### ${displayName} 的核心优势

${features.map((f, i) => `
#### ${i + 1}. ${f}

[详细说明...]
`).join('\n')}

### 功能对比

| 功能 | ${displayName} | 其他AI工具 |
|------|----------------|-----------|
| 文本生成 | ✅ 优秀 | ✅ 良好 |
| 代码编写 | ✅ 优秀 | ✅ 良好 |
| 多模态 | ✅ 支持 | ⚠️ 部分支持 |
| 上下文长度 | ✅ 超长 | ⚠️ 一般 |

---

## 快速开始使用

![场景图](images/scenario.jpg)

### 基础使用

#### 1. 文本对话

\`\`\`
你：请帮我写一篇关于AI的文章
AI：[生成文章内容...]
\`\`\`

#### 2. 代码编写

\`\`\`
你：用Python写一个快速排序
AI：[生成代码...]
\`\`\`

#### 3. 文件分析

- 上传PDF、Word、Excel等文件
- AI自动分析内容
- 回答相关问题

### 高级技巧

#### 提示词优化

**基础提示词**：
\`\`\`
写一篇文章
\`\`\`

**优化后**：
\`\`\`
请以专业的口吻，写一篇1000字的文章，主题是人工智能的发展趋势，
包含以下要点：
1. 当前AI技术现状
2. 未来发展方向
3. 对社会的影响
\`\`\`

#### 多轮对话

1. 先提出总体需求
2. 根据回复细化要求
3. 逐步完善结果

---

## 官网与镜像站对比

### 功能对比

| 功能 | 官网 | 镜像站 |
|------|------|--------|
| 基础对话 | ✅ | ✅ |
| 文件上传 | ✅ | ✅ |
| 多轮对话 | ✅ | ✅ |
| 历史记录 | ✅ | ✅ |
| 自定义设置 | ✅ | ✅ |

### 访问对比

| 对比项 | 官网 | 镜像站 |
|--------|------|--------|
| 需要VPN | ✅ 是 | ❌ 否 |
| 访问速度 | ⚠️ 慢 | ✅ 快 |
| 稳定性 | ⚠️ 一般 | ✅ 高 |
| 注册要求 | ✅ 需要 | ❌ 不需要 |

---

## 核心功能详解

### 1. 文本生成

- 文章写作
- 内容改写
- 摘要提取
- 翻译服务

### 2. 代码编写

- 多语言支持
- 代码解释
- Bug修复
- 代码优化

### 3. 数据分析

- 文件解析
- 数据可视化
- 趋势分析
- 报告生成

### 4. 创意辅助

- 头脑风暴
- 方案设计
- 内容策划
- 创意生成

---

## 常见问题FAQ

![FAQ图](images/faq.jpg)

### Q1: 镜像站安全吗？

**A**: 镜像站使用HTTPS加密传输，但建议：
- ❌ 不要输入个人敏感信息（身份证、银行卡等）
- ❌ 不要输入公司机密信息
- ✅ 可以用于学习、创作、编程等场景

### Q2: 镜像站会收费吗？

**A**: 目前推荐的镜像站都是免费的，但可能有以下限制：
- 每日使用次数限制
- 单次对话长度限制
- 部分高级功能需要注册

### Q3: 镜像站和官网有什么区别？

**A**: 
- **相同点**：功能基本一致，使用体验相似
- **不同点**：镜像站国内可直接访问，速度更快

### Q4: 如果镜像站无法访问怎么办？

**A**: 
1. 尝试备用入口
2. 访问镜像导航站，查找其他可用镜像
3. 清除浏览器缓存后重试

### Q5: 可以在手机上使用吗？

**A**: 可以！镜像站支持手机浏览器访问，体验与电脑端一致。

### Q6: 对话记录会保存吗？

**A**: 
- 未注册用户：对话记录保存在浏览器本地
- 注册用户：对话记录保存在服务器（建议定期导出）

### Q7: 支持哪些文件格式？

**A**: 
- 文档：PDF、Word、TXT、Markdown
- 表格：Excel、CSV
- 图片：JPG、PNG、GIF
- 代码：各种编程语言文件

### Q8: 如何获得更好的回复质量？

**A**: 
1. 提供清晰具体的问题描述
2. 给出必要的背景信息
3. 明确期望的输出格式
4. 使用多轮对话逐步完善

---

## 隐私安全建议

### ❌ 不建议输入的信息

- 个人身份信息（身份证、护照等）
- 金融信息（银行卡、密码等）
- 公司机密信息
- 他人隐私信息

### ✅ 适合的使用场景

- 学习辅助（作业、论文）
- 编程开发（代码、调试）
- 内容创作（文章、方案）
- 数据分析（公开数据）
- 创意设计（头脑风暴）

### 🔒 安全使用习惯

1. **定期清理**：定期清除对话记录
2. **谨慎分享**：不要分享包含敏感信息的对话
3. **备份重要内容**：及时导出重要对话记录
4. **使用多个镜像**：不要在单一镜像站存储所有信息

---

## 总结与行动建议

### 核心要点

1. **${displayName}** 是 ${company} 开发的强大AI助手
2. **镜像站** 提供国内直连访问，速度快、稳定
3. **免费使用** 大部分功能，无需VPN
4. **注意隐私** 不要输入敏感信息

### 立即开始

1. 点击上方 **主入口** 链接
2. 开始你的第一次对话
3. 探索更多功能

### 推荐阅读

- [${displayName} 官方文档](https://example.com)
- [AI工具使用技巧](https://example.com)
- [提示词工程指南](https://example.com)

---

## 更新日志

- **2025-01-17**: 创建文档，添加最新镜像站链接
- 持续更新中...

---

**免责声明**：本指南仅供学习交流使用，镜像站链接来自互联网公开资源。使用时请遵守相关法律法规和平台使用条款。

**最后更新**：2025年1月17日

---

**觉得有用？欢迎分享给需要的朋友！⭐**
`;
}

function generateHTML(toolInfo: AIToolInfo, mirrorUrls: { main: string; secondary?: string; nav: string }): string {
  const { displayName, features, useCases } = toolInfo;
  
  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${displayName}官网镜像站使用指南</title>
    <meta name="description" content="${displayName}国内镜像站使用指南，免费访问，无需VPN，稳定快速">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 60px 20px; text-align: center; border-radius: 10px; margin-bottom: 30px; box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3); }
        h1 { font-size: 2.5em; margin-bottom: 10px; }
        .subtitle { font-size: 1.2em; opacity: 0.9; }
        .links { background: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .link-item { margin: 15px 0; }
        .link-item a { display: inline-block; padding: 15px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; transition: all 0.3s; font-weight: 500; }
        .link-item a:hover { background: #764ba2; transform: translateY(-2px); box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4); }
        .content { background: white; padding: 40px; border-radius: 10px; margin-bottom: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .image-gallery { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 30px 0; }
        .image-card { background: #f9f9f9; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); transition: transform 0.3s; }
        .image-card:hover { transform: translateY(-5px); box-shadow: 0 4px 15px rgba(0,0,0,0.15); }
        .image-card img { width: 100%; height: 200px; object-fit: cover; }
        .image-card .caption { padding: 15px; text-align: center; font-weight: 500; color: #667eea; }
        .hero-image { width: 100%; max-width: 800px; margin: 30px auto; display: block; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
        h2 { color: #667eea; margin: 30px 0 15px; padding-bottom: 10px; border-bottom: 2px solid #667eea; }
        h3 { color: #764ba2; margin: 20px 0 10px; }
        ul, ol { margin-left: 30px; margin-bottom: 15px; }
        li { margin: 8px 0; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { padding: 12px; text-align: left; border: 1px solid #ddd; }
        th { background: #667eea; color: white; }
        tr:nth-child(even) { background: #f9f9f9; }
        .feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0; }
        .feature-card { padding: 20px; background: #f9f9f9; border-radius: 8px; border-left: 4px solid #667eea; transition: all 0.3s; }
        .feature-card:hover { background: #fff; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .feature-card h4 { color: #667eea; margin-bottom: 10px; }
        .highlight-box { background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #667eea; }
        footer { text-align: center; padding: 30px; color: #666; }
        .badge { display: inline-block; padding: 5px 10px; background: #667eea; color: white; border-radius: 3px; font-size: 0.85em; margin: 0 5px; }
        @media (max-width: 768px) {
            h1 { font-size: 1.8em; }
            .content { padding: 20px; }
            .feature-grid { grid-template-columns: 1fr; }
            .image-gallery { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>${displayName}官网镜像站使用指南</h1>
            <p class="subtitle">🚀 国内直连 | 💯 免费使用 | ⚡ 稳定快速</p>
        </header>

        <!-- 封面图 -->
        <img src="images/cover.jpg" alt="${displayName}封面" class="hero-image">

        <div class="links">
            <h2>✅ 精选入口</h2>
            <div class="link-item">
                <strong>主入口（推荐）：</strong>
                <a href="${mirrorUrls.main}" target="_blank">立即访问 →</a>
            </div>
            ${mirrorUrls.secondary ? `
            <div class="link-item">
                <strong>备用入口：</strong>
                <a href="${mirrorUrls.secondary}" target="_blank">立即访问 →</a>
            </div>
            ` : ''}
            <div class="link-item">
                <strong>镜像导航：</strong>
                <a href="${mirrorUrls.nav}" target="_blank">查看更多 →</a>
            </div>
        </div>

        <div class="content">
            <h2>🎯 什么是 ${displayName}？</h2>
            <div class="highlight-box">
                <p><strong>${displayName}</strong> 是一款强大的AI助手，具有以下核心特点：</p>
                <ul>
                    ${features.map(f => `<li><span class="badge">✓</span> ${f}</li>`).join('\n                    ')}
                </ul>
            </div>

            <!-- 配图展示 -->
            <h2>📸 功能展示</h2>
            <div class="image-gallery">
                <div class="image-card">
                    <img src="images/concept.jpg" alt="镜像站概念图">
                    <div class="caption">镜像站工作原理</div>
                </div>
                <div class="image-card">
                    <img src="images/flow.jpg" alt="使用流程图">
                    <div class="caption">快速开始流程</div>
                </div>
                <div class="image-card">
                    <img src="images/comparison.jpg" alt="功能对比图">
                    <div class="caption">功能对比分析</div>
                </div>
                <div class="image-card">
                    <img src="images/scenario.jpg" alt="应用场景图">
                    <div class="caption">实际应用场景</div>
                </div>
                <div class="image-card">
                    <img src="images/faq.jpg" alt="常见问题图">
                    <div class="caption">常见问题解答</div>
                </div>
            </div>

            <h2>📖 完整使用指南</h2>
            <p>查看完整的 Markdown 格式指南，请访问：<a href="README.md" style="color: #667eea; font-weight: 500;">README.md</a></p>
            
            <h2>🚀 快速开始</h2>
            <ol>
                <li><strong>访问镜像站</strong>：点击上方"主入口"链接</li>
                <li><strong>开始对话</strong>：无需注册，直接在输入框输入问题</li>
                <li><strong>等待回复</strong>：AI会快速生成回复</li>
                <li><strong>继续交流</strong>：可以进行多轮对话，逐步完善结果</li>
            </ol>

            <h2>💡 主要应用场景</h2>
            <div class="feature-grid">
                ${useCases.map(useCase => `
                <div class="feature-card">
                    <h4>📌 ${useCase}</h4>
                    <p>专业的AI辅助，提升工作效率</p>
                </div>
                `).join('\n                ')}
            </div>

            <h2>🎓 使用技巧</h2>
            <div class="feature-grid">
                <div class="feature-card">
                    <h4>清晰描述</h4>
                    <p>提供具体、清晰的问题描述，获得更准确的回复</p>
                </div>
                <div class="feature-card">
                    <h4>多轮对话</h4>
                    <p>通过多轮对话逐步完善和细化结果</p>
                </div>
                <div class="feature-card">
                    <h4>文件上传</h4>
                    <p>支持上传PDF、Word等文件进行分析</p>
                </div>
                <div class="feature-card">
                    <h4>导出记录</h4>
                    <p>及时导出重要的对话记录</p>
                </div>
            </div>

            <h2>⚠️ 安全提示</h2>
            <div class="highlight-box">
                <h3>❌ 不建议输入的信息</h3>
                <ul>
                    <li>个人敏感信息（身份证、银行卡等）</li>
                    <li>公司机密信息</li>
                    <li>他人隐私信息</li>
                </ul>
                <h3 style="margin-top: 15px;">✅ 适合的使用场景</h3>
                <ul>
                    <li>学习辅助（作业、论文）</li>
                    <li>编程开发（代码、调试）</li>
                    <li>内容创作（文章、方案）</li>
                    <li>数据分析（公开数据）</li>
                </ul>
            </div>
        </div>

        <footer>
            <p>本指南仅供学习交流使用 | 最后更新：2025年1月17日</p>
            <p>觉得有用？欢迎分享给需要的朋友！⭐</p>
            <p style="margin-top: 10px; font-size: 0.9em;">
                <a href="README.md" style="color: #667eea; text-decoration: none;">查看完整文档</a> | 
                <a href="https://github.com" style="color: #667eea; text-decoration: none;">GitHub</a>
            </p>
        </footer>
    </div>
</body>
</html>`;
}

async function createGitHubRepo(repoName: string, username: string, token: string): Promise<boolean> {
  console.log(`  [GitHub] 创建仓库: ${repoName}`);
  
  try {
    const response = await fetch('https://api.github.com/user/repos', {
      method: 'POST',
      headers: {
        'Authorization': `token ${token}`,
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: repoName,
        description: `${repoName} 官网镜像站使用指南（国内直连）`,
        private: false,
        auto_init: false,
      }),
    });

    if (response.status === 201) {
      console.log(`  [GitHub] ✓ 仓库创建成功`);
      return true;
    } else if (response.status === 422) {
      console.log(`  [GitHub] ⚠ 仓库已存在，跳过创建`);
      return true;
    } else {
      const error = await response.text();
      console.error(`  [GitHub] ✗ 创建失败: ${response.status} ${error}`);
      return false;
    }
  } catch (err) {
    console.error(`  [GitHub] ✗ 创建失败: ${err instanceof Error ? err.message : String(err)}`);
    return false;
  }
}

function pushToGitHub(repoPath: string, repoName: string, username: string, token: string): boolean {
  console.log(`  [Git] 推送代码到 GitHub...`);
  
  try {
    const { execSync } = require('node:child_process');
    
    // Git 初始化
    execSync('git init', { cwd: repoPath, stdio: 'pipe' });
    execSync('git add .', { cwd: repoPath, stdio: 'pipe' });
    execSync('git commit -m "Initial commit: AI mirror site guide with images"', { cwd: repoPath, stdio: 'pipe' });
    execSync('git branch -M main', { cwd: repoPath, stdio: 'pipe' });
    
    // 添加远程仓库
    const remoteUrl = `https://${token}@github.com/${username}/${repoName}.git`;
    try {
      execSync(`git remote add origin ${remoteUrl}`, { cwd: repoPath, stdio: 'pipe' });
    } catch {
      execSync(`git remote set-url origin ${remoteUrl}`, { cwd: repoPath, stdio: 'pipe' });
    }
    
    // 推送代码
    execSync('git push -u origin main --force', { cwd: repoPath, stdio: 'pipe' });
    
    console.log(`  [Git] ✓ 推送成功`);
    return true;
  } catch (err) {
    console.error(`  [Git] ✗ 推送失败: ${err instanceof Error ? err.message : String(err)}`);
    return false;
  }
}

async function processAITool(
  toolName: string,
  config: Config
): Promise<{ success: boolean; repoUrl?: string }> {
  const toolInfo = AI_TOOLS_INFO[toolName];
  if (!toolInfo) {
    console.error(`❌ 未知的AI工具: ${toolName}`);
    return { success: false };
  }

  const repoName = `${toolName}-mirror`;
  const baseDir = config.base_directory || './ai-mirror-repos';
  const repoPath = path.join(baseDir, repoName);

  console.log(`\n[${toolName}] 开始处理...`);

  try {
    // 1. 创建目录
    if (!fs.existsSync(repoPath)) {
      fs.mkdirSync(repoPath, { recursive: true });
    }
    console.log(`  ✓ 创建目录: ${repoPath}`);

    // 2. 生成配图
    const apiKey = config.zimage_api_key || DEFAULT_API_KEY;
    await generateImages(toolInfo, repoPath, apiKey);

    // 3. 生成 README.md
    const readme = generateREADME(toolInfo, config.mirror_urls);
    fs.writeFileSync(path.join(repoPath, 'README.md'), readme, 'utf-8');
    console.log(`  ✓ 生成内容: README.md`);

    // 4. 生成 index.html
    const html = generateHTML(toolInfo, config.mirror_urls);
    fs.writeFileSync(path.join(repoPath, 'index.html'), html, 'utf-8');
    console.log(`  ✓ 生成内容: index.html`);

    // 5. 生成 .gitignore
    const gitignore = `# 临时文件
*.tmp
*.log
.DS_Store

# 编辑器
.vscode/
.idea/
`;
    fs.writeFileSync(path.join(repoPath, '.gitignore'), gitignore, 'utf-8');

    // 6. 创建 GitHub 仓库
    const repoCreated = await createGitHubRepo(repoName, config.github_username, config.github_token);
    if (!repoCreated) {
      console.error(`  ✗ GitHub 仓库创建失败`);
      return { success: false };
    }

    // 7. 推送到 GitHub
    const pushed = pushToGitHub(repoPath, repoName, config.github_username, config.github_token);
    if (!pushed) {
      console.error(`  ✗ 推送失败`);
      return { success: false };
    }

    const repoUrl = `https://github.com/${config.github_username}/${repoName}`;
    console.log(`  📦 ${repoUrl}`);

    return { success: true, repoUrl };
  } catch (err) {
    console.error(`  ✗ 处理失败: ${err instanceof Error ? err.message : String(err)}`);
    return { success: false };
  }
}

function parseArgs(): Partial<Config> | null {
  const args = process.argv.slice(2);

  if (args.includes('--help') || args.includes('-h')) {
    printUsage();
    return null;
  }

  // 检查是否使用配置文件
  const configIndex = args.indexOf('--config');
  if (configIndex !== -1 && args[configIndex + 1]) {
    const configPath = args[configIndex + 1]!;
    try {
      const configContent = fs.readFileSync(configPath, 'utf-8');
      return JSON.parse(configContent);
    } catch (err) {
      console.error(`错误: 无法读取配置文件 ${configPath}`);
      console.error(err instanceof Error ? err.message : String(err));
      process.exit(1);
    }
  }

  // 解析命令行参数
  const config: Partial<Config> = {
    ai_tools: [],
    mirror_urls: {},
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--tools' && args[i + 1]) {
      config.ai_tools = args[++i]!.split(',').map(t => t.trim());
    } else if (arg === '--github-user' && args[i + 1]) {
      config.github_username = args[++i];
    } else if (arg === '--github-token' && args[i + 1]) {
      config.github_token = args[++i];
    } else if (arg === '--main-url' && args[i + 1]) {
      config.mirror_urls!.main = args[++i]!;
    } else if (arg === '--secondary-url' && args[i + 1]) {
      config.mirror_urls!.secondary = args[++i];
    } else if (arg === '--nav-url' && args[i + 1]) {
      config.mirror_urls!.nav = args[++i]!;
    } else if (arg === '--images' && args[i + 1]) {
      config.image_count = parseInt(args[++i]!, 10);
    } else if (arg === '--style' && args[i + 1]) {
      config.image_style = args[++i];
    } else if (arg === '--output' && args[i + 1]) {
      config.base_directory = args[++i];
    }
  }

  return config;
}

function printUsage(): void {
  console.log(`AI Mirror Site Publisher - 一键生成图文并茂的AI镜像站指南并发布到GitHub

用法:
  bun publish.ts --tools "tool1,tool2" [选项]
  bun publish.ts --config config.json

必需参数:
  --tools <list>         AI工具列表（逗号分隔）
  --github-user <name>   GitHub用户名
  --github-token <token> GitHub Personal Access Token
  --main-url <url>       主镜像站入口
  --nav-url <url>        镜像导航入口

可选参数:
  --secondary-url <url>  备用镜像站入口
  --images <n>           图片数量（默认6）
  --style <style>        配图风格（默认notion）
  --output <dir>         输出目录（默认./ai-mirror-repos）
  --config <file>        使用配置文件

支持的AI工具:
  chatgpt-gpt5.2        ChatGPT GPT-5.2 (2025年12月最新)
  claude-opus-4.5       Claude Opus 4.5 (编码最强)
  gemini-3-pro          Gemini 3 Pro (100万token)
  grok-4.1              Grok 4.1 (实时信息)
  deepseek-v3.2         DeepSeek v3.2 (开源)

示例:
  # 基础用法
  bun publish.ts \\
    --tools "chatgpt-gpt5.2,claude-opus-4.5" \\
    --github-user "your-username" \\
    --github-token "ghp_xxx" \\
    --main-url "https://geminiai.asia/list/#/home" \\
    --nav-url "https://chatgpt-plus.top/"

  # 使用配置文件
  bun publish.ts --config config.json
`);
}

async function main(): Promise<void> {
  console.log(`
========================================
  AI Mirror Site Publisher
  一键生成图文并茂的AI镜像站指南
========================================
`);

  const config = parseArgs();
  if (!config) {
    process.exit(0);
  }

  // 验证必需参数
  if (!config.ai_tools || config.ai_tools.length === 0) {
    console.error('错误: --tools 是必需的');
    process.exit(1);
  }
  if (!config.github_username) {
    console.error('错误: --github-user 是必需的');
    process.exit(1);
  }
  if (!config.github_token) {
    console.error('错误: --github-token 是必需的');
    process.exit(1);
  }
  if (!config.mirror_urls?.main) {
    console.error('错误: --main-url 是必需的');
    process.exit(1);
  }
  if (!config.mirror_urls?.nav) {
    console.error('错误: --nav-url 是必需的');
    process.exit(1);
  }

  const fullConfig = config as Config;

  console.log(`配置信息:`);
  console.log(`  AI工具: ${fullConfig.ai_tools.join(', ')}`);
  console.log(`  GitHub用户: ${fullConfig.github_username}`);
  console.log(`  主入口: ${fullConfig.mirror_urls.main}`);
  console.log(`  导航入口: ${fullConfig.mirror_urls.nav}`);
  console.log(`  输出目录: ${fullConfig.base_directory || './ai-mirror-repos'}`);
  console.log(`\n开始批量处理...\n`);

  const results: Array<{ tool: string; success: boolean; repoUrl?: string }> = [];
  const startTime = Date.now();

  for (let i = 0; i < fullConfig.ai_tools.length; i++) {
    const tool = fullConfig.ai_tools[i]!;
    console.log(`[${i + 1}/${fullConfig.ai_tools.length}] 处理 ${tool}...`);
    
    const result = await processAITool(tool, fullConfig);
    results.push({ tool, ...result });
  }

  const endTime = Date.now();
  const duration = Math.round((endTime - startTime) / 1000);

  console.log(`
========================================
✅ 完成！
========================================
`);

  const successCount = results.filter(r => r.success).length;
  console.log(`成功: ${successCount}/${results.length}`);
  console.log(`耗时: ${duration}秒\n`);

  if (successCount > 0) {
    console.log(`📦 仓库列表:`);
    results.forEach((r, i) => {
      if (r.success && r.repoUrl) {
        console.log(`${i + 1}. ${r.repoUrl}`);
      }
    });
  }

  if (successCount < results.length) {
    console.log(`\n⚠️  失败的工具:`);
    results.forEach(r => {
      if (!r.success) {
        console.log(`- ${r.tool}`);
      }
    });
  }

  console.log(`
========================================
`);
}

await main().catch((err) => {
  console.error(`\n错误: ${err.message}`);
  process.exit(1);
});
