#!/usr/bin/python
#-*-coding:utf-8 -*-
from yunapp import connection,Document
import datetime
from mongokit import OR


def max_length(length):
    def validate(value):
        if len(value) <= length:
            return True
    return validate


@connection.register
class Article(Document):
   __collection__ = 'article'
   __database__ = 'app'
   structure = {
        'title': unicode,
        'overview':unicode,
        'author':unicode,
        'type':unicode,
        'appkey': unicode,
        'date': OR(unicode,datetime.datetime),
        'source':int, #0 转发 1原创
        'recommend':unicode, #推荐类型
        'content':unicode, #markdown代码
        'htmlcontent':unicode, #html代码
        'status':int, #0未审核 1,审核,2,保存 3发布
        'reserved_1':unicode,    #预留字段1
        'reserved_2':unicode,    #预留字段1
        'reserved_3':unicode,    #预留字段1
        'reserved_4':unicode,    #预留字段1
        'reserved_5': unicode,  # 预留字段1
        'reserved_6': unicode,  # 预留字段1
        'reserved_7': unicode,  # 预留字段1
        'del':int, #0 存在 1删除
    }
   validators = {
        'title': max_length(50),
        'overview': max_length(520),
        'author': max_length(50),
        'type': max_length(120),
        'recommend': max_length(120),
        'content': max_length(10000),
        'htmlcontent': max_length(10000),
    }
   default_values = {
        'del': 0,
        'date':datetime.datetime.now(),
        'status':0,
        'source':0,
    }
   use_dot_notation = True

