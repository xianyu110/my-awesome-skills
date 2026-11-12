---
name: Codex 与 Claude Desktop 中转配置
description: >-
  用于在用户电脑上安装或重新配置 Codex Desktop、Claude Desktop，并通过 CC Switch 接到第三方中转（如
  momoai.asia）；也用于排查401、分组不支持模型、协议未注册或切换后仍走官方接口。不用于官方订阅、购买密钥或账号合租。
---
# Codex 与 Claude Desktop 中转配置

帮用户在自己的电脑上装官方客户端，并用 CC Switch 把请求指向他已有的第三方中转。这不是 OpenAI 或 Anthropic 的官方订阅；对话内容会经过中转站。开始前用一句话说清这一点，再继续。

本技能只覆盖：客户端与 CC Switch 的安装、本机配置、重启验证和常见报错。不要代用户购买套餐，不要写代充、合租或号池步骤，不要把密钥写进聊天、技能或截图。

## 边界

- 只在用户的电脑上操作，且先取得改动本机的授权。不要装到助手自己的电脑上。
- 用户必须已经自己拥有中转站的 API Key。没有 Key 就停在配置之前，请他到自己的中转控制台新建，再用保险库或助手的密钥表单提交，不要让他把 Key 贴到聊天里。
- 客户端优先走官方源。不要把网盘安装包当成首选；若官方地址打不开，改走官方 GitHub Releases 或微软商店，并告诉用户网盘包风险更高。
- 模型名、分组名和接口地址以当天控制台为准。下文的示例值只用于 momoai.asia 一类常见填法，发现不一致时以控制台为准。

## 1. 先确认目标

问清要配哪个客户端（可以两个都装，CC Switch 里各建一张卡片，互不影响），以及系统是 macOS 还是 Windows。

默认中转根地址用 `https://momoai.asia`。用户若指定了其他域名，用他给的地址，不要改回官方 `https://api.openai.com` 或 Anthropic 官方地址。

在控制台确认：

- 用 Codex 时，Key 所属分组要支持 Codex（常见是专用 Codex 分组，不要误用按量付费分组的 Key）。
- 用 Claude Desktop 时，Key 所属分组要支持 Claude（常见分组名是 `ClaudeMax`）。
- 记下该分组实际支持的模型 ID，配置时只填这些 ID。

## 2. 安装官方客户端

### Codex Desktop

- macOS：从 [Codex 官方安装包](https://persistent.oaistatic.com/codex-app-prod/Codex.dmg) 下载，或看 [openai/codex 的 Releases](https://github.com/openai/codex/releases)。
- Windows：优先用微软商店搜索 `Codex` 安装；也可从 [GitHub Releases](https://github.com/openai/codex/releases) 取安装包。

若之前登录过官方账号，先在客户端退出登录，再改为通过 CC Switch 使用 API Key。

### Claude Desktop

从 [Claude 官方下载页](https://claude.com/download) 取 macOS 或 Windows 安装包。macOS 把 `Claude.app` 拖进应用程序文件夹；Windows 跑安装向导。装好后先不要登录官方账号，先做下一步中转配置。

## 3. 安装并启动 CC Switch

CC Switch 是本机上用来切换中转地址和 Key 的工具，两个客户端都要靠它。

1. 从 [CC Switch Releases](https://github.com/farion1231/cc-switch/releases) 下载最新正式安装包：macOS 用 `.dmg`，也可 `brew install --cask cc-switch`；Windows 用 `.msi`。不要用 Portable zip，否则 `ccswitch://` 协议可能注册不上。
2. 安装后至少完整启动一次，让系统注册协议。
3. 需要从网页导入配置时，在浏览器弹窗里允许打开本地应用。失败就改为在 CC Switch 里手动添加供应商。

## 4. 填写并启动路由

从保险库或密钥表单取 Key，不要在聊天里展示它。两个客户端各建一张卡片。

### Codex 卡片

- 应用类型选 Codex（以 CC Switch 里实际可选项为准）。
- 中转地址（Base URL）：`https://momoai.asia`（或用户指定的域名），不要填 `https://api.openai.com`。
- API Key：该 Codex 分组下的 Key。
- 模型：常见填 `gpt-6-astra`。若控制台列的是其他 ID，按控制台填；同一家族可能还有 `gpt-6-sol`、`gpt-6-luna`，用相同任务对比即可，不要把变体名写成测评结论。

### Claude Desktop 卡片

- 应用类型必须选 `Claude Desktop`，不要选成 Codex 或其他应用。
- 中转地址：`https://momoai.asia`（或用户指定的域名）。
- API Key：该 Claude 分组下的 Key（常见分组名 `ClaudeMax`）。
- 模型：只填该分组实际支持的模型 ID。界面显示名可能只是别名，能不能调通看完整 ID。

配好后：勾选并启用对应卡片，点击启动路由。「切换成功」只表示路由就绪，已经打开的客户端不会自动换新。

## 5. 彻底重启再测试

1. 完全退出 Codex 或 Claude Desktop。Windows 检查托盘，macOS 检查菜单栏，确认没有残留进程。若终端里的 CLI 也已打开，一并重启终端。
2. 重新打开客户端，新建一个空白对话，不要在旧报错对话里重试。
3. 核对当前选中的模型 ID，发一条短消息，例如：「请只回复：连接测试成功。」
4. 短消息通了之后，再试长文档、传文件或改代码。

## 6. 报错排查

先对照完整错误信息，不要猜。每改一项配置，都要重新启动路由，再彻底重启客户端。

- **401 / 走了 `api.openai.com`：** Base URL 仍是官方地址。改成中转根地址，确认启用的是对应卡片，再重启。
- **`requested model is not supported by this group`：** 模型 ID 与 Key 所属分组不符。到控制台查该分组真实支持的 ID，改 CC Switch 里的模型后重启。
- **`no quota` / 没余额：** 先核对 Key 是否属于正确分组、额度是否真的用完。不要指导换号或合租。
- **「未安装或协议处理程序未注册」：** 没装正式版或还没启动过 CC Switch。改装 `.dmg` / `.msi`，启动一次后再导入；仍失败则手动填写供应商。
- **一直转圈或发送失败：** 先发短消息；检查网络、路由是否在跑、启用的是否为当前客户端的那张卡片；然后同时重启 CC Switch 和客户端。
- **Codex 仍走官方账号：** 先退出官方登录，再用中转 Key。
- **生图失败：** 先确认启用的是 Codex 卡片，且模型 ID 在中转支持列表里。不要一上来跑来路不明的「一键修复」脚本；若用户坚持用第三方修复脚本，先说清它会改本机鉴权配置，再按他的选择执行，执行后仍须彻底重启 Codex 并新建对话。

## 7. 完成前自查

- [ ] 客户端来自官方源
- [ ] CC Switch 为正式安装并已启动过
- [ ] Key 分组与客户端匹配，模型 ID 在该分组支持列表中
- [ ] Base URL 是中转地址，不是官方 API
- [ ] 对应卡片已启用，路由已启动
- [ ] 客户端已彻底退出并重新打开
- [ ] 新对话短消息测试成功
- [ ] 全程没有把 Key 写进聊天
