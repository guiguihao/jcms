#!/usr/bin/python
#-*-coding:utf-8 -*-
from yunapp import connection,Document
import datetime
from mongokit import OR



def max_length(length):
    def validate(value):
        if len(value) <= length:
            return True
        raise Exception('%s must be at most %s characters long' % length)
    return validate


@connection.register
class Product(Document):
   __collection__ = 'product'
   __database__ = 'shop'
   structure = {
        'title': unicode,      #标题
        'price':OR(float,int),          #销售价
        'costprice': OR(float,int),      # 成本价 用于计算分销提成
        'overview': unicode,    #简介\概述
        'type':unicode,         #类型
        'imgs':list,            #主图list 地址
        'describe':unicode,     #描述
        'describe_html': unicode,  # 描述html
        'recommend':unicode,        #推荐
        'buycount':int,         #购买数量
        'collectcount':int,     #收藏数量
        'appkey':unicode,
        'author':unicode,         #所有者 上传者
        'date': OR(unicode, datetime.datetime),
        'status':int, #0未审核 1,审核,2,未上架 3上架
        'reserved_1':unicode,    #预留字段1 
        'reserved_2':unicode,    #预留字段1 
        'reserved_3':unicode,    #预留字段1 
        'reserved_4':unicode,    #预留字段1 
        'del': int,#0 存在 1删除
    }
   validators = {
        'title': max_length(200),
        'overview': max_length(200),
        'type': max_length(200),
        'author': max_length(200),
        'describe': max_length(20000),
    }
   default_values = {
       'status':0,
       'del': 0,
       'date': datetime.datetime.now(),
       'buycount': 0,
       'collectcount': 0,
       'price':0,
       'costprice':0,
    }
   use_dot_notation = True
 
@connection.register
class Order(Document):
   __collection__ = 'orde'
   __database__ = 'shop'
   structure = {
        'time':unicode,           #订单时间
        'user':unicode,           #订单客户
        'price': unicode,         #订单实付价格
        'product': unicode,       #订单产品
        'colour':unicode,          #颜色 大小 
        'receiveinfo':unicode,      #收货信息
        'status':int,               #0 待付款 1已付款 2待发货 3已发货 4已收货 5申请退款中 6退款确认中.. 7同意退款,等待退货完成 8完成退款
        'appkey':unicode,
        'reserved_1':unicode,    #预留字段1 
        'reserved_2':unicode,    #预留字段1 
        'reserved_3':unicode,    #预留字段1 
        'reserved_4':unicode,    #预留字段1 
        'del': int,#0 存在 1删除
    }
   validators = {
        'time': max_length(200),
        'product': max_length(200),
        'receiveinfo': max_length(200),
    }
   default_values = {
        'del': 0,
    }
   required = ['time','user','price','product','receiveinfo','status']
   use_dot_notation = True


@connection.register
class Receiveinfo(Document):
   __collection__ = 'receive'
   __database__ = 'shop'
   structure = {
        'userid': unicode,         #用户
        'mphone':unicode,          #手机号码
        'phone':unicode,           #电话
        'area':unicode,            #区域 省市区
        'address': unicode,        #详细地址
        'sort':int,                #排序
        'del': int,#0 存在 1删除
    }
   validators = {
        'userid': max_length(200),
        'mphone': max_length(200),
        'phone': max_length(200),
        'area': max_length(200),
        'address': max_length(200),
    }
   default_values = {
        'del': 0,
    }
   required = ['time','user','price','product','receiveinfo','status']
   use_dot_notation = True

#退货信息
@connection.register
class ReturnGoodsinfo(Document):
   __collection__ = 'returnGoods'
   __database__ = 'shop'
   structure = {
        'appkey': unicode,         #appkey
        'phone':unicode,          #手机号码
        'telephone':unicode,           #电话
        'address': unicode,        #详细地址
        'receiver':unicode,        #收件人
        'code':unicode,             #邮编
        'mark': unicode,           # 备注
    }
   validators = {
        'receiver': max_length(200),
        'code': max_length(200),
        'telephone': max_length(200),
        'phone': max_length(200),
        'address': max_length(200),
        'mark': max_length(10000),
    }
   default_values = {
    }
   required = ['appkey']
   use_dot_notation = True