"""
    该模块包含了微信公众号token相关的函数
"""
from urllib import parse    # 用于解析获取url参数
import re
import time
import json
import random
import jsonpath

from src.base_spider import BaseSpider


class ArticleDetail(BaseSpider):
    """
        功能描述：
            使用token获取公众号内容
    """
    def __init__(self):
        super().__init__()
        self.biz = None
        self.uin = None
        self.key = None
        self.pass_ticket = None
        self.text = 'website'  # 预留位，保证返回值不会报错        

    def format_raw_link(self, token_url):
        """
            功能描述：
                检验token是否合法
                格式化原始链接, 提取出biz、uin、key、pass_ticket等参数
            输入：
                原始链接(包含token等参数)
            输出：
                无（参数值存储在类的属性中）
        """
        # 检验access_token是否合法
        access_token=parse.urlparse(token_url)    # 解析url，拆解为各主体信息，目标为query参数
        query_dict = parse.parse_qs(access_token.query)

        self.biz = query_dict['__biz'][0]
        self.uin = query_dict['uin'][0]
        self.key = query_dict['key'][0]
        self.pass_ticket = query_dict['pass_ticket'][0]

        if self.biz and self.uin and self.pass_ticket and self.key:
            # print('参数齐全，开始获取文章信息，默认状态获取全部文章')
            return True
        else:
            print('\n※※※ 参数有误，请重新输入')
            return False

    
    def whole_article_list(self, pages_start, pages_end):
        """
            功能描述：
                获取文章指定页数的链接列表
            输入：
                需要下载的页数(默认1页)
                若输入为0, 则获取全部文章
            输出：
                无（内容保存在文件）
        """
        all_article_link = []   # 存储所有文章链接
        if pages_start == 0:
            # 遍历公众号下所有文章链接
            page = 0
            passage_list = []
            print('开始获取公众号下所有的文章列表')
            while True:
                p_data = self.get_next_list(page)
                if p_data['m_flag'] == 1:
                    for i in p_data['one_page_list']:
                        passage_list.append(i)
                else:
                    print('请求结束，文章列表获取完毕！')
                    break
                page = page + 1
                self.delay_time()   # 随机延时做模拟手动操作，预防被封禁
            all_article_link = passage_list
        else:
            # 遍历指定页数的文章链接
            print('获取 ' + str(pages_start) + ' 至 ' + str(pages_end) + ' 页的文章列表')
            passage_list = []
            for pages in range(pages_start-1, pages_end):
                p_data = self.get_next_list(pages)
                if p_data['m_flag'] == 1:
                    for i in p_data['one_page_list']:
                        passage_list.append(i)
                else:
                    print('请求结束，文章列表获取完毕！')
                    break
                self.delay_time()   # 随机延时做模拟手动操作，预防被封禁
            all_article_link = passage_list
        # print('********************共获取到 ' + str(len(all_article_link)) + ' 篇文章，开始保存文章，若为 0 篇请检查错误！！！\n')
        if not all_article_link: 
            print('获取到文章列表为空，请注意检查！！！！')
            return None  # 如果获取为空
        else: 
            return all_article_link

        
    def get_next_list(self, page):
        """
            功能描述：
                获取指定页的文章列表
            输入：
                页码
            输出：
                文章列表
        """
        # 从0开始计数，第 0 页相当于默认页数据
        pages = int(page) * 10
        print('正在获取第 ' + str(page + 1) + ' 页文章列表')
        url = ('https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=' + self.biz + '&f=json&offset='
               + str(pages) + '&count=10&is_ok=1&scene=124&uin=' + self.uin + '&key=' + self.key + '&pass_ticket='
               + self.pass_ticket + '&wxtoken=&appmsg_token=&x5=0&f=json')
        try:
            res = self.session.get(url=url, headers=self.headers, timeout=10, verify=False)
        except:
            print('失败！！！获取第 ' + str(page + 1) + ' 页文章列表失败！！！')
            res = ArticleDetail()  # 保证返回值不会报错
        if 'app_msg_ext_info' in res.text:
            # 解码json数据
            get_page = json.loads(json.loads(res.text)['general_msg_list'])['list']
            ''' 
                返回内容解析
                get_page[0]为
                {
                    'comm_msg_info': {
                        'id': 1000000107, 'type': 49, 
                        'datetime': 1722467332, 'fakeid': '3910318108', 'status': 2, 'content': ''
                    }, 
                    'app_msg_ext_info': {
                        'title': '国务院7月重要政策', 
                        'digest': '', 'content': '', 'fileid': 100007840, 
                        'content_url': 'http://mp.weixin.qq.com/s?__biz=MzkxMDMxODEwOA==&amp;mid=2247491511&amp;idx=1&amp;sn=a36291fdee52a0f53d145edec8058e04&amp;chksm=c0084d6abbcac962a50153c89fe9c19b6f8b1c5e5ac50b05adcb49bdfad8638522ab426c3f4b&amp;scene=27#wechat_redirect', 
                        'source_url': '', 
                        'cover': 'https://mmbiz.qpic.cn/mmbiz_jpg/JRAjbHqmggrlZibDMibLP4ryNqhYXgolJOdQj2P8t2QQFVicickzAo7Gv1SzazwJY6lDylcanx2ic60HDbMvK8OKQpg/0?wx_fmt=jpeg', 
                        'subtype': 9, 'is_multi': 1, 
                        'multi_app_msg_item_list': [
                            {'
                                'title': '8月起，这些新规将影响你我生活！', 
                                'digest': '', 'content': '', 'fileid': 0, 
                                'content_url': 'http://mp.weixin.qq.com/s?__biz=MzkxMDMxODEwOA==&amp;mid=2247491511&amp;idx=2&amp;sn=b3f5b6bcf8727c8c90fce7e588e6e7da&amp;chksm=c0eb20c99ca2f90032a6234002ed2cc9c2c000f87cff34f4d8d763878c0bb5275800db876ca7&amp;scene=27#wechat_redirect', 
                                'source_url': '', 
                                'cover': 'https://mmbiz.qpic.cn/mmbiz_jpg/JRAjbHqmggrc08yJMZ6CQ3VL6VzmEIymSUyATlL6o3xaDJJ0D2CtpQg31Vy7jdCaic86zqkgJ9oAFGyia78ZOq7g/0?wx_fmt=jpeg', 
                                'author': '', 'copyright_stat': 100, 'del_flag': 1, 'item_show_type': 0, 'audio_fileid': 0, 
                                'duration': 0, 'play_url': '', 'malicious_title_reason_id': 0, 'malicious_content_type': 0
                            }, 
                            {
                                'title': '8月，你好！', 
                                'digest': '', 'content': '', 'fileid': 100007860, 
                                'content_url': 'http://mp.weixin.qq.com/s?__biz=MzkxMDMxODEwOA==&amp;mid=2247491511&amp;idx=3&amp;sn=cd25de57b74b63b0f3b1a9888b9cd94d&amp;chksm=c0c7f30fdd5fc0ea4a2765f5fd29e1faeb0e352e888ee8556521ab23bc9528d68f42deaa9d15&amp;scene=27#wechat_redirect', 
                                'source_url': '', 
                                'cover': 'https://mmbiz.qpic.cn/mmbiz_jpg/JRAjbHqmggrlZibDMibLP4ryNqhYXgolJO9CnECAnMLDPY39Y9iarcFtM1ibrBvhKcGFyl1wicHysvTrYx4GfLybt8g/0?wx_fmt=jpeg', 
                                'author': '', 'copyright_stat': 100, 'del_flag': 1, 'item_show_type': 0, 'audio_fileid': 0, 
                                'duration': 0, 'play_url': '', 'malicious_title_reason_id': 0, 'malicious_content_type': 0}
                            ], 
                        'author': '', 'copyright_stat': 100, 'duration': 0, 'del_flag': 1, 'item_show_type': 0, 'audio_fileid': 0, 'play_url': '', 'malicious_title_reason_id': 0, 'malicious_content_type': 0
                    }
                }
            '''
            one_page_list = []  # 存放一页内的所有文章
            for i in get_page:
                # 时间戳转换
                time_tuple = time.localtime(i['comm_msg_info']['datetime'])
                create_time = time.strftime("%Y-%m-%d", time_tuple)
                local_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 本地时间

                # 每日首篇文章的标题
                article_title = i['app_msg_ext_info']['title']
                content_cover = i['app_msg_ext_info']['cover']
                content_url = i['app_msg_ext_info']['content_url'].replace('#wechat_redirect', '')
                format_url = content_url.replace('amp;', '')
                
                temproary_page = page + 1   # 临时页码，用于抓取中断时的记录
                one_page_list.append([temproary_page, local_time, create_time, article_title, content_cover, content_url, format_url])

                if i['app_msg_ext_info']['multi_app_msg_item_list']:
                    for j in i['app_msg_ext_info']['multi_app_msg_item_list']:
                        article_title = j['title']
                        content_cover = j['cover']
                        content_url = j['content_url'].replace('#wechat_redirect', '')
                        format_url = content_url.replace('amp;', '')
                        one_page_list.append([temproary_page, local_time, create_time, article_title, content_cover, content_url, format_url])
            print('该页包含 ' + str(len(one_page_list)) + ' 篇文章')
            return {
                'm_flag': 1,
                'one_page_list': one_page_list,
                'length': len(one_page_list)
            }
        elif '"home_page_list":[]' in res.text:
            print('\n出现：操作频繁，请稍后再试\n该号已被封禁，请解封后再来！！！\n')
            return {'m_flag': 0}
        else:
            print('请求结束！未获取到第 ' + str(page + 1) + ' 页文章列表')
            return {'m_flag': 0}
        
    def get_detail_nickname(self):
        """
            功能描述：
                使用token获取公众号名称
            输入：
                无
            输出：
                无
        """
        # 提取nickname
        first_page_list = self.whole_article_list(1, 1)   # 获取第一页的文章列表
        if not first_page_list:
            print('获取文章列表失败')
            return None
        article_index = 0
        first_content = self.get_an_article(first_page_list[article_index][6])   # 提取nickname
        if first_content['content_flag'] == 0:
            print('提取第 ' + str(article_index + 1) + ' 篇文章的公众号名称失败')
            for i in range(1, len(first_page_list)):
                first_content = self.get_detail_nickname(first_page_list[i][6])   # 提取nickname
                if first_content['content_flag'] == 1:
                    break
            return None
        self.format_content(first_content['content'])   # 将公众号名称填入类属性
    
    def get_detail_content(self, source_url, article_title, one_content):
        """
            功能描述：
                获取单篇文章的文章详情
            输入：
                单篇文章的列表数据
            输出：
                当前文章的详情数据
        """
        # 设置延时
        self.delay_time()
        # 构建关键参数
        r = ''
        for rand in range(0, 16):
            r += str(random.randint(0, 9))
        r = '0.' + r
        appmsg_type = "9"
        mid = str(source_url).split('mid=')[1].split('&')[0]
        sn = str(source_url).split('sn=')[1].split('&')[0]
        idx = str(source_url).split('idx=')[1].split('&')[0]

        comment_id = re.search("var comment_id = '(.*?)'.*", one_content)
        if comment_id:
            comment_id = comment_id.group(1)
        else:
            print('没有匹配到comment_id, 文章标题为: ' + article_title)
            comment_id = ''
        if 'var req_id = ' in one_content:
            req_id = one_content.split('var req_id = ')[1].split(';')[0].replace("'", "").replace('"', '')
        else:
            print('没有匹配到req_id, 文章标题为: ' + article_title)
            req_id = ''

        '''获取文章详情信息'''
        detail_url = ('https://mp.weixin.qq.com/mp/getappmsgext?f=json&mock=&fasttmplajax=1&f=json' + '&uin=' + self.uin
                      + '&key=' + self.key + '&pass_ticket=' + self.pass_ticket + '&__biz=' + self.biz)
        data = {
            'r': r,
            'sn': sn,
            'mid': mid,
            'idx': idx,
            'req_id': req_id,
            'title': article_title,
            'comment_id': comment_id,
            'appmsg_type': appmsg_type,
            '__biz': self.biz,
            'pass_ticket': self.pass_ticket,
            'abtest_cookie': '', 'devicetype': 'Windows 10 x64', 'version': '63090b13', 'is_need_ticket': '0',
            'is_need_ad': '0', 'is_need_reward': '0', 'both_ad': '0', 'reward_uin_count': '0', 'send_time': '',
            'msg_daily_idx': '1', 'is_original': '0', 'is_only_read': '1', 'scene': '38', 'is_temp_url': '0',
            'item_show_type': '0', 'tmp_version': '1', 'more_read_type': '0', 'appmsg_like_type': '2',
            'related_video_sn': '', 'related_video_num': '5', 'vid': '', 'is_pay_subscribe': '0',
            'pay_subscribe_uin_count': '0', 'has_red_packet_cover': '0', 'album_id': '1296223588617486300',
            'album_video_num': '5', 'cur_album_id': 'undefined', 'is_public_related_video': 'NaN',
            'encode_info_by_base64': 'undefined', 'exptype': '', 'export_key_extinfo': '', 'business_type': '0',
        }
        res = self.session.post(url=detail_url, data=data, headers=self.headers, cookies=self.cookies, verify=False)
        # print(res.text)
        read_num = jsonpath.jsonpath(json.loads(res.text), "$.." + "read_num")
        like_num = jsonpath.jsonpath(json.loads(res.text), "$.." + "old_like_num")
        share_num = jsonpath.jsonpath(json.loads(res.text), "$.." + "share_num")
        show_read = jsonpath.jsonpath(json.loads(res.text), "$.." + "show_read")

        # 获取评论以及评论点赞数
        comment_url = ('https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment&__biz=' + self.biz +
                       '&appmsgid=2247491372&idx=1&comment_id=' + comment_id + '&offset=0&limit=100&uin='
                       + self.uin + '&key=' + self.key + '&pass_ticket=' + self.pass_ticket
                       + '&wxtoken=&devicetype=Windows+10&clientversion=62060833&appmsg_token=')
        response = self.session.get(comment_url, headers=self.headers, cookies=self.cookies, verify=False)
        json_content = json.loads(response.text)
        comments = jsonpath.jsonpath(json_content, '$..content')                    # 评论
        comments_star_nums = jsonpath.jsonpath(json_content, '$..like_num')         # 评论点赞数

        local_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())         # 本地时间
        print(str(local_time) + '请求完成, 文章标题为: ' + article_title)
        if read_num == [] or read_num == '':
            return None
        else:
            return (read_num[0], like_num[0], share_num[0], show_read[0],  # 阅读量，点赞数，转发数，在看数，
                    comments, comments_star_nums)  # 评论，评论点赞
        


        




        
        