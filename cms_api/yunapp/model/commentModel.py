#!/usr/bin/python
#-*-coding:utf-8 -*-
from yunapp import connection,Document



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
   __collection__ = 'Comment'
   __database__ = 'type'
   structure = {
        'pid': unicode,           #文章或产品id
        'level':int,              #评价级别 1- 5
        'content': unicode,       #内容
        'appkey':unicode,
        'del': int, #0 存在 1删除
    }
    required = ['pid','level','content','appkey']
    validators = {
        'name': max_length(100),
        'content': max_length(1000),
        'level':max_value(),
    }
    default_values = {
        'del': 0,
        'sort':0,
    }
   use_dot_notation = True