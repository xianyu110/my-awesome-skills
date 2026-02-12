#!/usr/bin/env bun
import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { spawnSync } from 'node:child_process';

const BASE_URL = 'https://api-inference.modelscope.cn/';
const API_KEY = process.env.ZIMAGE_API_KEY || 'ms-YOUR_MODELSCOPE_KEY_HERE';

interface TopicConfig {
  topic: string;
  keywords?: string[];
  style?: 'tech' | 'business' | 'education' | 'lifestyle';
  imageCount?: number;
  outputDir?: string;
  author?: string;
  theme?: 'default' | 'grace' | 'simple';
}

interface ArticleStructure {
  title: string;
  sections: Array<{
    heading: string;
    content: string;
    needsImage: boolean;
    imagePrompt?: string;
  }>;
  conclusion: string;
}

async function generateImage(prompt: string, outputPath: string): Promise<void> {
  console.log(`[image] Generating: ${path.basename(outputPath)}`);
  
  const submitResponse = await fetch(`${BASE_URL}v1/images/generations`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${API_KEY}`,
      'Content-Type': 'application/json',
      'X-ModelScope-Async-Mode': 'true',
    },
    body: JSON.stringify({
      model: 'Tongyi-MAI/Z-Image-Turbo',
      prompt,
    }),
  });

  if (!submitResponse.ok) {
    throw new Error(`Failed to submit: ${submitResponse.status}`);
  }

  const { task_id } = await submitResponse.json();

  let attempts = 0;
  while (attempts < 60) {
    await new Promise(resolve => setTimeout(resolve, 5000));
    attempts++;

    const statusResponse = await fetch(`${BASE_URL}v1/tasks/${task_id}`, {
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
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
      console.log(`[image] ✓ Saved: ${outputPath}`);
      return;
    } else if (data.task_status === 'FAILED') {
      throw new Error('Generation failed');
    }
  }

  throw new Error('Timeout');
}

function generateArticleStructure(config: TopicConfig): ArticleStructure {
  const { topic, style = 'tech', imageCount = 5 } = config;
  
  // 根据风格生成不同的文章结构
  const styleTemplates: Record<string, { title: string; sections: Array<{ heading: string; needsImage: boolean; imageType?: string }> }> = {
    tech: {
      title: `${topic}：技术革新与未来展望 🚀`,
      sections: [
        { heading: '技术背景', needsImage: true, imageType: 'cover' },
        { heading: '核心功能', needsImage: true, imageType: 'feature' },
        { heading: '实际应用', needsImage: true, imageType: 'application' },
        { heading: '技术优势', needsImage: false },
        { heading: '未来发展', needsImage: true, imageType: 'future' },
      ],
    },
    business: {
      title: `${topic}：商业价值与市场机遇 💼`,
      sections: [
        { heading: '市场概况', needsImage: true, imageType: 'cover' },
        { heading: '商业模式', needsImage: true, imageType: 'business' },
        { heading: '成功案例', needsImage: true, imageType: 'case' },
        { heading: '投资价值', needsImage: false },
        { heading: '发展趋势', needsImage: true, imageType: 'trend' },
      ],
    },
    education: {
      title: `${topic}：学习指南与实践技巧 📚`,
      sections: [
        { heading: '基础概念', needsImage: true, imageType: 'cover' },
        { heading: '学习路径', needsImage: true, imageType: 'path' },
        { heading: '实践案例', needsImage: true, imageType: 'practice' },
        { heading: '常见问题', needsImage: false },
        { heading: '进阶建议', needsImage: true, imageType: 'advanced' },
      ],
    },
    lifestyle: {
      title: `${topic}：生活方式与品质提升 ✨`,
      sections: [
        { heading: '生活场景', needsImage: true, imageType: 'cover' },
        { heading: '实用技巧', needsImage: true, imageType: 'tips' },
        { heading: '体验分享', needsImage: true, imageType: 'experience' },
        { heading: '注意事项', needsImage: false },
        { heading: '推荐建议', needsImage: true, imageType: 'recommendation' },
      ],
    },
    notion: {
      title: `${topic} 📖`,
      sections: [
        { heading: '概述', needsImage: true, imageType: 'cover' },
        { heading: '核心内容', needsImage: true, imageType: 'feature' },
        { heading: '实践指南', needsImage: true, imageType: 'application' },
        { heading: '注意事项', needsImage: false },
        { heading: '总结建议', needsImage: true, imageType: 'future' },
      ],
    },
  };

  const template = styleTemplates[style] || styleTemplates.tech;
  
  return {
    title: template.title,
    sections: template.sections.map(s => ({
      heading: s.heading,
      content: `[此处应包含关于${s.heading}的详细内容，约300-500字]`,
      needsImage: s.needsImage,
      imagePrompt: s.needsImage ? generateImagePrompt(topic, s.imageType!, style) : undefined,
    })),
    conclusion: `[总结${topic}的核心价值和未来展望]`,
  };
}

function generateImagePrompt(topic: string, imageType: string, style: string): string {
  // 基于 baoyu-article-illustrator 的9种专业风格
  const styleConfigs: Record<string, { colors: string; elements: string; mood: string }> = {
    tech: {
      colors: '深蓝电光青紫色，深灰近黑背景',
      elements: '电路图案，数据节点，几何网格，发光效果',
      mood: '现代未来感，科技专业',
    },
    business: {
      colors: '柔和珊瑚色静谧青色，温暖奶油背景',
      elements: '精致线条，优雅图标，微妙渐变，平衡留白',
      mood: '专业成熟，商务优雅',
    },
    education: {
      colors: '粉彩粉薄荷薰衣草天蓝，浅奶油背景',
      elements: '涂鸦星星，可爱角色，对话气泡，手绘线条',
      mood: '有趣活泼，友好温馨',
    },
    lifestyle: {
      colors: '温暖橙金黄陶土色，奶油柔和桃背景',
      elements: '圆润形状，微笑面孔，阳光光芒，爱心',
      mood: '温馨友好，生活气息',
    },
  };

  const config = styleConfigs[style] || styleConfigs.tech;
  
  const imageTypePrompts: Record<string, string> = {
    cover: `${topic}，${config.colors}，${config.elements}，${config.mood}，高质量专业设计，16:9横版`,
    feature: `${topic}功能展示，notion风格，极简手绘线条，黑色线条白色背景，浅蓝浅黄点缀，几何图形，最大化留白，清晰明了，16:9横版`,
    application: `${topic}应用场景，${config.colors}，实际使用场景，${config.elements}，${config.mood}，16:9横版`,
    future: `${topic}未来发展，tech科技风格，深蓝电光青色，深灰背景，数据节点上升曲线，发光效果，积极向上未来感，16:9横版`,
    business: `${topic}商业模式，minimal极简风格，纯黑纯白，白色背景，流程图数据可视化，细而精确线条，专业清晰，16:9横版`,
    case: `${topic}成功案例，warm温暖风格，温暖橙金黄色，奶油背景，团队协作场景，圆润形状，专业高效，16:9横版`,
    trend: `${topic}发展趋势，tech科技风格，深蓝电光青色，深灰背景，数据图表上升曲线，发光效果，积极向上，16:9横版`,
    path: `${topic}学习路径，notion风格，极简手绘线条，黑色线条白色背景，浅蓝点缀，几何图形箭头，思维导图，清晰明了，16:9横版`,
    practice: `${topic}实践场景，warm温暖风格，温暖橙金黄色，奶油背景，学习场景，专注认真氛围，温馨明亮，16:9横版`,
    advanced: `${topic}进阶技巧，tech科技风格，深蓝电光青色，深灰背景，创新概念，几何图形，知识升级感，16:9横版`,
    tips: `${topic}实用技巧，playful趣味风格，粉彩粉薄荷色，浅奶油背景，涂鸦星星，简洁清晰，有趣活泼，16:9横版`,
    experience: `${topic}体验分享，warm温暖风格，温暖橙金黄色，奶油背景，真实场景，温暖舒适，生活气息，16:9横版`,
    recommendation: `${topic}推荐建议，elegant优雅风格，柔和珊瑚色静谧青色，温暖奶油背景，精致图标，品质生活，16:9横版`,
  };

  return imageTypePrompts[imageType] || `${topic}，${config.colors}，${config.elements}，${config.mood}，专业设计，16:9横版`;
}

async function generateArticleContent(config: TopicConfig): Promise<string> {
  console.log(`\n[article] 正在生成文章内容...`);
  console.log(`[article] 主题: ${config.topic}`);
  console.log(`[article] 风格: ${config.style || 'tech'}`);
  
  const structure = generateArticleStructure(config);
  
  let markdown = `---\n`;
  markdown += `title: ${structure.title}\n`;
  markdown += `author: ${config.author || 'AI创作助手'}\n`;
  markdown += `date: ${new Date().toISOString().split('T')[0]}\n`;
  markdown += `---\n\n`;
  
  markdown += `# ${structure.title}\n\n`;
  
  // 添加引言
  markdown += `> 本文深入探讨${config.topic}的各个方面，为您提供全面的了解和实用的建议。\n\n`;
  markdown += `------\n\n`;
  
  // 生成各个章节
  structure.sections.forEach((section, index) => {
    markdown += `## ${index + 1}. ${section.heading}\n\n`;
    markdown += `${section.content}\n\n`;
    
    if (section.needsImage) {
      markdown += `![${section.heading}](images/section-${index + 1}.jpg)\n\n`;
    }
    
    markdown += `------\n\n`;
  });
  
  // 添加总结
  markdown += `## 总结\n\n`;
  markdown += `${structure.conclusion}\n\n`;
  markdown += `------\n\n`;
  
  // 添加互动引导
  markdown += `**你对${config.topic}有什么看法？欢迎在评论区分享！👇**\n\n`;
  markdown += `**觉得有用的话，点个赞、转发给需要的朋友！💪**\n`;
  
  return markdown;
}

async function generateImages(config: TopicConfig, outputDir: string): Promise<void> {
  console.log(`\n[images] 开始生成配图...`);
  
  const structure = generateArticleStructure(config);
  const imagesDir = path.join(outputDir, 'images');
  
  if (!fs.existsSync(imagesDir)) {
    fs.mkdirSync(imagesDir, { recursive: true });
  }
  
  let imageIndex = 0;
  for (let i = 0; i < structure.sections.length; i++) {
    const section = structure.sections[i]!;
    if (section.needsImage && section.imagePrompt) {
      imageIndex++;
      const imagePath = path.join(imagesDir, `section-${i + 1}.jpg`);
      
      try {
        await generateImage(section.imagePrompt, imagePath);
      } catch (err) {
        console.error(`[images] ✗ Failed: ${err instanceof Error ? err.message : String(err)}`);
      }
    }
  }
  
  console.log(`[images] ✓ 完成！共生成 ${imageIndex} 张图片`);
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  
  if (args.includes('--help') || args.includes('-h') || args.length === 0) {
    console.log(`从选题到发布：一键生成图文并茂的公众号文章

用法:
  bun topic-to-article.ts --topic "主题" [选项]

选项:
  --topic <text>      文章主题（必需）
  --style <type>      文章风格: tech, business, education, lifestyle (默认: tech)
  --images <n>        配图数量 (默认: 5)
  --author <name>     作者名称 (默认: AI创作助手)
  --theme <name>      公众号主题: default, grace, simple (默认: grace)
  --output <dir>      输出目录 (默认: ./articles/主题名)
  --keywords <words>  关键词，逗号分隔
  --help              显示帮助

示例:
  # 生成科技类文章
  bun topic-to-article.ts --topic "Claude Cowork" --style tech

  # 生成教育类文章
  bun topic-to-article.ts --topic "Python编程入门" --style education --images 6

  # 生成商业类文章
  bun topic-to-article.ts --topic "AI创业机会" --style business --author "商业观察"
`);
    process.exit(0);
  }
  
  const config: TopicConfig = {
    topic: '',
    style: 'tech',
    imageCount: 5,
    author: 'AI创作助手',
    theme: 'grace',
  };
  
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--topic' && args[i + 1]) {
      config.topic = args[++i]!;
    } else if (arg === '--style' && args[i + 1]) {
      config.style = args[++i] as any;
    } else if (arg === '--images' && args[i + 1]) {
      config.imageCount = parseInt(args[++i]!, 10);
    } else if (arg === '--author' && args[i + 1]) {
      config.author = args[++i];
    } else if (arg === '--theme' && args[i + 1]) {
      config.theme = args[++i] as any;
    } else if (arg === '--output' && args[i + 1]) {
      config.outputDir = args[++i];
    } else if (arg === '--keywords' && args[i + 1]) {
      config.keywords = args[++i]!.split(',').map(k => k.trim());
    }
  }
  
  if (!config.topic) {
    console.error('错误: --topic 是必需的');
    process.exit(1);
  }
  
  // 设置输出目录
  const outputDir = config.outputDir || path.join('./articles', config.topic.replace(/[^a-zA-Z0-9\u4e00-\u9fa5]/g, '-'));
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  console.log(`\n========================================`);
  console.log(`  📝 一键生成图文并茂的公众号文章`);
  console.log(`========================================`);
  console.log(`主题: ${config.topic}`);
  console.log(`风格: ${config.style}`);
  console.log(`配图: ${config.imageCount} 张`);
  console.log(`输出: ${outputDir}`);
  console.log(`========================================\n`);
  
  // 步骤1: 生成文章内容
  const articleContent = await generateArticleContent(config);
  const articlePath = path.join(outputDir, `${config.topic}.md`);
  fs.writeFileSync(articlePath, articleContent, 'utf-8');
  console.log(`[article] ✓ 文章已生成: ${articlePath}`);
  
  // 步骤2: 生成配图
  await generateImages(config, outputDir);
  
  // 步骤3: 生成发布脚本
  const publishScript = path.join(outputDir, 'publish.sh');
  const publishCommand = [
    '#!/bin/bash',
    '',
    '# 发布到微信公众号',
    'bun ../../.claude/skills/baoyu-post-to-wechat/scripts/wechat-article.ts \\',
    `  --markdown "${config.topic}.md" \\`,
    `  --theme ${config.theme} \\`,
    `  --author "${config.author}" \\`,
    '  --submit',
  ].join('\n');
  
  fs.writeFileSync(publishScript, publishCommand, 'utf-8');
  fs.chmodSync(publishScript, 0o755);
  
  console.log(`\n========================================`);
  console.log(`  ✅ 完成！`);
  console.log(`========================================`);
  console.log(`文章: ${articlePath}`);
  console.log(`配图: ${path.join(outputDir, 'images/')}`);
  console.log(`发布: bash ${publishScript}`);
  console.log(`========================================\n`);
  
  console.log(`💡 提示: 请编辑文章内容，补充详细信息后再发布`);
}

await main().catch((err) => {
  console.error(`错误: ${err.message}`);
  process.exit(1);
});
