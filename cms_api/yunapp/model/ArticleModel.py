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

#万能快
@connection.register
class WanNeng(Document):
    __collection__ = 'wanneng'
    __database__ = 'wanneng'
    structure = {
        'appkey': unicode,
        'w1': unicode,
        'w2': unicode,
        'w3': unicode,
        'w4': unicode,
        'w5': unicode,
        'w6': unicode,
        'w7': unicode,
        'w8': unicode,
        'w9': unicode,
        'w10': unicode,
        'w11': unicode,
        'w12': unicode,
        'w13': unicode,
        'w14': unicode,
        'w15': unicode,
        'w16': unicode,
        'w17': unicode,
        'date': OR(unicode, datetime.datetime),
        'del': int,  # 0 存在 1删除
    }
    validators = {
        'w1': max_length(500),
        'w2': max_length(500),
        'w3': max_length(500),
        'w4': max_length(500),
        'w5': max_length(500),
        'w6': max_length(500),
        'w7': max_length(500),
        'w8': max_length(500),
        'w9': max_length(500),
        'w10': max_length(500),
        'w11': max_length(500),
        'w12': max_length(500),
        'w13': max_length(500),
        'w14': max_length(500),
        'w15': max_length(500),
        'w16': max_length(500),
        'w17': max_length(500),
    }
    default_values = {
        'del': 0,
        'date': datetime.datetime.now(),
    }
    use_dot_notation = True

