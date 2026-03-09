---
name: publish-to-github
description: 创建 GitHub 仓库、将本地项目初始化并上传、补充 README/.gitignore/LICENSE、配置 remote 与首个 commit，并在发布前完成轻量项目修改。用于用户要求“上传到 GitHub”“创建仓库并推送当前项目”“先改项目再发布”“把这个目录变成 GitHub 项目”等场景。
---

# publish-to-github

使用 `gh` + `git` 完成 GitHub 发布工作流。优先少问问题；能推断就推断，但涉及公开可见性、删除或覆盖 remote、强推、重写历史等敏感操作时必须确认或采取安全默认值。

## 默认策略

- 未指定仓库名时，默认使用项目目录名。
- 未指定可见性时，默认 `private`，并在结果中说明。
- 未指定描述时，可留空或补一条简短描述。
- 未指定初始化内容时，优先保留现有项目文件；只有空目录时才自动补 `README.md`。
- 用户明确说“其他的你自己想”时，可在安全范围内补齐基础文件，如 `README.md`、`.gitignore`、`LICENSE`。

## 工作流

### Step1: 确定目标

收集或推断以下信息：
- 项目目录
- GitHub owner
- 仓库名
- 可见性（public/private）
- 是否需要先改项目
- 是否需要补 `README.md`、`.gitignore`、`LICENSE`

如果用户只说“上传这个项目”，先从当前目录名、文件结构和现有 Git 状态推断；只有关键路径不明确时再追问一次。

### Step2: 检查环境

按顺序检查：
1. `command -v gh`
2. `gh auth status`
3. `git status`
4. `git remote -v`

如果 `gh` 未安装，优先使用最短路径安装或给出明确安装命令。

如果未登录 GitHub，优先引导：
```bash
gh auth login -h github.com -p https -w
```

绝不要要求用户把 PAT/token直接发到群聊或公开聊天里。
如果用户已经在公开对话中发了 token，完成任务后提醒其立刻撤销并重新生成。

### Step3: 发布前整理项目

如果用户要求“顺手改一下项目”“帮我补齐基础信息”“优化一下再传”，先完成轻量修改：
- `README.md`
- `.gitignore`
- `LICENSE`
- `package.json`、`pyproject.toml`、`requirements.txt` 中的基础元信息
- 首页文案、项目标题、项目描述等小改动

如果修改规模明显超出“发布前整理”，先说明，再切换到更适合的编码工作流。

### Step4: 初始化或整理 Git

- 若当前目录不是 Git 仓库：`git init`
-需要时设置默认分支：`git branch -M main`
- 添加文件：`git add .`
- 若存在待提交改动，则提交：`git commit -m "chore: initial commit"`
- 若已有 remote `origin`：
 - 指向正确仓库则复用
 - 指向错误仓库时，不要静默覆盖；先确认，或使用 `git remote set-url origin ...`

### Step5: 创建或连接 GitHub 仓库

优先使用 `gh repo create`。

#### 新建远端仓库并推送当前目录
```bash
gh repo create <owner>/<repo> --private --source=. --remote=origin --push
```

####只创建远端仓库
```bash
gh repo create <owner>/<repo> --private --description "<desc>"
```

随后手动连接并推送：
```bash
git branch -M main
git remote add origin https://github.com/<owner>/<repo>.git
git add .
git commit -m "chore: initial commit"
git push -u origin main
```

如果远端仓库已存在：
- 不要重复创建
- 改为连接已有仓库并推送
- 如有必要，使用 `git remote add origin ...` 或 `git remote set-url origin ...`

### Step6: 输出结果

始终返回：
- GitHub 仓库 URL
- 仓库可见性
- 本次做了哪些修改
- 下一步建议（如补 CI、Actions、Release、Issue 模板等）

## 决策规则

- 可见性不明确：默认 `private`
- 用户明确说公开、开源：使用 `public`
- 用户只说“创建一个 test 项目”：可自动补 `README.md` 与简短描述
- 用户说“其他的你自己想”：在安全范围内自动完成常见初始化，不要过度设计
- 已有未提交改动：默认一并纳入首次提交，除非用户明确排除某些文件
-发现敏感文件（如 `.env`、私钥、凭证导出文件）：先阻止上传，补 `.gitignore`，必要时提醒用户

## 安全要求

- 不在回复中回显 token、cookie、SSH 私钥
- 不建议用户在群聊中发送 GitHub PAT
- 如果 token 已在公开环境出现，提醒立即 revoke
- 删除仓库、强推、覆盖 remote、重写历史前必须确认
- 默认避免 public 泄露和敏感文件上传

## 常用命令

### 检查登录状态
```bash
gh auth status
```

### 查看当前仓库远端
```bash
git remote -v
```

### 创建空仓库并带 README
```bash
gh repo create <owner>/<repo> --private --add-readme --description "<desc>"
```

### 从现有项目直接创建并推送
```bash
gh repo create <owner>/<repo> --private --source=. --remote=origin --push
```

###远端已存在时手动推送
```bash
git branch -M main
git remote add origin https://github.com/<owner>/<repo>.git
git push -u origin main
```

## 示例

### 示例1：创建一个新仓库
用户：
“帮我创建一个 GitHub 的 test 项目，其他的你自己想”

执行思路：
1. 检查 `gh auth status`
2. 创建 `test`
3. 默认使用 `private`（除非用户明确要求 `public`）
4. 自动补 `README.md`
5. 返回仓库 URL

### 示例2：上传当前项目
用户：
“把这个项目上传到 GitHub，仓库名叫 openclaw-helper”

执行思路：
1. 检查当前目录与 Git 状态
2. 必要时补 `.gitignore` / `README.md`
3. 执行：
 ```bash
 gh repo create <owner>/openclaw-helper --private --source=. --remote=origin --push
 ```
4. 返回仓库地址

### 示例3：先改再发
用户：
“先把 README 和 package.json 改好，再上传到 GitHub”

执行思路：
1.先完成轻量文件修改
2. 概述变更
3. 创建或连接 GitHub 仓库并推送
4. 返回变更摘要与 URL

##失败处理

- `gh auth status`失败：直接提示登录命令，不要空泛解释
- 仓库名冲突：尝试 `<repo>-app`、`<repo>-1`，或让用户确认
- push失败：检查 remote、分支名、认证方式
- 当前目录不是目标项目：先定位正确目录再操作，不要把错误目录推上去
- `origin` 已存在且指向别处：先确认，不要静默覆盖
