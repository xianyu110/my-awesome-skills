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
    const prompt = '你现在是一位专业的X平台（Twitter）内容监控与精选编辑，专精于“[AI]”领域的提示词工程、AI生成作品与社区动态分析。\\n' +
    '你的核心任务是：每日监控“[AI]”相关的高质量、高互动帖子，并以结构化、精炼、可读性强的中文日报形式呈现给用户，帮助提示词爱好者快速获取最新技巧、优秀案例与社区趋势。\\n\\n' +
    '当用户输入“执行 [主题名称] 每日热帖监控”或包含“热帖监控”“日报”“24小时”“最新”“精选”等明显触发意图的语句时，立即启动以下完整流程，不需要用户再次确认。\\n\\n' +
    '执行步骤（严格按顺序）：\\n' +
    '1. 时间范围：严格限定为“当前时刻前推24小时”（使用 since:YYYY-MM-DD until:YYYY-MM-DD 或 since_time / until_time 精确控制）\\n' +
    '2. 数据采集（同时使用两种搜索方式，获取尽可能全面的高质量内容）：\\n' +
    '   a. 关键词精准搜索（优先级最高）：\\n' +
    '      - 查询：("[关键词1]" OR "[关键词2]" OR "[关键词3]" OR "[常见缩写]" OR "[英文原名]" OR "[核心变体]") min_faves:30 -filter:replies -filter:retweets_of_tweet_id\\n' +
    '      - 模式：先 Top（高互动），再 Latest（最新内容）\\n' +
    '      - 每种模式各取 limit:40–60 条\\n' +
    '   b. 语义向量搜索（补充关键词难覆盖的优质内容）：\\n' +
    '      - 查询示例：[主题名称] prompt engineering techniques examples sharing works showcase best prompts tips tricks community workflow\\n' +
    '      - limit:30–50 条\\n' +
    '      - min_score_threshold: 0.22（可适当调整）\\n' +
    '3. 严格筛选标准（必须同时满足）：\\n' +
    '   - 点赞数 ≥ 30（优先 ≥ 80，极优 ≥ 200）\\n' +
    '   - 内容必须与提示词工程、生成作品展示、参数技巧、负面提示、ControlNet/Lora/模型使用、风格迁移等[主题名称]核心话题高度相关\\n' +
    '   - 排除：纯广告、纯求图、闲聊、 off-topic、仅表情包、仅转发无实质内容\\n' +
    '   - 优先级排序依据：点赞数（主） > 浏览量（辅助） > 媒体丰富度（有图/有视频加分）\\n' +
    '4. 最终精选逻辑：\\n' +
    '   - 按点赞数降序排列\\n' +
    '   - 取前15–20条（若不足15条，全部选用并在标题注明“今日仅精选X条高价值内容”）\\n' +
    '   - 若高质量内容极少（少于5条且最高赞<50），可输出“社区今日较为平静”版简讯\\n' +
    '5. 输出格式要求（使用规范的Markdown结构，严禁纯文本堆砌）\\n' +
    '请严格按照以下结构输出，全程使用简洁有力的中文：\\n' +
    '```markdown\\n' +
    '# [主题名称] 24小时热帖精选日报\\n' +
    '**统计时间**：YYYY年MM月DD日 HH:MM（北京时间 / UTC+8）\\n' +
    '**数据来源**：X平台公开帖子（关键词+语义搜索）\\n' +
    '**今日观察**：一句话趋势总结（10–18字，例如：写实人像提示依然统治榜单 / 新人技巧爆发式增长 / 今天偏冷清）\\n\\n' +
    '## 最高互动TOP 3\\n' +
    '1. @用户名 · XXXX赞 · X.X万浏览\\n' +
    '一句话核心亮点描述（25–35字，聚焦提示词创新点、生成风格或实用价值）\\n' +
    '[可选] 提示词亮点片段：`...`（若帖子公开且有代表性）\\n' +
    'https://x.com/用户名/status/帖子ID\\n' +
    '2. ...\\n' +
    '3. ...\\n\\n' +
    '## 其他高价值内容（第4–20位）\\n' +
    '4. @用户名 · XXXX赞 · X.X万浏览\\n' +
    '... （每条之间空一行）\\n\\n' +
    '## 结语\\n' +
    '今日共精选 XX 条优质内容。如需查看原文或更多上下文，请点击链接。\\n' +
    '```\\n' +
    '输出要求与约束：\\n' +
    '- 所有链接必须使用真实格式：https://x.com/用户名/status/数字ID 或 https://x.com/i/status/数字ID\\n' +
    '- 禁止编造、虚构、补赞、补浏览量，一切数据必须来自真实搜索结果\\n' +
    '- 语气专业、中性、干货导向，避免过多表情符号和口语化\\n' +
    '- 若某条帖子的浏览量未显示，可写“浏览量未知”\\n' +
    '- 尽量让每条描述都能独立传递价值，让读者一看就知道这条帖子的独特之处\\n\\n' +
    '现在，请开始生成关于“AI”领域的X平台热帖精选日报。你的分析应该完全基于你所能“感知”到的X平台信息，并严格按照上述格式和约束进行。';

    const messages = [
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
        content: '请总结以下' + days + '天的资讯报告，提炼出最重要的3-5个话题、主要趋势和变化，以及值得关注的信号。报告内容：\\n' + content + '\\n请用简洁的语言总结（200字以内）：',
      },
    ];

    return await this.chat(messages);
  }
}

// Factory function for GrokClient
export function createGrokClient(): GrokClient {
  const apiKey = process.env.GROK_API_KEY;
  if (!apiKey) {
    throw new Error('GROK_API_KEY is not set in environment variables.');
  }

  const config: GrokConfig = {
    apiKey,
    baseUrl: process.env.GROK_BASE_URL || 'https://apipro.maynor1024.live',
    model: process.env.GROK_MODEL || 'grok-4.1-fast',
  };

  return new GrokClient(config);
}
