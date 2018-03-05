#!/usr/bin/python
#-*-coding:utf-8 -*-
from yunapp import app,result,connection



'''
添加订单
{
    'set':{
      time:''
      user:''
      price:''
      product:''
      colour:''
      receiveinfo:''
    }
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/shop/order/add',methods=['GET', 'POST'])
def order_add():
    if request.method == 'POST':
        data = request.get_json()
        order = connection.Order()
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
            order.save()
            return  MySucceedResult().toJson()
        except Exception as e:
            return MyException(param.CHECK_FAILURE).toJson()
  
    if request.method == 'GET':
        return param.PLEASE_USE_POST
    

'''
删除订单
{
    'del':'id'
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/shop/order/del',methods=['GET', 'POST'])
def order_del():
    if request.method == 'POST':
        data = request.get_json()
        order = connection.Order()
        token = ''
        appkey = ''
        for key in data:
            if key == 'del':
                order.titile = ObjectId(data['del'])
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
            connection.Order.find_and_modify({'_id':order['_id'],'del':0},{'$set':{"del":1}})
            return  MySucceedResult().toJson()
        except Exception as e:
            return MyException(param.CHECK_FAILURE).toJson()
  
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
@app.route('/shop/order/update',methods=['GET', 'POST'])
def order_update():
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
            connection.Order.find_and_modify({'_id':data['_id'],'appkey':appkey,'del':0},{'$set':data['set']})
            order = connection.Order.find_one({'_id':data['_id'],'appkey':appkey,'del':0},{'del':0})
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
    根据id获取订单
    '_id': 'xxxxxxx'
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/shop/order/get/id',methods=['GET', 'POST'])
def order_get_id():
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
            order = connection.Order.find_one({'_id':data['_id'],'appkey':appkey,'del':0},{'del':0})
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
    获取用户订单
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
            orders = connection.Order.find(query,{'del':0})
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