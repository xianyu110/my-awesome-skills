不用魔法！免费Claude平替工具OpenCode保姆级教程
 
大家总问我有没有不用魔法、还免费的Claude平替，今天就给大家挖到宝——OpenCode！不管是写代码、做内容创作还是日常问答都能用，还能调用多款大模型，新手也能快速上手。
 
一、 下载安装：三步搞定，轻松改路径
 
1. 打开OpenCode官网，点击显眼的下载按钮，获取对应系统的安装包。
2. 双击安装包启动程序，全程跟着“下一步”走，重点在选择安装路径这一步——别默认装C盘，直接选D盘，避免占用系统盘空间拖慢电脑。
3. 安装完成后软件会自动启动，不用手动找快捷方式，超省心。
 
二、 首次使用：选对模型，中文友好优先
 
1. 软件打开后直接进入首页，不用复杂设置，随便点击输入框激活功能。
2. 模型列表里推荐优先选 GLM-4.7！它是智谱的模型，对中文语境支持拉满，不管是写文案、解代码还是日常聊天，体验都很丝滑。
3. 如果你有ChatGPT或Gemini会员，也能直接调用它们的模型：点击界面上的对应登录入口，跳转账号登录后，就能用CodeX等模型写代码、做深度任务啦。
 
三、 必装神级插件：Oh My OpenCode，解锁Agent超强能力
 
这一步是关键！装完OpenCode一定要加Oh My OpenCode插件，相当于给工具开了“外挂”。
 
1. 它内置了超多分工明确的专家Agent：架构设计、文档翻译、代码库扫描、UI前端设计，你能想到的技术和创作需求几乎都覆盖。
2. 安装超简单：复制插件的安装指令，粘贴到OpenCode的对话框里执行，一键搞定。
3. 没有会员也不影响！没订阅ChatGPT/Gemini的话，所有Agent默认调用GLM-4.7模型，功能完全不打折。
 
四、 额外惊喜：Skills功能，下期深挖
 
除了基础对话和Agent，OpenCode还能调用Skills拓展功能，不管是Web Coding还是数据处理都能实现，具体玩法我下期给大家详细拆解！
 
 Oh My OpenCode 是 OpenCode 的增强插件（类似 Oh My Zsh 对于 Zsh 的增强），它为 OpenCode 添加了更多强大功能：

多 AI 模型协作：可以同时调用多个 AI 模型协同工作
智能体系统（Agents）：内置多个专业智能体（如 frontend-ui-ux-engineer、oracle 等）
提示词优化：自动优化你给 AI 的指令
后台任务管理：可以并行执行多个任务
简单理解：安装 Oh My OpenCode 后，OpenCode 就从一个 AI 助手变成了一个完整的 AI 开发团队。
 
为什么推荐 GLM-4.7？
✅ 完全免费：不需要 API Key 或付费订阅
✅ 中文能力强：智谱出品，专门针对中文优化
✅ 国内访问友好：无需科学上网，网络稳定
✅ Agent 场景优化：知道什么时候该读文件、运行测试、自愈能力最好
 
 安装oh-my-opencode也特别简单，跟前面的
opencode-antigravity-auth流程一样。
在OpenCode中，新起一个对话。
然后直接把这个Prompt发过去：
Install and configure by following the
instructions here
https://raw.githubusercontent.com/code-
yeongyu/oh-my-
opencode/refs/heads/master/README.md

Oh-My-Opencode内部已经内置了一套 Agent 结构。

主控 Agent 负责整体规划，不同子 Agent 分工明确，有的管架构，有的管前端体验，有的专门用来翻文档、扫代码库。这种拆分在处理复杂任务时非常有价值。

更重要的一点是，它和 Claude Code 高度兼容。

Command、Agent、Skill、MCP、Hook 这些机制都可以直接用，这也是 Skill 能顺畅运行的前提。