import type { DailyReport } from './types.js';

export class ReportFormatter {
  formatMarkdown(report: DailyReport): string {
    let md = `# 热点资讯日报 - ${report.date}\n\n`;

    if (report.summary) {
      md += `## 📋 今日概览\n\n${report.summary}\n\n`;
    }

    md += `## 🔥 详细资讯\n\n`;

    for (const category of report.categories) {
      md += `### ${category.name}\n\n`;

      for (const topic of category.topics) {
        md += `#### ${topic.title}\n\n`;
        md += `- **摘要**：${topic.summary}\n`;
        md += `- **重要性**：${'⭐'.repeat(Math.min(topic.importance, 10))}\n`;
        if (topic.source) {
          md += `- **来源**：${topic.source}\n`;
        }
        if (topic.url) {
          md += `- **链接**：${topic.url}\n`;
        }
        md += `- **时间**：${topic.timestamp}\n\n`;
      }
    }

    md += `---\n\n`;
    md += `*报告生成时间：${new Date().toLocaleString('zh-CN')}*\n`;
    md += `*由 Grok News Tracker 自动生成*\n`;

    return md;
  }

  formatJSON(report: DailyReport): string {
    return JSON.stringify(report, null, 2);
  }

  formatHTML(report: DailyReport): string {
    let html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>热点资讯日报 - ${report.date}</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      max-width: 900px;
      margin: 0 auto;
      padding: 20px;
      line-height: 1.6;
      color: #333;
    }
    h1 {
      color: #2c3e50;
      border-bottom: 3px solid #3498db;
      padding-bottom: 10px;
    }
    h2 {
      color: #34495e;
      margin-top: 30px;
    }
    h3 {
      color: #7f8c8d;
      margin-top: 20px;
    }
    .topic {
      background: #f8f9fa;
      border-left: 4px solid #3498db;
      padding: 15px;
      margin: 15px 0;
      border-radius: 4px;
    }
    .topic h4 {
      margin-top: 0;
      color: #2c3e50;
    }
    .meta {
      color: #7f8c8d;
      font-size: 0.9em;
    }
    .importance {
      color: #f39c12;
    }
    .footer {
      margin-top: 40px;
      padding-top: 20px;
      border-top: 1px solid #ecf0f1;
      color: #95a5a6;
      font-size: 0.9em;
      text-align: center;
    }
  </style>
</head>
<body>
  <h1>🔥 热点资讯日报 - ${report.date}</h1>
`;

    if (report.summary) {
      html += `  <div class="summary">
    <h2>📋 今日概览</h2>
    <p>${report.summary}</p>
  </div>
`;
    }

    html += `  <h2>📰 详细资讯</h2>\n`;

    for (const category of report.categories) {
      html += `  <h3>${category.name}</h3>\n`;

      for (const topic of category.topics) {
        html += `  <div class="topic">
    <h4>${topic.title}</h4>
    <p>${topic.summary}</p>
    <div class="meta">
      <span class="importance">重要性：${'⭐'.repeat(Math.min(topic.importance, 10))}</span><br>
`;
        if (topic.source) {
          html += `      来源：${topic.source}<br>\n`;
        }
        if (topic.url) {
          html += `      链接：<a href="${topic.url}" target="_blank">${topic.url}</a><br>\n`;
        }
        html += `      时间：${topic.timestamp}
    </div>
  </div>
`;
      }
    }

    html += `  <div class="footer">
    <p>报告生成时间：${new Date().toLocaleString('zh-CN')}</p>
    <p>由 Grok News Tracker 自动生成</p>
  </div>
</body>
</html>`;

    return html;
  }

  format(report: DailyReport, format: 'markdown' | 'json' | 'html'): string {
    switch (format) {
      case 'json':
        return this.formatJSON(report);
      case 'html':
        return this.formatHTML(report);
      case 'markdown':
      default:
        return this.formatMarkdown(report);
    }
  }
}
