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
class Product(Document):
   __collection__ = 'product'
   __database__ = 'shop'
   structure = {
        'title': unicode,      #标题
        'price':OR(float,int),          #销售价
        'costprice': OR(float,int),      # 成本价 用于计算分销提成
        'overview': unicode,    #简介\概述
        'type':unicode,         #类型
        'colour': list,  # 颜色 大小
        'size': list,  # 大小
        'repertory':int,  # 库存
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
class Sale(Document):
   __collection__ = 'sale'
   __database__ = 'shop'
   structure = {
        'title': unicode,      #标题
        'describe':unicode,     #描述
        'startdate':unicode,
        'enddate': unicode,
        'appkey': unicode,
        'status': int,
        'products':[],           #参与活动的产品
        'reserved_1':unicode,    #预留字段1
        'reserved_2':unicode,    #预留字段1
        'reserved_3':unicode,    #预留字段1
        'reserved_4':unicode,    #预留字段1
        'del': int,#0 存在 1删除
    }
   validators = {
        'title': max_length(200),
        'describe': max_length(200),
        'startdate': max_length(200),
        'enddate': max_length(200),
    }
   default_values = {
       'del': 0,
       'status':-1,
    }
   use_dot_notation = True
 
@connection.register
class Order(Document):
   __collection__ = 'order'
   __database__ = 'shop'
   structure = {
        'user':unicode,           #订单客户
        'price': OR(float,int),         #订单实付价格
        'product': [{                #订单产品
            'title':unicode,        #产品名称
            'imgs':[],              #产品图片
            'price': OR(float,int),  # 产品单价
            'saleprice': OR(float, int),  # 产品促销价
            'colour': unicode,  # 颜色 大小
            'size': unicode,  # 大小
            'count':int,     #购买数量
        }],
        'date': OR(unicode, datetime.datetime),
        'receiveinfo':{
            'name':unicode,
            'phone':unicode,
            'address':unicode,
            'code':unicode,   #邮编
            'remake': unicode,  # 备注
        },      #收货信息
        'status':IS(0,1,2,3,4),               #0 待付款 1已付款 2,已发货  3.交易完成 4关闭交易
        'refund': {                #退款信息
            'status': IS(0,1,2,3,4,5),         # 退款状态 0 无退款 1申请退款  2同意退款 3拒绝退款 4退款完成,5关闭退款
            'remake':unicode,      #退款备注
            'price': OR(float, int), #退款金额
            'products': list,  # 退款产品
            'express':{            #快递信息
                'name':unicode,    #快递名称
                'code': unicode,  # 快递单号
            },
        },
        'express':{        #物流信息
            'name': unicode,  # 快递名称
            'code': unicode,  # 快递单号
        },
        'remake': unicode,  # 备注
        'appkey':unicode,
        'reserved_1':unicode,    #预留字段1 
        'reserved_2':unicode,    #预留字段1 
        'reserved_3':unicode,    #预留字段1 
        'reserved_4':unicode,    #预留字段1 
        'del': int,#0 存在 1删除
    }
   validators = {
       'user': max_length(200),
       'refund.remake': max_length(200),
       'refund.express.name': max_length(200),
       'refund.express.code': max_length(200),
       'remake': max_length(200),
       'express.code': max_length(200),
       'express.name': max_length(200),
    }
   default_values = {
        'del': 0,
        'date': datetime.datetime.now(),
        'status':0,
        'refund.status':0,
    }
   required = ['user','price','receiveinfo','status']
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