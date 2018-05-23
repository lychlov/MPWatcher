# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     article_crawler
   Description :
   Author :       Lychlov
   date：          2018/5/22
-------------------------------------------------
   Change Activity:
                   2018/5/22:
-------------------------------------------------
"""
import os
import urllib
from urllib.parse import urlparse, parse_qs

import _thread
import pymongo
from time import sleep
import re
import requests
from lxml import etree

from apis.use_api import get_true_video_url
from db.mongodb import MongoDB
from utils import get_header, get_img_store


# url = 'https://mp.weixin.qq.com/s?__biz=MzU0MjQ1ODQxMA==&mid=2247483940&idx=1&sn=8ad01dc2c4305993f861a7bea1f16137&chksm=fb1b1561cc6c9c7745c9eb4d5b7eb10e81eeec882b4c33fc4ada783b7ac20cbf00bea8896954&mpshare=1&scene=1&srcid=0507ZVlFoGCAsgxRyQ3Xdp80&pass_ticket=HWZMx5AHq59uTXZQp9X91Qxlbq0loKsy%2FEUaHDPvT1iJL%2FflpXc4bmButMhmEme3#rd'


# url = 'https://mp.weixin.qq.com/s?__biz=MzAwMDI2MjU1Ng==&mid=2650495904&idx=1&sn=4b980f1f42dd852fbd8b8079f5807f3c&chksm=82e45353b593da457efd8eaa2157b9a6a950f39dc21d3d9519cd4cf369f330370e8c5033bb08&mpshare=1&scene=1&srcid=0523vcBvLDobWeoXMAZjeU9b&pass_ticket=N0owVjmLJQsStOHKTn5v%2BLwmBqT5AvSKO6NQgn4yslQOaDmH3VIaaQJvEmMJK6OT#rd'


# content_url = article.url
# title = article.title
# summary = article.summary
# cover_url = article.cover
# receive_time = msg.receive_time

def url2dict(url):
    query = urlparse(url).query
    return dict([(k, v[0]) for k, v in parse_qs(query).items()])


def set_file_title(title):
    file_name = re.sub('[\/:*?"<>|]', '', title)  # 去掉非法字符
    return file_name


def check_file_path(dict_info, file_path='', ):
    account = set_file_title(dict_info.get('account', 'unkown'))
    title = set_file_title(dict_info.get('title', 'unkown'))
    file_path = get_img_store()
    file_dir = os.path.join(file_path, account, title)
    if not os.path.exists(file_dir):
        # 如果不存在则创建目录
        #  创建目录操作函数
        os.makedirs(file_dir)
    return file_dir


def download_videos(dict_info, file_path='', video_urls=[]):
    file_dir = check_file_path(dict_info, file_path)
    for fake_url in video_urls:
        vid = url2dict(fake_url).get('vid', 'unknown')
        file_name = vid + ".mp4"
        true_url = get_true_video_url(fake_url)
        video_file = requests.get(true_url, stream=True, timeout=10)
        if video_file.status_code == 403:
            print("下载视频失败")
        with open(file_dir + "/" + file_name, 'wb') as fh:
            for chunk in video_file.iter_content(chunk_size=1024):
                fh.write(chunk)
        print("下载视频：%s 完成" % file_name)
        sleep(10)
    pass


def download_pictures(dict_info, file_path='', picture_urls=[]):
    file_dir = check_file_path(dict_info, file_path)
    for picture_url in picture_urls:
        pic_type = picture_url.split('=')[-1]
        file_name = picture_url.split('/')[4] + "." + pic_type
        try:
            pic = requests.get(picture_url, timeout=5)
            fp = open(file_dir + "/" + file_name, 'wb')
            fp.write(pic.content)  # 写入图片
            fp.close()
        except IOError as e:
            print('文件操作失败', e)
        except Exception as e:
            print('错误 ：', e)
        sleep(2)
    pass


def crawl_article(dicts):
    """
    :param dicts: 
    """
    # print(dicts)
    for article_dict in dicts:
        sess = requests.Session()
        headers = get_header()
        url = article_dict.get('url')
        print("开始爬取：%s" % url)
        res = sess.get(url, headers=headers)
        selector = etree.HTML(res.text)
        # print(res.text)
        rich_media = selector.xpath(
            "//div[@class='rich_media_inner']/div[@id='page-content']/div[1]/div[2]")[0]
        author = selector.xpath("//div[@id='meta_content']/span[@class='rich_media_meta rich_media_meta_text']")[
            0].xpath(
            "string(.)")
        __biz = url2dict(url).get('__biz', '')
        # 正文文字
        content = rich_media.xpath("string(.)")
        # 图片集合
        picture_urls = selector.xpath("//img/@data-src")
        # 视频集合
        video_urls = selector.xpath("//iframe[@class='video_iframe']/@data-src")
        mongodb = MongoDB()
        article_item = {'title': article_dict.get('title', ""), 'author': author,
                        'summary': article_dict.get('summary', ""),
                        'cover': article_dict.get('cover', ""), 'content': content, 'like_num': 0, 'read_num': 0,
                        'comment': "", 'url': url, 'receive_time': article_dict.get('receive_time', ""),
                        'account': article_dict.get('account', ""), '__biz': __biz}
        mongodb.add("wechat_article", article_item)
        try:
            download_pictures(dict_info=article_item, picture_urls=picture_urls)
            _thread.start_new_thread(download_videos, (article_item, '', video_urls))

        except:
            print("下载多媒体内容失败")
        sleep(60)
    pass

# download_pictures(title='水电费克里斯反馈算法开始是劳动法几十块了房间', biz="KLJSKLASJDKLJSKLD==")
