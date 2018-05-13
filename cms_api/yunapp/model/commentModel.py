#!/usr/bin/python
#-*-coding:utf-8 -*-
from yunapp import connection,Document
import datetime
from mongokit import OR
from mongokit import IS


def max_length(length):
    def validate(value):
        if len(value) <= length:
            return True
        raise Exception('%s must be at most %s characters long' % length)
    return validate
def max_value(length):
    def validate(value):
        if value>=0 and value<=5:
            return True
        raise Exception('%s must be at most %s characters long' % length)
    return validate

@connection.register
class Comment(Document):
   __collection__ = 'col'
   __database__ = 'comment'
   structure = {
        'oid': unicode,           #文章或产品id
        'level':int,              #评价级别 1- 5
        'type': IS(0,1),          #0留言 1评论
        'content': unicode,       #内容
        'imgs':[unicode],
        'userId':unicode,
        'appkey':unicode,
        'date': OR(unicode, datetime.datetime),
        'answer':unicode,
        'reserved_1': unicode,  # 预留字段1
        'reserved_2': unicode,  # 预留字段1
        'reserved_3': unicode,  # 预留字段1
        'reserved_4': unicode,  # 预留字段1
        'del': int, #0 存在 1删除
    }
   required = ['oid','level','content','appkey','userId']
   validators = {
        'oid': max_length(100),
        'content': max_length(1000),
        'answer': max_length(1000),
   }
   default_values = {
        'del': 0,
        'type':0,
        'date': datetime.datetime.now(),
   }
   use_dot_notation = True