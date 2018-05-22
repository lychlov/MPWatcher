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
            title = article.title
            summary = article.summary
            cover_url = article.cover
            receive_time = msg.receive_time
            alert_msg = "接收到推文来自：%s\n标题：%s\n url:%s" % (msg.sender.name, title, content_url)
            # 通知用户接受文章
            bot.self.send(alert_msg)
            # 调用爬取任务

    my_mp_msg = msg


# @bot.register(except_self=False)
# def print_group_msg(msg):
#     print(msg)


# 南周知道 : 儿童性早熟真会和拉丁舞扯上关系？ (Sharing)

embed()
