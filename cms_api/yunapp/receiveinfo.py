#!/usr/bin/python
#-*-coding:utf-8 -*-
from yunapp import app,result,connection,request,tool,config,sms
from yunapp.model.shopModel import *
from yunapp.result import *
from yunapp import param
from bson.objectid import ObjectId
from datetime import datetime



'''
添加收货地址
{
    'set':{
      userid:''
      mphone:''
      phone:''
      area:''
      address:''
      sort:''
    }
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/shop/Receiveinfo/add',methods=['GET', 'POST'])
def Receiveinfo_add():
    if request.method == 'POST':
        data = request.get_json()
        receiveinfo = connection.Receiveinfo()
        token = ''
        appkey = ''
        for key in data:
            if key == 'token':
                token = data['token']
        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson() 
        else:
            resultTooken = tool.ruleToken(token)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0] 
        try:
            receiveinfo.save()
            return  MySucceedResult().toJson()
        except Exception as e:
            return MyException(param.CHECK_FAILURE).toJson()
  
    if request.method == 'GET':
        return param.PLEASE_USE_POST
    

'''
删除收货地址
{
    'del':'id'
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/shop/Receiveinfo/del',methods=['GET', 'POST'])
def Receiveinfo_del():
    if request.method == 'POST':
        data = request.get_json()
        receiveinfo = connection.Receiveinfo()
        token = ''
        appkey = ''
        order = ''
        for key in data:
            if key == 'del':
                pass
                # order.titile = ObjectId data['del']
            if key == 'token':
                token = data['token']
        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson() 
        else:
            resultTooken = tool.ruleToken(token)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0] 
        if order.titile and order.price:
            try:
                connection.Receiveinfo.find_and_modify({'_id':order['_id'],'del':0},{'$set':{"del":1}})
                return  MySucceedResult().toJson()
            except Exception as e:
                return MyException(param.CHECK_FAILURE).toJson()
        else:
           return MyException(param.REGISTER_FAILURE).toJson()
  
    if request.method == 'GET':
        return param.PLEASE_USE_POST




'''
post 
{
    '_id': 'xxxxxxx',
    set:{
       设置需要更新的字段即可,如下,可多个字段,不能包含_id
        time:''
      user:''
      price:''
      product:''
      colour:''
      receiveinfo:''
    },
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/shop/Receiveinfo/update',methods=['GET', 'POST'])
def receiveinfo_update():
    if request.method == 'POST':
        data = request.get_json()
        token = ''
        appkey = ''
        for key in data:
            if key == '_id':
                data['_id'] = ObjectId(data['_id'])
            if key == 'token':
                token = data['token']
        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson() 
        else:
            resultTooken = tool.ruleToken(token)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0]
        try:
            connection.Receiveinfo.find_and_modify({'_id':data['_id'],'appkey':appkey,'del':0},{'$set':data['set']})
            order = connection.Receiveinfo.find_one({'_id':data['_id'],'appkey':appkey,'del':0},{'del':0})
            #ptype = connection.Type.find_one({'_id':product.type,'appkey':appkey,'del':0},{'del':0})
            order['_id'] = str(order['_id'])
            #product.type = ptype
            return MyResult(order).toJson()
        except Exception as e:
            return MyException(param.PARAM_FAILURE).toJson()
            
    if request.method == 'GET':
        return param.PLEASE_USE_POST

'''
post 
{
    根据id获取收货地址
    '_id': 'xxxxxxx'
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/shop/Receiveinfo/get/id',methods=['GET', 'POST'])
def receiveinfo_get_id():
    if request.method == 'POST':
        data = request.get_json()
        token = ''
        appkey = ''
        for key in data:
            if key == '_id':
                data['_id'] = ObjectId(data['_id'])
            if key == 'token':
                token = data['token']
        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson() 
        else:
            resultTooken = tool.ruleToken(token)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0]
        try:
            #connection.Order.find_and_modify({'_id':data['_id'],'appkey':appkey,'del':0},{'$set':data['set']})
            order = connection.Receiveinfo.find_one({'_id':data['_id'],'appkey':appkey,'del':0},{'del':0})
            #ptype = connection.Type.find_one({'_id':product.type,'appkey':appkey,'del':0},{'del':0})
            order['_id'] = str(order['_id'])
            #product.type = ptype
            return MyResult(order).toJson()
        except Exception as e:
            return MyException(param.PARAM_FAILURE).toJson()
            
    if request.method == 'GET':
        return param.PLEASE_USE_POST

'''
post 
{
    获取用户收货地址
    'get':{
       user:
       status:
    }
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/shop/order/get/user',methods=['GET', 'POST'])
def order_get_user():
    if request.method == 'POST':
        data = request.get_json()
        token = ''
        appkey = ''
        query = {}
        for key in data:
            if key == '_id':
                data['_id'] = ObjectId(data['_id'])
            if key == 'token':
                token = data['token']
            if key == 'get':
                query = data['get']
        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson() 
        else:
            resultTooken = tool.ruleToken(token)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0]
                query['appkey'] = appkey
                query['del'] = 0
        try:
            #connection.Order.find_and_modify({'_id':data['_id'],'appkey':appkey,'del':0},{'$set':data['set']})
            orders = connection.Receiveinfo.find(query,{'del':0})
            olist = []
            for o in orders:
            	o['_id'] = str(o['_id'])
                olist.append(o)
            #product.type = ptype
            return MyResult(olist).toJson()
        except Exception as e:
            return MyException(param.PARAM_FAILURE).toJson()
            
    if request.method == 'GET':
        return param.PLEASE_USE_POST