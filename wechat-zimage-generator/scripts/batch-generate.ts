#!/usr/bin/env bun
import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { spawnSync } from 'node:child_process';

interface ImageTask {
  prompt: string;
  output: string;
  style?: string;
}

interface BatchConfig {
  images: ImageTask[];
  outputDir?: string;
}

async function batchGenerate(configPath: string): Promise<void> {
  const configContent = fs.readFileSync(configPath, 'utf-8');
  const config: BatchConfig = JSON.parse(configContent);

  const outputDir = config.outputDir || './generated-images';
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  console.log(`[batch] Generating ${config.images.length} images...`);

  const scriptDir = path.dirname(new URL(import.meta.url).pathname);
  const scriptPath = path.join(scriptDir, 'generate-image.ts');

  for (let i = 0; i < config.images.length; i++) {
    const task = config.images[i]!;
    const outputPath = path.join(outputDir, task.output);

    console.log(`\n[batch] [${i + 1}/${config.images.length}] Generating: ${task.output}`);
    console.log(`[batch] Prompt: ${task.prompt}`);

    const args = [scriptPath, '--prompt', task.prompt, '--output', outputPath];
    if (task.style) {
      args.push('--style', task.style);
    }

    const result = spawnSync('bun', args, { stdio: 'inherit' });

    if (result.status !== 0) {
      console.error(`[batch] Failed to generate ${task.output}`);
      continue;
    }

    console.log(`[batch] ✓ Generated: ${outputPath}`);
  }

  console.log(`\n[batch] Complete! All images saved to: ${outputDir}`);
}

function printUsage(): void {
  console.log(`Batch generate images from config file

Usage:
  bun batch-generate.ts <config.json>

Config format:
{
  "outputDir": "./images",
  "images": [
    {
      "prompt": "科技感的AI大脑",
      "output": "cover.jpg",
      "style": "cover"
    },
    {
      "prompt": "温馨的办公场景",
      "output": "illustration-1.jpg",
      "style": "illustration"
    }
  ]
}

Example:
  bun batch-generate.ts images-config.json
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

  await batchGenerate(configPath);
}

await main().catch((err) => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
