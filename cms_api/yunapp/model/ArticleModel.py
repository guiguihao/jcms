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
        'recommend':[int,int,int,int,int,int,int,int], #推荐类型 0未推荐 1推荐
        'content':unicode, #markdown代码
        'htmlcontent':unicode, #html代码
        'review':int, #0未审核 1,审核
        'push':int,   #0,未发布 1发布
        'reserved_1':unicode,    #预留字段1
        'reserved_2':unicode,    #预留字段1
        'reserved_3':unicode,    #预留字段1
        'reserved_4':unicode,    #预留字段1
        'del':int, #0 存在 1删除
    }
   validators = {
        'title': max_length(50),
        'overview': max_length(520),
        'author': max_length(50),
        'type': max_length(120),
        'content': max_length(10000),
        'htmlcontent': max_length(10000),
    }
   default_values = {
        'del': 0,
        'date':datetime.datetime.now(),
        'review':0,
        'push': 0,
        'source':0,
        'recommend': [0, 0, 0, 0, 0, 0, 0, 0],
    }
   use_dot_notation = True

