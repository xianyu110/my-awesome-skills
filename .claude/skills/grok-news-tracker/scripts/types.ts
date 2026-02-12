export interface GrokConfig {
  apiKey: string;
  baseUrl: string;
  model: string;
}

export interface NewsSource {
  id: string;
  name: string;
  category: string;
}

export interface NewsTopic {
  title: string;
  summary: string;
  source: string;
  url?: string;
  importance: number;
  timestamp: string;
  category: string;
}

export interface NewsCategory {
  name: string;
  topics: NewsTopic[];
}

export interface DailyReport {
  date: string;
  categories: NewsCategory[];
  summary?: string;
}

export interface TrackerOptions {
  sources?: string[];
  output?: string;
  format?: 'markdown' | 'json' | 'html';
  days?: number;
}

export interface GrokResponse {
  id: string;
  object: string;
  created: number;
  model: string;
  choices: Array<{
    index: number;
    message: {
      role: string;
      content: string;
    };
    finish_reason: string;
  }>;
  usage: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}
