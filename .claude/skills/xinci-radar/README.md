# 出海新词雷达（Xinci Radar）

按「新词日更」方法，在本地跑三路采集、交叉验证、5 年核验和五重去重，生成中文日报。方法技能见同目录 [SKILL.md](SKILL.md)。

不要编造搜索量、难度或首页盘面。运行产生的数据库、cache 和密钥不要提交进仓库。

## 怎么跑

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python run_daily.py
# 只基于已采集数据重跑交叉验证 / 5 年核验 / 报告：
.venv/bin/python run_daily.py --reuse --run-date YYYY-MM-DD
```

时区默认 `Asia/Shanghai`，可用环境变量 `RADAR_TZ` 覆盖。报告写到 `reports/YYYY-MM-DD.md` 和 `reports/YYYY-MM-DD.html`。SQLite 在 `data/radar.db`，发布去重状态在 `data/published_state.json`。

可选：另开一个进程监听证书透明日志（已买域名但 WhoisDS 日包还没收进去、已经申请了 HTTPS 证书的那批）：

```bash
.venv/bin/python certstream_listener.py
```

需要能连上 `wss://certstream.calidog.io`。连不上就关掉，日更脚本仍然只用 WhoisDS 免费日包。

## 三路信源

1. **域名**：WhoisDS 免费新注册域名日包 → 滤垃圾 → wordninja 切词根 → DNS + HTTP 探针。未解析域名会保留（早鸟信号）。已上线的抓 title / description，并探测定价页。核心词只取自域名词根，不用网页 title 里的堆砌词。
2. **同行 sitemap**：配置里的工具站（默认 8 个 AI 图片/视频/音频站）。按 lastmod 倒序收录，剥 `/es/` `/fr/` `/de/` 等语言重复路径。**lastmod 绝不当成关键词起量日。**
3. **Google Trends**：`config/roots.json` 里 73 个词根，5 个一批，`today 1-m` 和 `now 7-d`，全球，收 Rising / Breakout；Breakout 再做一层二级下钻。响应要先切掉 XSSI 前缀再解析 JSON。间隔 2–3 秒，429 退避。

## 核验与去重

- 两路及以上命中进重点池，单路进观察池；停放页和品牌杂音丢弃。
- 候选词必须单独拉 `today 5-y`（约 262 周），不得和大词打包。没有 5 年数据的词不进关键词板块。`has_data=false` 的周按 0 计入均值。
- 分类：纯血从零突发（均值 ≤ 2 且近期拉升）、年度周期回潮（≥ 3 个年度峰）、长青老词翻红（均值 20–70，只标注，不当首次爆发）。
- 模型版本号正则过滤。
- 五重去重：字符归一化、实义词 Jaccard、垂直同义词、域名词根双向子串、写稿后回填 JSON。
- 不够 20 条不会硬凑，报告如实写过了几条。

## 布局

```
run_daily.py
certstream_listener.py
config/roots.json sites.yaml synonyms.json
radar/          # 采集、交叉验证、5 年、去重、报告
SKILL.md
data/           # 本地运行生成，不入库
reports/        # 本地运行生成，不入库
```
