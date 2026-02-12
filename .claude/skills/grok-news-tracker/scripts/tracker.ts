#!/usr/bin/env bun

import { parseArgs } from 'util';
import { writeFile, mkdir } from 'fs/promises';
import { join, dirname } from 'path';
import { createGrokClient } from './grok-client.js';
import { ReportFormatter } from './formatter.js';
import type { DailyReport, NewsCategory, TrackerOptions } from './types.js';

const DEFAULT_SOURCES = ['tech', 'ai', 'startup'];
const OUTPUT_DIR = process.env.OUTPUT_DIR || 'reports';

const SOURCE_NAMES: Record<string, string> = {
  tech: '科技资讯',
  ai: 'AI/机器学习',
  startup: '创业/商业',
  finance: '金融/投资',
  dev: '开发者资讯',
  design: '设计/创意',
  product: '产品/运营',
};

async function track(options: TrackerOptions): Promise<void> {
  const sources = options.sources || DEFAULT_SOURCES;
  const format = options.format || 'markdown';
  const output = options.output || join(OUTPUT_DIR, `${new Date().toISOString().split('T')[0]}.${format === 'html' ? 'html' : format === 'json' ? 'json' : 'md'}`);

  console.log('🔍 开始追踪热点资讯...');
  console.log(`📊 信息源：${sources.map(s => SOURCE_NAMES[s] || s).join('、')}`);

  try {
    const client = createGrokClient();
    const content = await client.analyzeNews(sources);

    // 解析 Grok 返回的内容为结构化数据
    const report: DailyReport = {
      date: new Date().toISOString().split('T')[0],
      categories: parseGrokResponse(content, sources),
    };

    // 格式化输出
    const formatter = new ReportFormatter();
    const formattedContent = formatter.format(report, format);

    // 确保输出目录存在
    await mkdir(dirname(output), { recursive: true });

    // 写入文件
    await writeFile(output, formattedContent, 'utf-8');

    console.log('✅ 报告生成完成！');
    console.log(`📄 输出文件：${output}`);
    console.log(`📝 格式：${format}`);

    // 如果是 markdown，显示预览
    if (format === 'markdown') {
      console.log('\n--- 报告预览 ---\n');
      console.log(formattedContent.split('\n').slice(0, 20).join('\n'));
      console.log('\n...\n');
    }
  } catch (error) {
    console.error('❌ 追踪失败：', error);
    process.exit(1);
  }
}

function parseGrokResponse(content: string, sources: string[]): NewsCategory[] {
  const categories: NewsCategory[] = [];
  
  // 简单的解析逻辑，将 Grok 的响应转换为结构化数据
  const lines = content.split('\n');
  let currentCategory: NewsCategory | null = null;
  let currentTopic: any = null;

  for (const line of lines) {
    // 检测分类标题（## 🔥 [领域名称]）
    if (line.match(/^##\s+🔥\s+(.+)/)) {
      if (currentCategory && currentTopic) {
        currentCategory.topics.push(currentTopic);
      }
      if (currentCategory) {
        categories.push(currentCategory);
      }
      
      const categoryName = line.replace(/^##\s+🔥\s+/, '').trim();
      currentCategory = {
        name: categoryName,
        topics: [],
      };
      currentTopic = null;
    }
    // 检测话题标题（### [话题标题]）
    else if (line.match(/^###\s+(.+)/) && currentCategory) {
      if (currentTopic) {
        currentCategory.topics.push(currentTopic);
      }
      
      const title = line.replace(/^###\s+/, '').trim();
      currentTopic = {
        title,
        summary: '',
        source: '',
        importance: 5,
        timestamp: new Date().toISOString(),
        category: currentCategory.name,
      };
    }
    // 解析元数据
    else if (currentTopic) {
      if (line.includes('**摘要**：')) {
        currentTopic.summary = line.split('**摘要**：')[1]?.trim() || '';
      } else if (line.includes('**重要性**：')) {
        const match = line.match(/(\d+)/);
        if (match) {
          currentTopic.importance = parseInt(match[1], 10);
        }
      } else if (line.includes('**来源**：')) {
        currentTopic.source = line.split('**来源**：')[1]?.trim() || '';
      }
    }
  }

  // 添加最后一个话题和分类
  if (currentCategory && currentTopic) {
    currentCategory.topics.push(currentTopic);
  }
  if (currentCategory) {
    categories.push(currentCategory);
  }

  return categories;
}

async function report(options: TrackerOptions): Promise<void> {
  console.log('📊 生成汇总报告...');
  console.log(`📅 时间范围：最近 ${options.days || 7} 天`);
  
  // TODO: 实现历史报告汇总功能
  console.log('⚠️  历史报告汇总功能开发中...');
}

async function schedule(cron: string): Promise<void> {
  console.log('⏰ 设置定时任务...');
  console.log(`📅 Cron 表达式：${cron}`);
  
  console.log('\n建议使用系统 cron 或 Kiro Hooks 实现定时任务：');
  console.log('\n1. 使用系统 cron：');
  console.log(`   ${cron} cd $(pwd) && npx -y bun ${__filename} track\n`);
  console.log('2. 使用 Kiro Hooks：');
  console.log('   在 Kiro 中创建 userTriggered hook，手动触发追踪\n');
}

async function main() {
  const { values, positionals } = parseArgs({
    args: process.argv.slice(2),
    options: {
      sources: { type: 'string', short: 's' },
      output: { type: 'string', short: 'o' },
      format: { type: 'string', short: 'f' },
      days: { type: 'string', short: 'd' },
      cron: { type: 'string', short: 'c' },
      help: { type: 'boolean', short: 'h' },
    },
    allowPositionals: true,
  });

  if (values.help) {
    console.log(`
Grok News Tracker - 自动追踪热点资讯

用法：
  tracker.ts <command> [options]

命令：
  track              追踪热点资讯
  report             生成汇总报告
  schedule           设置定时任务

选项：
  -s, --sources      信息源（逗号分隔）
  -o, --output       输出文件路径
  -f, --format       输出格式（markdown/json/html）
  -d, --days         报告天数
  -c, --cron         Cron 表达式
  -h, --help         显示帮助

示例：
  tracker.ts track
  tracker.ts track --sources tech,ai --output report.md
  tracker.ts report --days 7 --format html
  tracker.ts schedule --cron "0 8 * * *"

环境变量：
  GROK_API_KEY       Grok API 密钥（必需）
  GROK_BASE_URL      API 基础地址
  GROK_MODEL         使用的模型
  OUTPUT_DIR         报告输出目录
`);
    return;
  }

  const command = positionals[0] || 'track';
  const options: TrackerOptions = {
    sources: values.sources?.split(','),
    output: values.output,
    format: (values.format as any) || 'markdown',
    days: values.days ? parseInt(values.days, 10) : 7,
  };

  switch (command) {
    case 'track':
      await track(options);
      break;
    case 'report':
      await report(options);
      break;
    case 'schedule':
      await schedule(values.cron || '0 8 * * *');
      break;
    default:
      console.error(`❌ 未知命令：${command}`);
      console.log('使用 --help 查看帮助');
      process.exit(1);
  }
}

main().catch(console.error);
