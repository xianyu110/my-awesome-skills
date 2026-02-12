#!/usr/bin/env ts-node

import * as fs from 'fs';
import * as path from 'path';

interface Config {
  fetchMethod: 'python' | 'jina';
  pythonCrawlerPath?: string;
  jinaApiKey?: string;
  aiProvider: 'anthropic' | 'openai';
  apiKey: string;
  model: string;
  removeWatermarks: boolean;
  watermarkKeywords: string[];
}

interface RewriteOptions {
  url: string;
  mode: 'light' | 'medium' | 'deep' | 'style';
  output?: string;
}

// 加载配置
function loadConfig(): Config {
  const configPath = path.join(__dirname, '../config.json');
  if (!fs.existsSync(configPath)) {
    console.error('❌ 配置文件不存在，请创建 config.json');
    process.exit(1);
  }
  return JSON.parse(fs.readFileSync(configPath, 'utf-8'));
}

// 使用 Python 爬虫抓取文章
async function fetchArticleWithPython(url: string, crawlerPath: string): Promise<string> {
  console.log('📥 使用 Python 爬虫抓取文章...');
  
  const { execSync } = require('child_process');
  const tempFile = path.join(__dirname, '../temp_article.txt');
  
  try {
    // 调用 Python 爬虫
    const pythonScript = path.join(crawlerPath, 'main.py');
    const command = `cd ${crawlerPath} && source venv/bin/activate && python ${pythonScript} --url "${url}" --output "${tempFile}"`;
    
    execSync(command, { encoding: 'utf-8' });
    
    // 读取抓取结果
    if (fs.existsSync(tempFile)) {
      const content = fs.readFileSync(tempFile, 'utf-8');
      fs.unlinkSync(tempFile); // 清理临时文件
      return content;
    } else {
      throw new Error('Python 爬虫未生成输出文件');
    }
  } catch (error) {
    console.error('Python 爬虫抓取失败，尝试使用 Jina Reader...');
    throw error;
  }
}

// 使用 Jina Reader 抓取文章
async function fetchArticleWithJina(url: string, apiKey?: string): Promise<string> {
  console.log('📥 使用 Jina Reader 抓取文章...');
  
  const jinaUrl = `https://r.jina.ai/${url}`;
  const headers: Record<string, string> = {
    'Accept': 'application/json',
  };
  
  if (apiKey) {
    headers['Authorization'] = `Bearer ${apiKey}`;
  }
  
  const response = await fetch(jinaUrl, { headers });
  
  if (!response.ok) {
    throw new Error(`抓取失败: ${response.statusText}`);
  }
  
  const data = await response.json();
  return data.data?.content || data.content || '';
}

// 使用 Jina Reader 抓取文章
async function fetchArticle(url: string, config: Config): Promise<string> {
  // 优先使用 Python 爬虫
  if (config.fetchMethod === 'python' && config.pythonCrawlerPath) {
    try {
      return await fetchArticleWithPython(url, config.pythonCrawlerPath);
    } catch (error) {
      console.log('⚠️  Python 爬虫失败，切换到 Jina Reader');
    }
  }
  
  // 使用 Jina Reader
  return await fetchArticleWithJina(url, config.jinaApiKey);
}

// 清理水印
function removeWatermarks(content: string, keywords: string[]): string {
  console.log('🧹 清理水印...');
  
  let cleaned = content;
  
  // 移除包含水印关键词的段落
  const lines = cleaned.split('\n');
  const filteredLines = lines.filter(line => {
    const lowerLine = line.toLowerCase();
    return !keywords.some(keyword => 
      lowerLine.includes(keyword.toLowerCase())
    );
  });
  
  cleaned = filteredLines.join('\n');
  
  // 移除常见的推广模式
  cleaned = cleaned.replace(/【.*?推荐.*?】/g, '');
  cleaned = cleaned.replace(/\*\*.*?关注.*?\*\*/g, '');
  cleaned = cleaned.replace(/!\[.*?二维码.*?\]\(.*?\)/g, '');
  
  // 清理多余空行
  cleaned = cleaned.replace(/\n{3,}/g, '\n\n');
  
  return cleaned.trim();
}

// 获取改写提示词
function getRewritePrompt(mode: string): string {
  const prompts = {
    light: `请对以下文章进行轻度润色：
- 保持90%的原文结构和表达
- 仅优化语句通顺度和用词准确性
- 不改变核心观点和论述逻辑
- 保留所有重要信息`,

    medium: `请对以下文章进行中度改写：
- 保持核心观点和主要论据
- 调整表达方式和句式结构
- 可以重新组织段落顺序
- 用自己的语言重新表述
- 保持文章的专业性和可读性`,

    deep: `请对以下文章进行深度改写：
- 提取核心观点和关键信息
- 完全重新组织内容结构
- 用全新的表达方式和案例
- 可以补充相关知识点
- 形成一篇全新的原创文章
- 保持逻辑严谨和信息准确`,

    style: `请对以下文章进行风格转换改写：
- 将正式的技术文章转换为轻松易懂的科普风格
- 使用更多比喻、类比和生活化的例子
- 增加互动性和趣味性
- 保持信息准确性
- 适合公众号阅读`
  };
  
  return prompts[mode as keyof typeof prompts] || prompts.medium;
}

// AI 改写
async function rewriteContent(
  content: string,
  mode: string,
  config: Config
): Promise<string> {
  console.log(`✍️  正在进行 ${mode} 模式改写...`);
  
  const prompt = getRewritePrompt(mode);
  const fullPrompt = `${prompt}

原文：
${content}

请直接输出改写后的文章，使用 Markdown 格式。`;

  if (config.aiProvider === 'anthropic') {
    return await rewriteWithClaude(fullPrompt, config);
  } else {
    return await rewriteWithOpenAI(fullPrompt, config);
  }
}

// 使用 Claude API 改写
async function rewriteWithClaude(prompt: string, config: Config): Promise<string> {
  const response = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': config.apiKey,
      'anthropic-version': '2023-06-01'
    },
    body: JSON.stringify({
      model: config.model,
      max_tokens: 4096,
      messages: [{
        role: 'user',
        content: prompt
      }]
    })
  });
  
  if (!response.ok) {
    throw new Error(`Claude API 调用失败: ${response.statusText}`);
  }
  
  const data = await response.json();
  return data.content[0].text;
}

// 使用 OpenAI API 改写
async function rewriteWithOpenAI(prompt: string, config: Config): Promise<string> {
  const response = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${config.apiKey}`
    },
    body: JSON.stringify({
      model: config.model,
      messages: [{
        role: 'user',
        content: prompt
      }],
      max_tokens: 4096
    })
  });
  
  if (!response.ok) {
    throw new Error(`OpenAI API 调用失败: ${response.statusText}`);
  }
  
  const data = await response.json();
  return data.choices[0].message.content;
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args.includes('--help')) {
    console.log(`
公众号文章改写工具

用法:
  ts-node rewrite.ts --url <文章链接> [选项]

选项:
  --url <链接>        公众号文章链接（必需）
  --mode <模式>       改写模式: light|medium|deep|style（默认: medium）
  --output <文件>     输出文件路径（默认: 改写后文章.md）
  --help             显示帮助信息

示例:
  ts-node rewrite.ts --url "https://mp.weixin.qq.com/s/xxxxx"
  ts-node rewrite.ts --url "https://mp.weixin.qq.com/s/xxxxx" --mode deep
  ts-node rewrite.ts --url "https://mp.weixin.qq.com/s/xxxxx" --output "output.md"
    `);
    process.exit(0);
  }
  
  const options: RewriteOptions = {
    url: '',
    mode: 'medium',
    output: '改写后文章.md'
  };
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--url' && args[i + 1]) {
      options.url = args[i + 1];
      i++;
    } else if (args[i] === '--mode' && args[i + 1]) {
      options.mode = args[i + 1] as any;
      i++;
    } else if (args[i] === '--output' && args[i + 1]) {
      options.output = args[i + 1];
      i++;
    }
  }
  
  if (!options.url) {
    console.error('❌ 请提供文章链接: --url <链接>');
    process.exit(1);
  }
  
  try {
    const config = loadConfig();
    
    // 1. 抓取文章
    let content = await fetchArticle(options.url, config);
    console.log(`✅ 抓取成功，文章长度: ${content.length} 字符`);
    
    // 2. 清理水印
    if (config.removeWatermarks) {
      content = removeWatermarks(content, config.watermarkKeywords);
      console.log(`✅ 水印清理完成`);
    }
    
    // 3. AI 改写
    const rewritten = await rewriteContent(content, options.mode, config);
    console.log(`✅ 改写完成`);
    
    // 4. 保存文件
    fs.writeFileSync(options.output!, rewritten, 'utf-8');
    console.log(`✅ 已保存到: ${options.output}`);
    
    console.log('\n📊 统计信息:');
    console.log(`   原文长度: ${content.length} 字符`);
    console.log(`   改写后长度: ${rewritten.length} 字符`);
    console.log(`   改写模式: ${options.mode}`);
    
  } catch (error) {
    console.error('❌ 错误:', error instanceof Error ? error.message : error);
    process.exit(1);
  }
}

main();
