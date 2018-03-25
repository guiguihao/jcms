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
class APP_admin(Document):
   __collection__ = 'app'
   __database__ = 'app'
   structure = {
        'name': unicode,
        'password':unicode,
        'phone':unicode,
        'email': unicode,
        'vip'  :unicode,
        'permission':[int,int,int,int,int,int,int,int], #[0]系统设置 #[1]文章模块 #[2]产品模块 #[3]用户模块 #[4]备用 #[5]备用 
        'qq':unicode,    
        'wachat':unicode,
        'nickname':unicode,
        'appkey':unicode,
        'appsecret':unicode,
        'superadmin':int,        #0不是超级管理员 1超级管理员
        'active':int,            #0未激活 1激活
        'appinfo':unicode,       #app信息
        'reserved_1':unicode,    #预留字段1 
        'reserved_2':unicode,    #预留字段1 
        'reserved_3':unicode,    #预留字段1 
        'reserved_4':unicode,    #预留字段1 
        'del':int, #0 存在 1删除
    }
   validators = {
        'name': max_length(50),
        'password': max_length(120),
        'phone': max_length(50),
        'email': max_length(120),
        'qq': max_length(120),
        'wachat': max_length(120),
        'nickname': max_length(120),
        'reserved_1': max_length(120),
        'reserved_2': max_length(120),
        'reserved_3': max_length(120),
        'reserved_4': max_length(120),
    }
   default_values = {
        'del': 0,
        'active':0,
        'superadmin':0,
    }
   use_dot_notation = True



@connection.register
class APP_User(Document):
   __collection__ = 'user'
   __database__ = 'app'
   structure = {
        'name': unicode,
        'password':unicode,
        'phone':unicode,
        'email': unicode,
        'vip'  :unicode,
        'qq':unicode,
        'integral':int,    #用户积分点数之类
        'wachat':unicode,
        'nickname':unicode,
        'appkey':unicode,
        'date':OR(unicode,datetime.datetime),
        'status':int,              #用户状态 1.正常 2.禁用 3.自定义
        'reserved_1':unicode,    #预留字段1 
        'reserved_2':unicode,    #预留字段1 
        'reserved_3':unicode,    #预留字段1 
        'reserved_4':unicode,    #预留字段1 
        'del':int, #0 存在 1删除
    }
   validators = {
        'name': max_length(50),
        'password': max_length(120),
        'phone': max_length(50),
        'email': max_length(120),
        'qq': max_length(120),
        'wachat': max_length(120),
        'nickname': max_length(120),
        'reserved_1': max_length(120),
        'reserved_2': max_length(120),
        'reserved_3': max_length(120),
        'reserved_4': max_length(120),
    }
   default_values = {
        'del': 0,
        'status':1,
        'integral':0,
    }
   use_dot_notation = True

@connection.register
class UserType(Document):
   __collection__ = 'type'
   __database__ = 'app'
   structure = {
        'level': int,
        'level_name':unicode,
        'level_dec':unicode,
        'appkey':unicode,
        'date':OR(unicode,datetime.datetime),
        'reserved_1':unicode,    #预留字段1 
        'reserved_2':unicode,    #预留字段1 
        'reserved_3':unicode,    #预留字段1 
        'reserved_4':unicode,    #预留字段1 
        'del': int,#0 存在 1删除
    }
   validators = {
        'level_name': max_length(50),
        'level_dec': max_length(10000),
        'reserved_1': max_length(10000),
        'reserved_2': max_length(10000),
        'reserved_3': max_length(10000),
        'reserved_4': max_length(10000),
    }
   default_values = {
        'del': 0,
        'date':datetime.datetime.now(),
        'level':1
    }
   use_dot_notation = True
 



@connection.register
class AppInfo(Document):
   __collection__ = 'info'
   __database__ = 'app'
   structure = {
        'appkey':unicode,
        'domian':unicode, #域名
        'status':int,    #0关闭 1开启
        'name':unicode,  #应用名称
        'email':unicode,  #开发者邮箱
        'phone':unicode,  #开发者电话
        'beian':unicode,  #备案号
        'reserved_1':unicode,    #预留字段1 
        'reserved_2':unicode,    #预留字段1 
        'reserved_3':unicode,    #预留字段1 
        'reserved_4':unicode,    #预留字段1 
    }
   validators = {
    }
   default_values = {

    }
   use_dot_notation = True



 
    