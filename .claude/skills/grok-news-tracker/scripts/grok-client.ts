import type { GrokConfig, GrokResponse } from './types.js';

export class GrokClient {
  private config: GrokConfig;

  constructor(config: GrokConfig) {
    this.config = config;
  }

  async chat(messages: Array<{ role: string; content: string }>): Promise<string> {
    const response = await fetch(`${this.config.baseUrl}/v1/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.config.apiKey}`,
      },
      body: JSON.stringify({
        model: this.config.model,
        messages,
        temperature: 0.7,
        max_tokens: 4000,
      }),
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Grok API error: ${response.status} ${error}`);
    }

    const data = await response.json() as GrokResponse;
    return data.choices[0]?.message?.content || '';
  }

  async analyzeNews(sources: string[]): Promise<string> {
    const prompt = `你是一个专业的资讯分析师。请分析以下领域的最新热点资讯：${sources.join('、')}

请按以下格式输出：

## 🔥 [领域名称]

### [话题标题]
- **摘要**：简要描述（50字以内）
- **重要性**：1-10分
- **影响**：对行业/用户的影响
- **来源**：信息来源

要求：
1. 每个领域至少3个热点话题
2. 按重要性排序
3. 关注最新（24小时内）的资讯
4. 提供客观、准确的分析
5. 使用中文输出

请开始分析：`;

    const messages = [
      {
        role: 'system',
        content: '你是一个专业的资讯分析师，擅长追踪和分析各领域的热点话题。你的分析客观、准确、有洞察力。',
      },
      {
        role: 'user',
        content: prompt,
      },
    ];

    return await this.chat(messages);
  }

  async summarizeReport(content: string, days: number): Promise<string> {
    const messages = [
      {
        role: 'system',
        content: '你是一个专业的内容总结专家，擅长提炼关键信息和趋势。',
      },
      {
        role: 'user',
        content: `请总结以下${days}天的资讯报告，提炼出：
1. 最重要的3-5个话题
2. 主要趋势和变化
3. 值得关注的信号

报告内容：
${content}

请用简洁的语言总结（200字以内）：`,
      },
    ];

    return await this.chat(messages);
  }
}

export function createGrokClient(config?: Partial<GrokConfig>): GrokClient {
  const defaultConfig: GrokConfig = {
    apiKey: process.env.GROK_API_KEY || '',
    baseUrl: process.env.GROK_BASE_URL || 'https://apipro.maynor1024.live',
    model: process.env.GROK_MODEL || 'grok-4.1-fast',
  };

  if (!defaultConfig.apiKey) {
    throw new Error('GROK_API_KEY environment variable is required');
  }

  return new GrokClient({ ...defaultConfig, ...config });
}
