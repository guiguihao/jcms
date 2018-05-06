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
class Img2(Document):
   __collection__ = 'col'
   __database__ = 'img'
   structure = {
        'url': unicode,           #路径
        'size':OR(int,float,unicode),              #大小
        'pf': unicode,       #后缀
        'name': unicode,  # 后缀
        'appkey':unicode,
        'userid': unicode,
        'date': OR(unicode, datetime.datetime),
        'del': int, #0 存在 1删除
    }
   required = ['url','pf','appkey']
   validators = {
        'url': max_length(100),
        'userid': max_length(100),
        'name': max_length(100),
        'pf': max_length(10),
   }
   default_values = {
        'del': 0,
        'date': datetime.datetime.now(),
   }
   use_dot_notation = True