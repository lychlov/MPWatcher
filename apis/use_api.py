# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     use_api.py
   Description :
   Author :       Lychlov
   date：          2018/5/22
-------------------------------------------------
   Change Activity:
                   2018/5/22:
-------------------------------------------------
"""
import json

import requests

from utils import get_header, get_true_video_api_url

TRUE_VIDEO_API_URL = get_true_video_api_url()


def get_true_video_url(fake_url):
    sess = requests.Session()
    headers = get_header()
    url = TRUE_VIDEO_API_URL + fake_url
    try:
        res = sess.get(url, headers=headers)
        result = json.loads(res.text, encoding='utf-8')
        string = result.get('data')[0].get('url')
        return string
    except Exception as e:
        print("视频真实地址API调用失败")
        print(e)

def get_article_info(article_url):
    pass
