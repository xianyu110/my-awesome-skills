# example-output

## 成功输出示例

```markdown
已开始执行公众号草稿发布：
- 模式：article
- Markdown：/Users/chinamanor/articles/2026-03-08/openclaw-wechat/article.md
- 图片目录：/Users/chinamanor/articles/2026-03-08/openclaw-wechat/images
- 动作：保存为草稿

说明：
- 当前版本走浏览器自动化发布链路
- 首次运行如未登录公众号后台，需要先扫码登录
- 发布完成后建议去后台复查封面、摘要和图片位置
```

## 失败输出示例

```markdown
发布未执行：
- 原因：image-text 模式下没有找到 images/、assets/ 或 img/ 目录
- 建议：把图片放到文章目录下的 images/ 目录后重试
```

## V2 目标输出示例

```markdown
已完成公众号草稿更新：
- 模式：article
- 草稿 media_id：xxxxxxxx
- 新上传图片：2 张
- 复用缓存图片：5 张
- 动作：已更新已有草稿，未创建重复草稿
```
