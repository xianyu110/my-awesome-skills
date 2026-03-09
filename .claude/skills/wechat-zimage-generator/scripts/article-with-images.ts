#!/usr/bin/env bun
import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { spawnSync } from 'node:child_process';

interface ArticleConfig {
  markdown: string;
  title?: string;
  author?: string;
  theme?: string;
  images: Array<{
    prompt: string;
    position?: 'cover' | 'inline';
    style?: 'cover' | 'illustration' | 'photo';
  }>;
  outputDir?: string;
}

async function generateArticleWithImages(configPath: string): Promise<void> {
  const configContent = fs.readFileSync(configPath, 'utf-8');
  const config: ArticleConfig = JSON.parse(configContent);

  const outputDir = config.outputDir || './article-output';
  const imagesDir = path.join(outputDir, 'images');
  
  // Create directories
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  if (!fs.existsSync(imagesDir)) {
    fs.mkdirSync(imagesDir, { recursive: true });
  }

  console.log(`[article] Processing: ${config.markdown}`);
  console.log(`[article] Output directory: ${outputDir}`);

  // Step 1: Generate all images
  console.log(`\n[article] Step 1: Generating ${config.images.length} images...`);
  
  const scriptDir = path.dirname(new URL(import.meta.url).pathname);
  const generateScript = path.join(scriptDir, 'generate-image.ts');

  const generatedImages: string[] = [];

  for (let i = 0; i < config.images.length; i++) {
    const img = config.images[i]!;
    const filename = `image-${i + 1}.jpg`;
    const outputPath = path.join(imagesDir, filename);

    console.log(`\n[article] [${i + 1}/${config.images.length}] Generating: ${filename}`);
    console.log(`[article] Prompt: ${img.prompt}`);

    const args = [generateScript, '--prompt', img.prompt, '--output', outputPath];
    if (img.style) {
      args.push('--style', img.style);
    }

    const result = spawnSync('bun', args, { stdio: 'inherit' });

    if (result.status !== 0) {
      console.error(`[article] Failed to generate ${filename}`);
      continue;
    }

    generatedImages.push(outputPath);
    console.log(`[article] ✓ Generated: ${outputPath}`);
  }

  // Step 2: Read and process markdown
  console.log(`\n[article] Step 2: Processing markdown...`);
  
  const markdownPath = path.resolve(process.cwd(), config.markdown);
  if (!fs.existsSync(markdownPath)) {
    throw new Error(`Markdown file not found: ${markdownPath}`);
  }

  let markdownContent = fs.readFileSync(markdownPath, 'utf-8');

  // Insert cover image if specified
  const coverImage = config.images.find(img => img.position === 'cover');
  if (coverImage) {
    const coverIndex = config.images.indexOf(coverImage);
    const coverPath = generatedImages[coverIndex];
    if (coverPath) {
      // Add cover image after title
      const lines = markdownContent.split('\n');
      let insertIndex = 0;
      
      // Find first heading
      for (let i = 0; i < lines.length; i++) {
        if (lines[i]?.startsWith('#')) {
          insertIndex = i + 1;
          break;
        }
      }
      
      lines.splice(insertIndex, 0, '', `![封面图](${path.relative(outputDir, coverPath!)})`);
      markdownContent = lines.join('\n');
    }
  }

  // Insert inline images
  const inlineImages = config.images.filter(img => img.position === 'inline' || !img.position);
  if (inlineImages.length > 0) {
    // Add images at the end or at specific markers
    const imageMarkdown = inlineImages
      .map((img, idx) => {
        const actualIndex = config.images.indexOf(img);
        const imagePath = generatedImages[actualIndex];
        if (!imagePath) return '';
        return `\n![配图${idx + 1}](${path.relative(outputDir, imagePath)})`;
      })
      .filter(Boolean)
      .join('\n');
    
    markdownContent += '\n' + imageMarkdown;
  }

  // Save processed markdown
  const processedMarkdownPath = path.join(outputDir, 'article-with-images.md');
  fs.writeFileSync(processedMarkdownPath, markdownContent, 'utf-8');
  console.log(`[article] ✓ Processed markdown saved: ${processedMarkdownPath}`);

  // Step 3: Generate publish command
  console.log(`\n[article] Step 3: Ready to publish!`);
  console.log(`\n[article] To publish to WeChat, run:`);
  console.log(`\nbun .claude/skills/baoyu-post-to-wechat/scripts/wechat-article.ts \\`);
  console.log(`  --markdown ${processedMarkdownPath} \\`);
  if (config.theme) {
    console.log(`  --theme ${config.theme} \\`);
  }
  if (config.author) {
    console.log(`  --author "${config.author}" \\`);
  }
  console.log(`  --submit`);

  // Create a publish script
  const publishScript = path.join(outputDir, 'publish.sh');
  const publishCommand = [
    '#!/bin/bash',
    '',
    'bun .claude/skills/baoyu-post-to-wechat/scripts/wechat-article.ts \\',
    `  --markdown ${processedMarkdownPath} \\`,
    config.theme ? `  --theme ${config.theme} \\` : '',
    config.author ? `  --author "${config.author}" \\` : '',
    '  --submit',
  ].filter(Boolean).join('\n');

  fs.writeFileSync(publishScript, publishCommand, 'utf-8');
  fs.chmodSync(publishScript, 0o755);
  console.log(`\n[article] ✓ Publish script created: ${publishScript}`);
  console.log(`[article] Run: bash ${publishScript}`);

  // Summary
  console.log(`\n[article] ========== Summary ==========`);
  console.log(`[article] Generated images: ${generatedImages.length}`);
  console.log(`[article] Processed markdown: ${processedMarkdownPath}`);
  console.log(`[article] Publish script: ${publishScript}`);
  console.log(`[article] ==============================\n`);
}

function printUsage(): void {
  console.log(`Generate images and prepare article for WeChat publication

Usage:
  bun article-with-images.ts <config.json>

Config format:
{
  "markdown": "./article.md",
  "title": "文章标题",
  "author": "作者名",
  "theme": "grace",
  "outputDir": "./article-output",
  "images": [
    {
      "prompt": "科技感的AI大脑",
      "position": "cover",
      "style": "cover"
    },
    {
      "prompt": "程序员写代码的场景",
      "position": "inline",
      "style": "illustration"
    }
  ]
}

Position options:
  - cover: Insert after title as cover image
  - inline: Insert in article body (default)

Example:
  bun article-with-images.ts my-article-config.json
`);
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);

  if (args.includes('--help') || args.includes('-h') || args.length === 0) {
    printUsage();
    process.exit(0);
  }

  const configPath = args[0]!;
  if (!fs.existsSync(configPath)) {
    console.error(`Error: Config file not found: ${configPath}`);
    process.exit(1);
  }

  await generateArticleWithImages(configPath);
}

await main().catch((err) => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
