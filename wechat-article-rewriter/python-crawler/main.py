from src.all_process import AccessWechatArticle


if __name__=="__main__":
    AWA = AccessWechatArticle()
    screen_text = '''请输入数字键！
        数字键1: 获取公众号主页链接
        数字键2: 获取公众号已发布的文章列表 
        数字键3: 下载公众号文章内容 (默认下载 "文章列表" 中的所有文章)
        数字键4: 同功能3, 另外获取每篇文章的 "阅读量"、"点赞数"等信息
                 (请注意请求间隔，若请求太多太快可能会触发封禁!!)
        输入其他任意字符退出!'''
    print('欢迎使用, ' + screen_text)
    while True:
        text = str(input('请输入功能数字: '))

        if text == '1':
            screen_text1 = '########## 默认公众号主页链接为“研招网资讯”，按回车键使用。##########\n' + \
                           '########## 若需获取其他公众号主页链接，请输入公众号下任意一篇已发布的文章链接。##########\n' + \
                           '请输入文章链接：'
            temporary_url = (input(screen_text1) or 'https://mp.weixin.qq.com/s/4r_LKJu0mOeUc70ZZXK9LA')
            AWA.get_public_main_link(temporary_url)
            
            input("按回车键继续...")
            print('\n' + screen_text)

        elif text == '2':
            screen_text21 = '\n########## 以下内容需要用到fiddler工具 ##########\n' + \
                            ' (1) 在微信客户端打开步骤1获取到的链接,\n' + \
                            ' (2) 在fiddler中查看——主机地址为https://mp.weixin.qq.com, URL地址为: /mp/profile_ext?acti\n' + \
                            ' (3) 选中此项后按快捷键: Ctrl+U 复制该网址到剪贴板, 将内容粘贴到此处\n' + \
                            '请输入复制的链接(づ￣ 3￣)づ：'
            access_token = input(screen_text21)
            screen_text22 = '\n########## 获取指定页数的文章列表 ##########\n' + \
                            '一页文章数量约 15 篇, 请根据实际情况估算 (即: input * 15 = 文章数量)\n' + \
                            '例如: 获取前3页的文章列表, 请输入 3 \n' + \
                            '      公众号下全部文章列表, 请输入: 0  (注意: 若输入0, 全部列表可能需要较长时间, 视文章数量而定)\n' + \
                            '      公众号下第2页到第5页的文章列表, 请输入 2-5 \n' + \
                            '请输入需要下载的页数(默认: 1): '            
            pages = input(screen_text22) or '1'
            if '-' in pages:
                pages = pages.split('-')
                pages_start = int(pages[0])
                pages_end = int(pages[1])
                AWA.get_article_list(access_token, pages_start, pages_end)
            else:
                pages = int(pages)
                AWA.get_article_list(access_token, pages)

            input("按回车键继续...")
            print('\n' + screen_text)

        elif text == '3':   # 该功能不需要token
            screen_text31 = '\n########## 保存公众号文章内容 ##########\n' + \
                            '输入: 已下载文章列表的公众号名称 (例如: 研招网资讯) 或 公众号的一篇文章链接 \n' + \
                            '(若当前会话已执行过步骤2, 可按回车跳过)\n' + \
                            '请输入: '
            nickname = input(screen_text31)
            screen_text32 = '\n########## 是否保存图片 ##########\n' + \
                            '是否保存图片? 是(输入任意值), 否(默认，按回车跳过): '
            save_img = input(screen_text32)
            AWA.save_article_content(str(nickname), save_img)
            
            input("按回车键继续...")
            print('\n' + screen_text)

        elif text == '4':
            screen_text41 = '\n########## 保存公众号文章详情 ##########\n' + \
                            '以下内容需要用到fiddler工具, 参考步骤2将 URL地址 粘贴到此处\n' + \
                            '请输入复制的链接(づ￣ 3￣)づ: '
            access_token = input(screen_text41)
            AWA.save_article_details(access_token)
            
            input("按回车键继续...")
            print('\n未成功获取的链接已保存到本地。' + '\n' + screen_text)

        else:
            print('\n已成功退出！')
            break


