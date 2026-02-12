# Python 爬虫集成指南

使用 [Access_wechat_article](https://github.com/yeximm/Access_wechat_article) 项目实现强大的微信文章抓取功能。

## 为什么使用 Python 爬虫？

相比 Jina Reader API，Python 爬虫方案可以：

- ✅ 获取文章完整内容（包括格式、图片）
- ✅ 获取文章元数据（阅读量、点赞数、评论等）
- ✅ 批量处理多篇文章
- ✅ 不受 API 调用次数限制
- ✅ 更稳定可靠

## 安装步骤

### 1. 克隆爬虫项目

```bash
cd .claude/skills/wechat-article-rewriter
git clone https://github.com/yeximm/Access_wechat_article.git python-crawler
```

### 2. 安装 Python 依赖

```bash
cd python-crawler

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置微信 PC 版 + Fiddler

这是 Python 爬虫的核心配置，用于抓取微信文章。

#### 3.1 安装微信 PC 版

- 下载并安装微信 PC 版（推荐版本：4.1.5.16）
- 登录你的微信账号

#### 3.2 安装 Fiddler Classic

- 下载地址: https://www.telerik.com/fiddler/fiddler-classic
- 推荐版本: v5.0.20253.3311
- 安装并启动 Fiddler

#### 3.3 配置 Fiddler

1. 打开 Fiddler，点击 `Tools` -> `Options`
2. 切换到 `HTTPS` 标签：
   - 勾选 `Capture HTTPS CONNECTs`
   - 勾选 `Decrypt HTTPS traffic`
   - 点击 `Actions` -> `Trust Root Certificate`（信任证书）
3. 切换到 `Connections` 标签：
   - 设置端口为 `8888`（默认）
   - 勾选 `Allow remote computers to connect`

#### 3.4 配置微信代理

1. 打开微信 PC 版
2. 点击左下角 `设置` -> `通用设置`
3. 找到 `网络设置` -> `代理设置`
4. 选择 `手动设置代理`：
   - 服务器: `127.0.0.1`
   - 端口: `8888`

### 4. 测试抓取

```bash
# 在 python-crawler 目录下
python main.py

# 根据提示选择功能 3（获取文章内容）
# 输入公众号文章链接测试
```

## 使用方法

### 方式一：通过本工具调用（推荐）

配置 `config.json`：

```json
{
  "fetchMethod": "python",
  "pythonCrawlerPath": "./python-crawler",
  ...
}
```

然后正常使用：

```bash
ts-node scripts/rewrite.ts --url "https://mp.weixin.qq.com/s/xxxxx"
```

### 方式二：直接使用 Python 爬虫

```bash
cd python-crawler
source venv/bin/activate  # 激活虚拟环境
python main.py
```

按照提示选择功能：
- 功能 1: 获取公众号主页链接
- 功能 2: 获取公众号文章列表
- 功能 3: 批量下载文章内容
- 功能 4: 获取文章详细信息（阅读量、点赞等）

## 常见问题

### Q: 为什么需要 Fiddler？

A: Fiddler 作为代理服务器，可以拦截微信的网络请求，从而获取文章内容。这是绕过微信反爬虫机制的关键。

### Q: 抓取失败怎么办？

A: 检查以下几点：
1. 微信 PC 版是否正常运行
2. Fiddler 是否正常启动
3. 微信代理设置是否正确
4. 证书是否已信任

### Q: 可以不用 Python 爬虫吗？

A: 可以，配置 `fetchMethod: "jina"` 使用 Jina Reader API，但功能会受限。

### Q: 批量处理多篇文章？

A: 使用 Python 爬虫的功能 2 和 3，可以批量获取公众号的所有文章。

## 工作流程

```
微信 PC 版
    ↓
Fiddler 代理拦截
    ↓
Python 爬虫解析
    ↓
获取文章完整数据
    ↓
本工具进行改写
    ↓
输出 Markdown
```

## 技术原理

1. **代理拦截**: Fiddler 拦截微信的 HTTPS 请求
2. **数据解析**: Python 爬虫解析微信 API 返回的数据
3. **内容提取**: 提取文章标题、正文、图片、元数据等
4. **格式转换**: 转换为 Markdown 格式

## 参考资料

- [Access_wechat_article GitHub](https://github.com/yeximm/Access_wechat_article)
- [Fiddler Classic 官网](https://www.telerik.com/fiddler/fiddler-classic)
- [微信 PC 版下载](https://pc.weixin.qq.com/)

## 注意事项

⚠️ **重要提醒**

1. 仅供学习研究使用
2. 请遵守微信公众平台的使用规范
3. 不要频繁抓取，避免被限制
4. 尊重原创作者的版权
5. 不要用于商业用途

## License

本工具遵循 MIT License，但请注意：
- Access_wechat_article 项目遵循 CC BY-NC-SA 4.0 协议
- 仅供学习研究，禁止商业使用
