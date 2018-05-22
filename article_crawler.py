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
import pymongo
import re
import requests
from lxml import etree

from utils import get_header, get_img_store

url = 'https://mp.weixin.qq.com/s?__biz=MzU0MjQ1ODQxMA==&mid=2247483940&idx=1&sn=8ad01dc2c4305993f861a7bea1f16137&chksm=fb1b1561cc6c9c7745c9eb4d5b7eb10e81eeec882b4c33fc4ada783b7ac20cbf00bea8896954&mpshare=1&scene=1&srcid=0507ZVlFoGCAsgxRyQ3Xdp80&pass_ticket=HWZMx5AHq59uTXZQp9X91Qxlbq0loKsy%2FEUaHDPvT1iJL%2FflpXc4bmButMhmEme3#rd'


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


def download_pictures(title, biz, file_path='', picture_urls=[]):
    title = title[0:10] + "-"+biz
    title = set_file_title(title)
    file_path = get_img_store()
    file_dir = os.path.join(file_path, title)
    if not os.path.exists(file_dir):
        # 如果不存在则创建目录
        #  创建目录操作函数
        os.makedirs(file_dir)
    print(file_dir)
    pass


def crawl_article(url):
    sess = requests.Session()
    headers = get_header()
    res = sess.get(url, headers=headers)
    selector = etree.HTML(res.text)
    # print(res.text)
    rich_media = selector.xpath(
        "/html/body[@id='activity-detail']/div[@id='js_article']/div[@class='rich_media_inner']/div[@id='page-content']/div[@id='img-content']/div[@id='js_content']/*")[
        0]
    picture_urls = selector.xpath("//img/@data-src")
    text_info = rich_media.xpath("string(.)")
    print(text_info)
    print(picture_urls)
    pass


download_pictures(title='水电费克里斯反馈算法开始是劳动法几十块了房间', biz="KLJSKLASJDKLJSKLD==")
