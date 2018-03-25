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

@connection.register
class Type(Document):
   __collection__ = 'type'
   __database__ = 'app'
   structure = {
        'level': int,
        'name':unicode,
        'dec':unicode,
        'appkey':unicode,
        'date':OR(unicode,datetime.datetime),
        'type':IS(u'article', u'shop', u'user'),
        'parentID':unicode, 
        'reserved_1':unicode,    #预留字段1 
        'reserved_2':unicode,    #预留字段1 
        'reserved_3':unicode,    #预留字段1 
        'reserved_4':unicode,    #预留字段1 
        'del': int,#0 存在 1删除
    }
   validators = {
        'name': max_length(50),
        'dec': max_length(10000),
        'reserved_1': max_length(10000),
        'reserved_2': max_length(10000),
        'reserved_3': max_length(10000),
        'reserved_4': max_length(10000),
    }
   default_values = {
        'del': 0,
        'date':datetime.datetime.now(),
        'level':1,
        'parentID':u'', 
    }
   use_dot_notation = True
 