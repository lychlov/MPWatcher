# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     wechat_watcher
   Description :
   Author :       Lychlov
   date：          2018/5/22
-------------------------------------------------
   Change Activity:
                   2018/5/22:
-------------------------------------------------
"""
from wxpy import *
from time import sleep
from crawler.article_tasks import crawl_article
from utils import MP_ACCOUNT

bot = Bot(cache_path=True,qr_path='')
bot.self.add()
bot.self.accept()


# bot.self.send('能收到吗？')


# bot.add_mp(user='oNetwork')

def check_mps():
    my_mps = bot.mps(update=True)


@bot.register(msg_types=SHARING, except_self=False)
def auto_add_mps(msg):
    # print("收到微信公众号推文")
    # print(msg)
    # print(msg.id)
    # print(msg.text)
    # print(msg.get_file)
    # print(msg.sender)
    # print(msg.receive_time)
    # print(msg.url)
    # print(msg.articles)
    # print(msg.cover)
    if msg.sender.name in MP_ACCOUNT:
        print("hit %s" % msg.sender.name)
    else:
        print("miss %s" % msg.sender.name)
        # return
    if msg.articles is None:
        return
    if msg.articles is not None:
        for article in msg.articles:
            content_url = article.url
            temp_dict = dict()
            temp_dict['title'] = article.title
            temp_dict['summary'] = article.summary
            temp_dict['cover'] = article.cover
            temp_dict['receive_time'] = msg.receive_time
            temp_dict['account'] = msg.sender.name

            alert_msg = "接收到推文来自：%s\n标题：%s\n url:%s" % (msg.sender.name, article.title, content_url)
            # 通知用户接受文章
            bot.file_helper.send(alert_msg)
            # 调用爬取任务
            crawl_article(url=content_url, dict_info=temp_dict)
            sleep(60)

# temp_dict = {"title": "政变四周年，曼谷反军方大示威今日正式爆发！",
#              "summary": 'jianjie',
#              "cover": "http://sdfsdf",
#              "receive_time": "2018-05-23 23:23:23",
#              "account": '泰国网'}
# crawl_article(url=url, dict_info=temp_dict)

embed()
