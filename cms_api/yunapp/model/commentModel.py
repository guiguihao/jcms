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
        'content': unicode,       #内容
        'imgs':[unicode],
        'appkey':unicode,
        'date': OR(unicode, datetime.datetime),
        'del': int, #0 存在 1删除
    }
   required = ['oid','level','content','appkey']
   validators = {
        'oid': max_length(100),
        'content': max_length(1000),
   }
   default_values = {
        'del': 0,
        'date': datetime.datetime.now(),
   }
   use_dot_notation = True