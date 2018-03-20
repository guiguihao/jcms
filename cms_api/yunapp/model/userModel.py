#!/usr/bin/python
#-*-coding:utf-8 -*-
from yunapp import connection,Document



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
class UserVip(Document):
   __collection__ = 'vip'
   __database__ = 'user'
   structure = {
        'level': int,
        'level_name':unicode,
        'level_dec':unicode,
        'appkey':unicode,
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
    }
   use_dot_notation = True
 



@connection.register
class App(Document):
   __collection__ = 'col'
   __database__ = 'app'
   structure = {
        'userid': unicode,
        'appkey':unicode,
        'appsecret':unicode,
        'appicon':unicode,    
        'appname':unicode,
        'del':int,  #0 存在 1删除
    }
   validators = {
        'userid': max_length(200),
        'appkey': max_length(200),
        'appsecret': max_length(200),
        'appicon': max_length(200),
        'appname': max_length(200),
    }
   default_values = {
        'del': 0,
    }
   use_dot_notation = True



@connection.register
class DeveloperUser(Document):
   __collection__ = 'DeveloperUser'
   __database__ = 'user'
   structure = {
        'name': unicode,
        'password':unicode,
        'phone':unicode,
        'email': unicode,
        'vip': unicode,
    }
   validators = {
        'name': max_length(50),
        'password': max_length(120),
        'phone': max_length(50),
        'email': max_length(120),
    }
   required = ['password']
   use_dot_notation = True


 
    