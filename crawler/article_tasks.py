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
from time import sleep
import re
import requests
from lxml import etree

from db.mongodb import MongoDB
from utils import get_header, get_img_store

url = 'https://mp.weixin.qq.com/s?__biz=MzU0MjQ1ODQxMA==&mid=2247483940&idx=1&sn=8ad01dc2c4305993f861a7bea1f16137&chksm=fb1b1561cc6c9c7745c9eb4d5b7eb10e81eeec882b4c33fc4ada783b7ac20cbf00bea8896954&mpshare=1&scene=1&srcid=0507ZVlFoGCAsgxRyQ3Xdp80&pass_ticket=HWZMx5AHq59uTXZQp9X91Qxlbq0loKsy%2FEUaHDPvT1iJL%2FflpXc4bmButMhmEme3#rd'


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


def download_pictures(dict_info, file_path='', picture_urls=[]):
    account = set_file_title(dict_info.get('account', 'unkown'))
    title = set_file_title(dict_info.get('title', 'unkown'))
    file_path = get_img_store()
    file_dir = os.path.join(file_path, account, title)
    if not os.path.exists(file_dir):
        # 如果不存在则创建目录
        #  创建目录操作函数
        os.makedirs(file_dir)
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
        sleep(10)
    pass


def crawl_article(url, dict_info):
    """
    :param recieve_time: 文章接收时间
    :param url: 文章url
    :param title: 文章标题
    :param account_name: string,公众号名
    """
    sess = requests.Session()
    headers = get_header()
    res = sess.get(url, headers=headers)
    selector = etree.HTML(res.text)
    # print(res.text)
    rich_media = selector.xpath(
        "//div[@class='rich_media_inner']/div[@id='page-content']/div[1]/div[2]")[0]
    author = selector.xpath("//div[@id='meta_content']/span[@class='rich_media_meta rich_media_meta_text']")[0].xpath(
        "string(.)")
    __biz = url2dict(url).get('__biz', '')
    # 正文文字
    content = rich_media.xpath("string(.)")
    # 图片集合
    picture_urls = selector.xpath("//img/@data-src")
    # 视频集合
    video_urls = selector.xpath("//iframe[@class='video_iframe']/@data-src")
    mongodb = MongoDB()
    article_item = {}
    article_item['title'] = dict_info.get('title', "")
    article_item['author'] = author
    article_item['summary'] = dict_info.get('summary', "")
    article_item['cover'] = dict_info.get('cover', "")
    article_item['content'] = content
    article_item['like_num'] = 0
    article_item['read_num'] = 0
    article_item['comment'] = ""
    article_item['url'] = url
    article_item['receive_time'] = dict_info.get('receive_time', "")
    article_item['account'] = dict_info.get('account', "")
    article_item['__biz'] = __biz
    mongodb.add("wechat_article", article_item)
    download_pictures(dict_info=article_item, picture_urls=picture_urls)
    pass


# download_pictures(title='水电费克里斯反馈算法开始是劳动法几十块了房间', biz="KLJSKLASJDKLJSKLD==")
temp_dict = {"title": "政变四周年，曼谷反军方大示威今日正式爆发！",
             "summary": 'jianjie',
             "cover": "http://sdfsdf",
             "receive_time": "2018-05-23 23:23:23",
             "account": '泰国网'}
picture_urls = [
    'https://mmbiz.qpic.cn/mmbiz_png/2U1Ohu1dZsyLh2PlRV5ymhSDwicfAH1w4ow8lwNkS4TN5bpkibBB3ibNsP5t3Sk96VN3TI40CbLeRR4u2qs5R8aBA/640?wx_fmt=png',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJPWiandMt7UNGibIXsJ2QelE8PGsyYLbfTnOsvyaETqsOl9KnYwfIR6yQ/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJLdGWUgyiascWSZf2dm5XdHs0kGLmlVytdYic9EFYeX3pN6pN4Y1yJfKA/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJXs4SbAUR7tmWuq91F07sJfiaOKLG1TNbZrAsbnFGzV4pYuKaiazhPBOg/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_png/2U1Ohu1dZsyLh2PlRV5ymhSDwicfAH1w4jicSc4PYic3BepxHFKENpld90m11e9F0iavucibvUZ7ibYqVaasaN7aga0g/640?wx_fmt=png',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJAdQz0T6dZibBoUKf8ziamqHkUTic0Fb8s4ia1Qv2mQQF9llkZCbuEb1IqQ/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJnTzYSve7TGeXXCEicxzuRK43zJcKf7td5omPoaMdHwl53NJ0boSkX4g/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_gif/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJs0uDAia0EsuoFoasQc9Aa9V2icaPjPXWFibZBeretA9mzicKRVaic1JqBtw/640?wx_fmt=gif',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJRrralA7qyqsRicTHm9ubz3ibexiaiblvWpaYRZ7RJuLhvrCf0Pcost4pbQ/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_gif/ENw5LI09ksyeibVR7EEpfOPmSxH69OWibTnmGbiaNajIq5JqPhgfLECAcu41WgoMfzVmeibckD5xhrEf4kIH8J2UnA/640?wx_fmt=gif',
    'https://mmbiz.qpic.cn/mmbiz_gif/nibxMsb16PQQiccxgtA7bxjNbzDs1BrpI7MX16pXEXcCaP6WBQsVJXRdm4oFXLvf27Pu7iabQicJaMr5otibgyFAMaQ/640?wx_fmt=gif',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJWgl0s6m2mNTfUbV8oTsBZxKyOJKBcRcFvCia7T9XSdbHL6gmweT3MQQ/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJA8oVvWKPbJT3VR9Wl8HLiciaDChkGXFesmgM1UPT3GaW6PfWQvPbbpNw/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJtpqCgosZ8icxdDuLr8HvAUvjtDODo0AwxmCX5QONphxQdwMxjicIoJMQ/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJZeuoEvbY4rYuwprzztpLZjMh9rkyRNj0yLpicsuCWpoawVibH0wpzLCg/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJGYwhUnesuPib65aPVibJgT5YdtxSbgic6HFYSa6WgME5ibStXcKKVIy0Fg/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJ3gpOR68dqdnp3BBaQGZ9cBpTmZsepzeNcDa8IK3DicUuHvht2qc7fLg/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJFaIWBN9vRI8tPiatEFOibyn7WdJWCYW9c9HAslL5EE80Ud8CZeZm4mKg/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJG6SfLGOmvFuDvCWyXMfJXsiacQLva0TiaHuE0Vl7Yibn3qBIcuEZJ7n0w/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_gif/ENw5LI09ksyeibVR7EEpfOPmSxH69OWibTnmGbiaNajIq5JqPhgfLECAcu41WgoMfzVmeibckD5xhrEf4kIH8J2UnA/640?wx_fmt=gif',
    'https://mmbiz.qpic.cn/mmbiz_png/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJzGC04A0u33icNVs02dL9z6jxbIKnD47Y9JqUIfyxic8lHwnUBrkvLYRg/640?wx_fmt=png',
    'https://mmbiz.qpic.cn/mmbiz_png/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJD4z3RpfibhBqKA421iaJSo3ic1UF3y1b9GTwBXWwAnuKx8mlr9Tg5Y91Q/640?wx_fmt=png',
    'https://mmbiz.qpic.cn/mmbiz_png/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJqib113SYNsdIM0SF37kUibRMjvsmWs29mpFBdiavJI8XeXNk2EPkictAvQ/640?wx_fmt=png',
    'https://mmbiz.qpic.cn/mmbiz_png/a76nL5zFMCqfKLBIJZ2X4n2dsmdZwvTxqoxHMwLOb5Yjqoqb7IajFdicKwe2xEft7oltZG9qoiaVNYuTtHgmh5bw/640?wx_fmt=png',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJEAgSicxxCvNGicZQpQTXrRiaAfzmibaqyTsXqo4s7UicG0pZpn7LlIN70Qw/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_png/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJibNYSdUzfibpIKTL7dxusrP29JHzP8uctLgSMyXqgoOwD8Q2SaOuC49Q/640?wx_fmt=png',
    'https://mmbiz.qpic.cn/mmbiz_png/yyRO8jtwmzPrTxwABSgXTzXw5WCqTialynibVPmrIwIpVVsibaLYbVqS64oicJXX8tUEGibvdOM783cUGfh5MT962UQ/640?wx_fmt=png',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJdOicl3nicsvsY1hc1lSibwdQb7YYm6tl0UUF8rkMmKgfb66cQYnsJjfUA/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/nSCFwRAl6zs1UndkfCmghhRXHZ9tmI2In35oobHhyicJVtN7ECBnuV1KAia73Pj3XBACfyev3ePlUF839WaCsX8Q/640?wx_fmt=jpeg']
# crawl_article(url=url, dict_info=temp_dict)
# download_pictures(dict_info=temp_dict, picture_urls=picture_urls)
