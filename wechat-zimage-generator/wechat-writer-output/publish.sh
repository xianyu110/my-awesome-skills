#!/bin/bash
bun .claude/skills/baoyu-post-to-wechat/scripts/wechat-article.ts \
  --markdown wechat-writer-output/article-with-images.md \
  --theme grace \
  --author "内容创作助手" \
  --submit