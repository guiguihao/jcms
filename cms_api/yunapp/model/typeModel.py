#!/usr/bin/python
#-*-coding:utf-8 -*-
from yunapp import connection,Document



def max_length(length):
    def validate(value):
        if len(value) <= length:
            return True
        raise Exception('%s must be at most %s characters long' % length)
    return validate


@connection.register
class Type(Document):
   __collection__ = 'col'
   __database__ = 'type'
   structure = {
        'name': unicode,       #标题
        'parentID':unicode,    #父id 0为大类
        'appkey':unicode,
        'sort':int,            #排序
        'del': int, #0 存在 1删除
    }
   validators = {
        'name': max_length(100),
    }
   default_values = {
        'parentID':u'0',
        'del': 0,
        'sort':0,
    }
   required = ['name','parentID','appkey','sort','del']
   use_dot_notation = True
    