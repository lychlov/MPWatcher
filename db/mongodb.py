# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     mongodb
   Description :
   Author :       Lychlov
   date：          2018/5/23
-------------------------------------------------
   Change Activity:
                   2018/5/23:
-------------------------------------------------
"""
import sys

from utils import get_mongo_uri

sys.path.append('../')
import pymongo

MONGO_URI = get_mongo_uri()


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_inst'):
            cls._inst = super(Singleton, cls).__new__(cls, *args, **kwargs)

        return cls._inst


class MongoDB(Singleton):
    def __init__(self, mongo_uri=MONGO_URI):
        super(MongoDB, self).__init__()

        if not hasattr(self, '_db'):
            try:
                with pymongo.MongoClient(mongo_uri) as client:
                    self._db = client.get_database()
            except Exception as e:
                raise

    def get_db(self):
        return self._db

    def find(self, table, condition={}, limit=0, sort=[]):
        '''
        @summary: 查询
        ---------
        @param table: 表名
        @param condition: 条件 默认查询全部
        @param limit: 个数限制 默认查询全部
        @param sort: 排序 默认不排序
        ---------
        @result:
        '''

        result = []
        if sort:
            result = self._db[table].find(condition).limit(limit).sort(sort)
        else:
            result = self._db[table].find(condition).limit(limit)

        return list(result)

    def add(self, table, key_value):
        '''
        @summary: 添加 表不存在自动创建表
        ---------
        @param table: 表名
        @param key_value: 要添加的值 字典格式
        ---------
        @result: True / False
        '''

        try:
            self._db[table].save(key_value)
        except Exception as e:
            return False
        else:
            return True

    def update(self, table, old_value, new_value, multi=True):
        """
        @summary: 更新
        ---------
        @param table: 表名
        @param old_value: 旧值
        @param new_value: 新值
        @param multi: 是否删除多个 默认是
        ---------
        @result:
        """

        try:
            self._db[table].update(old_value, {'$set': new_value}, multi=multi)
        except Exception as e:
            return False
        else:
            return True

    def delete(self, table, condition={}):
        '''
        @summary: 删除数据
        ---------
        @param table: 表名
        @param condition: 删除条件 {}删除所有
        ---------
        @result:
        '''
        try:
            self._db[table].remove(condition)
        except Exception as e:
            return False
        else:
            return True

    def set_unique_key(self, table, key):
        try:
            self._db[table].ensure_index(key, unique=True)
        except:
            pass

    def set_ensure_index(self, table, key):
        try:
            self._db[table].ensure_index(key, unique=False)
        except Exception as e:
            pass
