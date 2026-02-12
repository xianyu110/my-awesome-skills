## 微信公众号/文章 获取（Access_wechat_article）

更新时间：2025-12-03

本项目是基于Python语言的爬虫程序，支持对微信公众号文章内容获取

目前支持 Windows / Linux 开箱即用，**建议使用虚拟环境运行项目**

如果感兴趣，请 **Fork** 项目后自行研究使用

使用过程中如遇到错误，欢迎提交 [issues](https://github.com/yeximm/Access_wechat_article/issues) 来讨论

**注**：请在 [GitHub](https://github.com/) 平台提交 [issues](https://github.com/yeximm/Access_wechat_article/issues)

## 一、主要功能

1. 获取**公众号主页链接**，通过微信内置浏览器可直接打开
2. 获取公众号**已发布**的文章列表（**微信公众号**下的历史文章）
3. 批量下载公众号文章的**网页文本数据**
4. 获取微信公众号文章的**所有信息**，如阅读量、点赞数、转发数、评论、评论点赞等信息。

## 二、项目开发环境及工具

1. 系统环境：Windows 11 ×64
2. 程序运行环境：python 3.13
3. 涉及应用：微信**PC版**，当前项目已适配的微信版本：**`4.1.5.16`**
4. 使用工具：[Fiddler Classic](https://www.telerik.com/fiddler/fiddler-classic)，当前项目适配的Fiddler Classic版本：**`v5.0.20253.3311`**

**目录架构**

```bash
Access_wechat_article/
├── .venv/                # 虚拟环境目录
├── src/                  # 源代码目录 
│   ├── all_process.py    # 流程汇总
│   ├── base_spider.py    # 基础爬虫模块
│   ├── save_to_excel.py  # 存储模块
│   ├── tools.py          # 其他工具模块
│   └── wechat_funcs.py   # 微信token模块
├── LICENSE               # 许可凭证
├── main.py               # 项目主文件
├── README/               # 项目说明文档资源（图片、文件）
├── README.md             # 项目说明文档
└── requirements.txt      # 项目依赖列表
```

## 三、程序使用

### 3.1下载 / Download

- 下载地址：[https://github.com/yeximm/Access_wechat_article/releases](https://github.com/yeximm/Access_wechat_article/releases)
  - 👆👆👆以上为本项目发布页地址，选取所需版本下载即可。


- 存储库快照：[Github_master](https://github.com/yeximm/Access_wechat_article/archive/refs/heads/master.zip)
  - 存储库快照等同于 [Releases](https://github.com/yeximm/Access_wechat_article/releases) 中的 [Source Code (zip)](https://github.com/yeximm/Access_wechat_article/archive/refs/heads/master.zip) 等，包含 `README` 等内容

### 3.2 Python环境配置

（1）创建虚拟环境

```bash
python -m venv .venv
```

`venv`指定存放环境的目录，一般使用 `venv`，这是一个不成文的规定。

（2）**激活**环境

- Windows

  ```bash
  .\.venv\Scripts\activate
  ```

- Unix/macOS

  ```bash
  source .venv/bin/activate
  ```

（3）退出环境

```bash
deactivate
```

### 3.3 安装项目依赖包

`requirements.txt`中包含所需python包文件名称，用来批量安装python包文件

安装命令：

```bash
pip install -r requirements.txt
```

### 3.4 运行参数

1. 项目主文件为：`main.py`，其功能调用方式详见于此。
   项目中**生成文件的存储路径**为：`./all_data`（该目录由程序**自动创建**）
2. 运行命令：
   
   1. 首先进入**虚拟环境**（详见**激活**虚拟环境）
   
   2. 安装python包文件（如已安装则进行下一步）
   
   3. 在项目目录运行：
   
      - ```bash
        python main.py
        ```
   
   4. 根据控制台提示输入
   
   5. 如需**自定义功能**，参照`main.py`中的函数调用方式自行编写。

## 四、功能示例

### 4.1 功能1

```bash
欢迎使用, 请输入数字键！
        数字键1: 获取公众号主页链接
        数字键2: 获取公众号已发布的文章列表
        数字键3: 下载公众号文章内容 (默认下载 "文章列表" 中的所有文章)
        数字键4: 同功能3, 另外获取每篇文章的 "阅读量"、"点赞数"等信息
                 (请注意请求间隔，若请求太多太快可能会触发封禁!!)
        输入其他任意字符退出!
请输入功能数字: 1
```

**程序执行结果**

```bash
########## 默认公众号主页链接为“研招网资讯”，按回车键使用。##########
########## 若需获取其他公众号主页链接，请输入公众号下任意一篇已发布的文章链接。##########
请输入文章链接：https://mp.weixin.qq.com/s/ZNXDr2ErJno9-NdS4RYDCg
为预防被封禁, 短延时：0.906秒
正常获取到文章内容
当前文章为>>>> 法国总统马克龙抵达北京开始访华
公众号名称：新华网
公众号主页: https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzA4MjQxNjQzMA==&scene=124#wechat_redirect
将此链接 （￣︶￣）↗ ↗ ↗ ↗ 粘贴发送到 "微信PC端-文件传输助手"
按回车键继续...
```

### 4.2 功能2

```bash
请输入数字键！
        数字键1: 获取公众号主页链接
        数字键2: 获取公众号已发布的文章列表
        数字键3: 下载公众号文章内容 (默认下载 "文章列表" 中的所有文章)
        数字键4: 同功能3, 另外获取每篇文章的 "阅读量"、"点赞数"等信息
                 (请注意请求间隔，若请求太多太快可能会触发封禁!!)
        输入其他任意字符退出!
请输入功能数字: 2
```

**输入参数**

```bash
########## 以下内容需要用到fiddler工具 ##########
 (1) 在微信客户端打开步骤1获取到的链接,
 (2) 在fiddler中查看——主机地址为https://mp.weixin.qq.com, URL地址为: /mp/profile_ext?acti
 (3) 选中此项后按快捷键: Ctrl+U 复制该网址到剪贴板, 将内容粘贴到此处
请输入复制的链接(づ￣ 3￣)づ：https://mp.weixin.qq.com/mp/profile_ext?xxxxxx...
```

```bash
########## 获取指定页数的文章列表 ##########
一页文章数量约 15 篇, 请根据实际情况估算 (即: input * 15 = 文章数量)
例如: 获取前3页的文章列表, 请输入 3
      公众号下全部文章列表, 请输入: 0  (注意: 若输入0, 全部列表可能需要较长时间, 视文章数量而定)
      公众号下第2页到第5页的文章列表, 请输入 2-5
请输入需要下载的页数(默认: 1): 2-5
```

**程序执行结果**

```bash
参数齐全，开始获取文章信息，默认状态获取全部文章
获取 2 至 5 页的文章列表
正在获取第 2 页文章列表
该页包含 15 篇文章
为预防被封禁,开始延时操作，延时时间：4.962秒
正在获取第 3 页文章列表
该页包含 13 篇文章
为预防被封禁,开始延时操作，延时时间：3.599秒
正在获取第 4 页文章列表
该页包含 14 篇文章
为预防被封禁,开始延时操作，延时时间：6.705秒
正在获取第 5 页文章列表
该页包含 12 篇文章
为预防被封禁,开始延时操作，延时时间：3.075秒
已检测到公众号名称: 新华网

2025-12-03 17:37:16 存储路径>>>> all_data\公众号----新华网\文章列表 (article_list).xlsx
文章列表保存成功
按回车键继续...
```

### 4.3 功能3

```bash
请输入数字键！
        数字键1: 获取公众号主页链接
        数字键2: 获取公众号已发布的文章列表
        数字键3: 下载公众号文章内容 (默认下载 "文章列表" 中的所有文章)
        数字键4: 同功能3, 另外获取每篇文章的 "阅读量"、"点赞数"等信息
                 (请注意请求间隔，若请求太多太快可能会触发封禁!!)
        输入其他任意字符退出!
请输入功能数字: 3
```

**输入参数**

```bash
########## 保存公众号文章内容 ##########
输入: 已下载文章列表的公众号名称 (例如: 研招网资讯) 或 公众号的一篇文章链接
(若当前会话已执行过步骤2, 可按回车跳过)
请输入: 新华网
```

```bash
########## 是否保存图片 ##########
是否保存图片? 是(输入任意值), 否(默认，按回车跳过):y
```

**程序执行结果**

```bash
为预防被封禁, 短延时：1.043秒
正常获取到文章内容
当前文章为>>>> “时速能破150公里”？这种“爆改”太吓人！
为预防被封禁, 短延时：0.988秒
正常获取到文章内容
当前文章为>>>> 流感季，发烧了怎么办？
...
正常获取到文章内容
当前文章为>>>> 武装袭击事件，中国公民3死1伤！我使馆紧急提醒→
2025-12-03 17:40:43 存储路径>>>> all_data\公众号----新华网\文章内容 (article_contents).xlsx
2025-12-03 17:40:43 存储路径>>>> all_data\公众号----新华网\问题链接 (error_links).xlsx
按回车键继续...
```

### 4.4 功能4

```bash
请输入数字键！
        数字键1: 获取公众号主页链接
        数字键2: 获取公众号已发布的文章列表
        数字键3: 下载公众号文章内容 (默认下载 "文章列表" 中的所有文章)
        数字键4: 同功能3, 另外获取每篇文章的 "阅读量"、"点赞数"等信息
                 (请注意请求间隔，若请求太多太快可能会触发封禁!!)
        输入其他任意字符退出!
请输入功能数字: 4
```

**输入参数**

```bash
########## 保存公众号文章详情 ##########
以下内容需要用到fiddler工具, 参考步骤2将 URL地址 粘贴到此处
请输入复制的链接(づ￣ 3￣)づ: https://mp.weixin.qq.com/mp/profile_ext?xxxxxx...
```

**程序执行结果**

```bash
参数齐全，开始获取文章信息，默认状态获取全部文章
获取 1 至 1 页的文章列表
正在获取第 1 页文章列表
该页包含 13 篇文章
为预防被封禁,开始延时操作，延时时间：5.049秒
为预防被封禁, 短延时：0.148秒
正常获取到文章内容
当前文章为>>>> 湖南省人大常委会原党组成员、副主任叶红专被查
为预防被封禁, 短延时：0.702秒
...
正常获取到文章内容
当前文章为>>>> 武装袭击事件，中国公民3死1伤！我使馆紧急提醒→
为预防被封禁,开始延时操作，延时时间：5.352秒
2025-12-03 17:48:43请求完成, 文章标题为: 武装袭击事件，中国公民3死1伤！我使馆紧急提醒→
2025-12-03 17:48:44 存储路径>>>> all_data\公众号----新华网\文章详情 (article_detiles).xlsx
2025-12-03 17:48:44 存储路径>>>> all_data\公众号----新华网\问题链接 (error_links).xlsx
按回车键继续...
```

## 五、鼓励一下

开源不易，若此项目有帮到你，望你能动用你的发财小手**Star**☆一下。

如有遇到代码方面的问题，欢迎一起讨论，你的鼓励是这个项目继续更新的最大动力！

<p align = "center">    
<img  src="https://github.com/yeximm/Access_wechat_article/blob/master/README/qrcode_1749894334903.jpg" width="300" />
</p>



另外，十分感谢大家对于本项目的关注。

[![Stargazers repo roster for @yeximm/Access_wechat_article](https://reporoster.com/stars/yeximm/Access_wechat_article)](https://github.com/yeximm/Access_wechat_article/stargazers)
[![Forkers repo roster for @yeximm/Access_wechat_article](https://reporoster.com/forks/yeximm/Access_wechat_article)](https://github.com/yeximm/Access_wechat_article/network/members)

## 六、程序流程图

![wechat_article_drawio](./README/wechat_article_drawio.png)

### 6.1 基础爬虫模块

![image-20251203185742977](README/image-20251203185742977.png)

### 6.2 获取文章列表模块（需token）

![image-20251203185757196](README/image-20251203185757196.png)

### 6.3 文章内容获取

![image-20251203185810439](README/image-20251203185810439.png)

### 6.4 文章详细信息获取（需token）

![image-20251203185822659](README/image-20251203185822659.png)

## LICENSE

本作品采用许可协议 <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International</a> ,简称 **[CC BY-NC-SA 4.0](http://creativecommons.org/licenses/by-nc-sa/4.0/)**。

所有以任何方式查看本仓库内容的人、或直接或间接使用本仓库内容的使用者都应仔细阅读此声明。本仓库管理者保留随时更改或补充此免责声明的权利。一旦使用、复制、修改了本仓库内容，则视为您已接受此免责声明。

项目内容仅供学习研究，请勿用于商业用途。如对本仓库内容的功能有需求，应自行开发相关功能。所有基于本仓库内容的源代码，进行的任何修改，为其他个人或组织的自发行为，与本仓库内容没有任何直接或间接的关系，所造成的一切后果亦与本仓库内容和本仓库管理者无关。

本仓库内容中涉及的第三方硬件、软件等，与本仓库内容没有任何直接或间接的关系。本仓库内容仅对部署和使用过程进行客观描述，不代表支持使用任何第三方硬件、软件。使用任何第三方硬件、软件，所造成的一切后果由使用的个人或组织承担，与本仓库内容无关。

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yeximm/Access_wechat_article&type=Date)](https://www.star-history.com/#yeximm/Access_wechat_article&Date)

