#!/usr/bin/env bun
/**
 * 根据选题生成图文并茂的公众号文章
 * 用法: bun article-generator.ts <topic> [options]
 */

interface ArticleImage {
  prompt: string;
  position: string;
  style: 'cover' | 'illustration' | 'photo';
  filename: string;
}

interface ArticleConfig {
  topic: string;
  style?: string;
  imageCount?: number;
  outputDir: string;
  author: string;
  theme?: string;
}

class ArticleGenerator {
  private config: ArticleConfig;
  private images: ArticleImage[] = [];

  constructor(config: ArticleConfig) {
    this.config = config;
  }

  async generate(): Promise<void> {
    console.log(`[article-gen] 开始生成文章: ${this.config.topic}`);

    // Step 1: 生成文章内容
    console.log('[article-gen] Step 1: 生成文章内容...');
    const articleContent = await this.generateArticleContent();

    // Step 2: 分析文章，确定配图位置和提示词
    console.log('[article-gen] Step 2: 分析配图需求...');
    this.analyzeImageNeeds(articleContent);

    // Step 3: 生成配图
    console.log(`[article-gen] Step 3: 生成 ${this.images.length} 张配图...`);
    await this.generateImages();

    // Step 4: 组装最终文章
    console.log('[article-gen] Step 4: 组装最终文章...');
    const finalArticle = this.assembleFinalArticle(articleContent);

    // Step 5: 保存文章
    const articlePath = await this.saveArticle(finalArticle);
    console.log(`[article-gen] ✅ 文章已生成: ${articlePath}`);

    // Step 6: 生成发布脚本
    await this.generatePublishScript(articlePath);
  }

  private async generateArticleContent(): Promise<string> {
    const prompt = `
请根据以下选题，写一篇高质量的公众号文章：

选题：${this.config.topic}

要求：
1. 标题：15-25字，吸引眼球但不做标题党
2. 开头：用故事、问题或数据引入
3. 正文：使用小标题分段，每段3-5行
4. 结尾：包含行动号召（CTA）
5. 使用emoji表情适度增强互动感：✨💡🎯 等
6. 重要内容用**加粗**强调
7. 全文1500-3000字
8. 每段不超过150字，保持阅读节奏
9. 多用"你""我们"拉近距离

格式要求：
- 一级标题：文章主标题
- 二级标题：段落小标题
- 每3-4段加一个小标题
- 用 <!-- IMAGE --> 标记需要配图的位置

请直接输出markdown格式的���章。
`;

    // 这里需要调用AI生成文章
    // 暂时返回示例内容
    return this.generateSampleArticle();
  }

  private generateSampleArticle(): string {
    return `# ${this.config.topic}

✨ 你是否曾经想过，${this.config.topic}可以如此简单？

## 为什么选择我们？

在当今快速发展的时代，**掌握核心技术**变得越来越重要。我们提供了一套完整的解决方案。

<!-- IMAGE -->

### 核心优势

1. **简单易用** - 无需复杂的学习过程
2. **高效便捷** - 节省80%的时间
3. **专业可靠** - 经过大量验证

## 实战应用

让我们来看看具体的应用场景。

<!-- IMAGE -->

### 场景一：日常工作

在日常工作中，你可以通过以下方式提升效率：

- 制定明确的计划
- 使用合适的工具
- 持续优化流程

### 场景二：学习成长

学习是一个持续的过程，需要：

- 保持好奇心
- 勇于尝试
- 总结反思

## 总结

${this.config.topic}并不难，关键是要**付诸行动**。

💡 **行动建议**：
1. 从小处着手
2. 持续迭代
3. 寻求反馈

如果觉得有帮助，欢迎**点赞、在看、转发**，让更多人看到！

我们下期再见！👋`;
  }

  private analyzeImageNeeds(content: string): void {
    const imagePositions: ArticleImage[] = [];
    const imageCount = this.config.imageCount || 3;

    // 生成封面图
    imagePositions.push({
      prompt: `${this.config.topic}，公众号封面图，蓝色科技感，高质量`,
      position: 'cover',
      style: 'cover',
      filename: 'cover.jpg'
    });

    // 为每个 IMAGE 标记生成配图
    let imageIndex = 1;
    const lines = content.split('\n');
    let sectionTitle = '';

    for (const line of lines) {
      if (line.startsWith('## ')) {
        sectionTitle = line.replace('## ', '').trim();
      } else if (line.includes('<!-- IMAGE -->') && imageIndex <= imageCount) {
        imagePositions.push({
          prompt: `${sectionTitle}，插画风格，清晰明亮`,
          position: `section-${imageIndex}`,
          style: 'illustration',
          filename: `image-${imageIndex}.jpg`
        });
        imageIndex++;
      }
    }

    this.images = imagePositions;
  }

  private async generateImages(): Promise<void> {
    const { GenerateImage } = await import('./generate-image.ts');

    for (let i = 0; i < this.images.length; i++) {
      const image = this.images[i];
      console.log(`[article-gen] [${i + 1}/${this.images.length}] 生成: ${image.filename}`);

      try {
        const imagePath = await GenerateImage({
          prompt: image.prompt,
          style: image.style,
          output: `${this.config.outputDir}/${image.filename}`
        });

        console.log(`[article-gen] ✅ 已生成: ${imagePath}`);
      } catch (error) {
        console.error(`[article-gen] ❌ 生成失败: ${image.filename}`, error);
      }
    }
  }

  private assembleFinalArticle(content: string): string {
    let finalContent = content;
    let imageIndex = 0;

    // 替换封面图
    if (this.images.length > 0 && this.images[0].position === 'cover') {
      const coverImage = this.images[0];
      finalContent = `![封面图](${coverImage.filename})\n\n${finalContent}`;
      imageIndex++;
    }

    // 替换内容配图
    finalContent = finalContent.replace(/<!-- IMAGE -->/g, () => {
      if (imageIndex < this.images.length) {
        const image = this.images[imageIndex];
        imageIndex++;
        return `![配图](${image.filename})`;
      }
      return '';
    });

    return finalContent;
  }

  private async saveArticle(content: string): Promise<string> {
    const fs = await import('fs');
    const path = await import('path');

    const filename = `${Date.now()}.md`;
    const articlePath = path.join(this.config.outputDir, filename);

    await fs.promises.mkdir(this.config.outputDir, { recursive: true });
    await fs.promises.writeFile(articlePath, content, 'utf-8');

    return articlePath;
  }

  private async generatePublishScript(articlePath: string): Promise<void> {
    const fs = await import('fs');
    const path = await import('path');

    const scriptContent = `#!/bin/bash
# 发布到公众号
bun .claude/skills/baoyu-post-to-wechat/scripts/wechat-article.ts \\
  --markdown "${articlePath}" \\
  --theme ${this.config.theme || 'grace'} \\
  --author "${this.config.author}" \\
  --submit
`;

    const scriptPath = path.join(this.config.outputDir, 'publish.sh');
    await fs.promises.writeFile(scriptPath, scriptContent, 'utf-8');
    await fs.promises.chmod(scriptPath, 0o755);

    console.log(`[article-gen] 📝 发布脚本: ${scriptPath}`);
  }
}

// CLI 入口
async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log('用法: bun article-generator.ts <topic> [options]');
    console.log('');
    console.log('选项:');
    console.log('  --style <style>       配图风格 (cover|illustration|photo)');
    console.log('  --image-count <n>     配图数量 (默认: 3)');
    console.log('  --output-dir <dir>    输出目录 (默认: ./output)');
    console.log('  --author <name>       作者名称 (默认: AI助手)');
    console.log('  --theme <theme>       公众号主题 (默认: grace)');
    process.exit(1);
  }

  const topic = args[0];
  const config: ArticleConfig = {
    topic,
    outputDir: './output',
    author: 'AI助手',
    theme: 'grace'
  };

  // 解析选项
  for (let i = 1; i < args.length; i += 2) {
    const key = args[i];
    const value = args[i + 1];

    switch (key) {
      case '--style':
        // config.style = value;
        break;
      case '--image-count':
        config.imageCount = parseInt(value);
        break;
      case '--output-dir':
        config.outputDir = value;
        break;
      case '--author':
        config.author = value;
        break;
      case '--theme':
        config.theme = value;
        break;
    }
  }

  const generator = new ArticleGenerator(config);
  await generator.generate();
}

main().catch(console.error);
