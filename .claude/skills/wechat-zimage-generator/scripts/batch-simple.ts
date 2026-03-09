#!/usr/bin/env bun
import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

const BASE_URL = 'https://api-inference.modelscope.cn/';
const API_KEY = process.env.ZIMAGE_API_KEY || 'ms-YOUR_MODELSCOPE_KEY_HERE';

interface ImageTask {
  prompt: string;
  output: string;
}

interface BatchConfig {
  images: ImageTask[];
  outputDir?: string;
}

async function generateImage(prompt: string, outputPath: string): Promise<void> {
  console.log(`[generate] Prompt: ${prompt}`);
  
  // Submit task
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
  console.log(`[generate] Task ID: ${task_id}`);

  // Poll for completion
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
    console.log(`[generate] Status: ${data.task_status} (${attempts}/60)`);

    if (data.task_status === 'SUCCEED') {
      const imageUrl = data.output_images[0];
      const imageResponse = await fetch(imageUrl);
      const imageBuffer = Buffer.from(await imageResponse.arrayBuffer());
      fs.writeFileSync(outputPath, imageBuffer);
      console.log(`[generate] ✓ Saved: ${outputPath}`);
      return;
    } else if (data.task_status === 'FAILED') {
      throw new Error('Generation failed');
    }
  }

  throw new Error('Timeout');
}

async function main(): Promise<void> {
  const configPath = process.argv[2];
  if (!configPath) {
    console.error('Usage: bun batch-simple.ts <config.json>');
    process.exit(1);
  }

  const config: BatchConfig = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
  const outputDir = config.outputDir || './';

  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  console.log(`[batch] Generating ${config.images.length} images...\n`);

  for (let i = 0; i < config.images.length; i++) {
    const task = config.images[i]!;
    const outputPath = path.join(outputDir, task.output);

    console.log(`\n[batch] [${i + 1}/${config.images.length}] ${task.output}`);
    
    try {
      await generateImage(task.prompt, outputPath);
    } catch (err) {
      console.error(`[batch] ✗ Failed: ${err instanceof Error ? err.message : String(err)}`);
    }
  }

  console.log(`\n[batch] Complete!`);
}

await main().catch((err) => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
