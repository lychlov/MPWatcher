# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     dbshot
   Description :
   Author :       Lychlov
   date：          2018/5/24
-------------------------------------------------
   Change Activity:
                   2018/5/24:
-------------------------------------------------
"""
from db.mongodb import MongoDB

temp_dict = {"title": "政变四周年，曼谷反军方大示威今日正式爆发！",
             "summary": 'jianjie',
             "cover": "http://sdfsdf",
             "receive_time": "2018-05-23 23:23:23",
             "account": '泰国网'}
temp_dict2 = {"title": "政变四周年，曼谷反军方大示威今日正式爆发！",
              "summary": 'jianjie',
              "account": '泰国网'}
mongodb = MongoDB()
add_res = mongodb.add('wechat_article', temp_dict)

res = mongodb.find('wechat_article', temp_dict2)
print(res)
