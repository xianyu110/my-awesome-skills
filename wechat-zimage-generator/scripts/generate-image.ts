#!/usr/bin/env bun
import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

const BASE_URL = 'https://api-inference.modelscope.cn/';
const API_KEY = process.env.ZIMAGE_API_KEY || 'ms-YOUR_MODELSCOPE_KEY_HERE';

interface GenerateOptions {
  prompt: string;
  model?: string;
  output?: string;
  size?: string;
  style?: string;
}

async function generateImage(options: GenerateOptions): Promise<string> {
  const { prompt, model = 'Tongyi-MAI/Z-Image-Turbo', output = 'generated-image.jpg' } = options;

  console.log(`[zimage] Generating image with prompt: "${prompt}"`);
  console.log(`[zimage] Model: ${model}`);

  // Step 1: Submit generation task
  const submitResponse = await fetch(`${BASE_URL}v1/images/generations`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${API_KEY}`,
      'Content-Type': 'application/json',
      'X-ModelScope-Async-Mode': 'true',
    },
    body: JSON.stringify({
      model,
      prompt,
    }),
  });

  if (!submitResponse.ok) {
    const error = await submitResponse.text();
    throw new Error(`Failed to submit task: ${submitResponse.status} ${error}`);
  }

  const { task_id } = await submitResponse.json();
  console.log(`[zimage] Task submitted: ${task_id}`);

  // Step 2: Poll for completion
  let attempts = 0;
  const maxAttempts = 60; // 5 minutes max

  while (attempts < maxAttempts) {
    await new Promise(resolve => setTimeout(resolve, 5000)); // Wait 5 seconds
    attempts++;

    const statusResponse = await fetch(`${BASE_URL}v1/tasks/${task_id}`, {
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
        'X-ModelScope-Task-Type': 'image_generation',
      },
    });

    if (!statusResponse.ok) {
      throw new Error(`Failed to check status: ${statusResponse.status}`);
    }

    const data = await statusResponse.json();
    console.log(`[zimage] Status: ${data.task_status} (attempt ${attempts}/${maxAttempts})`);

    if (data.task_status === 'SUCCEED') {
      console.log(`[zimage] Generation succeeded!`);
      
      // Download image
      const imageUrl = data.output_images[0];
      const imageResponse = await fetch(imageUrl);
      const imageBuffer = Buffer.from(await imageResponse.arrayBuffer());
      
      // Save to file
      const outputPath = path.resolve(process.cwd(), output);
      fs.writeFileSync(outputPath, imageBuffer);
      console.log(`[zimage] Image saved to: ${outputPath}`);
      
      return outputPath;
    } else if (data.task_status === 'FAILED') {
      throw new Error(`Image generation failed: ${JSON.stringify(data)}`);
    }
  }

  throw new Error('Generation timeout after 5 minutes');
}

function printUsage(): void {
  console.log(`Generate images using Z-Image API for WeChat articles

Usage:
  bun generate-image.ts --prompt "描述" [options]

Options:
  --prompt <text>    Image description (required)
  --model <name>     Model name (default: Tongyi-MAI/Z-Image-Turbo)
  --output <path>    Output file path (default: generated-image.jpg)
  --style <style>    Style preset (cover, illustration, photo)
  --help             Show this help

Environment:
  ZIMAGE_API_KEY     ModelScope API key (default: built-in)

Examples:
  # Generate cover image
  bun generate-image.ts --prompt "科技感的AI大脑" --style cover

  # Generate article illustration
  bun generate-image.ts --prompt "温馨的办公场景" --style illustration --output article-1.jpg

  # Custom prompt
  bun generate-image.ts --prompt "A golden cat sitting on a laptop"
`);
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);

  if (args.includes('--help') || args.includes('-h') || args.length === 0) {
    printUsage();
    process.exit(0);
  }

  let prompt = '';
  let model = 'Tongyi-MAI/Z-Image-Turbo';
  let output = 'generated-image.jpg';
  let style: string | undefined;

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--prompt' && args[i + 1]) {
      prompt = args[++i]!;
    } else if (arg === '--model' && args[i + 1]) {
      model = args[++i]!;
    } else if (arg === '--output' && args[i + 1]) {
      output = args[++i]!;
    } else if (arg === '--style' && args[i + 1]) {
      style = args[++i]!;
    }
  }

  if (!prompt) {
    console.error('Error: --prompt is required');
    process.exit(1);
  }

  // Apply style presets
  if (style === 'cover') {
    prompt = `公众号封面图，${prompt}，高质量，专业设计，16:9比例`;
  } else if (style === 'illustration') {
    prompt = `文章配图，${prompt}，清晰明亮，插画风格`;
  } else if (style === 'photo') {
    prompt = `摄影作品，${prompt}，高清，专业摄影`;
  }

  await generateImage({ prompt, model, output });
}

await main().catch((err) => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
