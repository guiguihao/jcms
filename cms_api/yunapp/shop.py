#!/usr/bin/python
#-*-coding:utf-8 -*-
from yunapp import app,result,connection
from yunapp.model.shopModel import *
from yunapp.model.typeModel import *
from yunapp.result import *

'''
添加产品
{
    'titile':'xiaosan', #或phone email
    'price':88
    ''
    ''
    ...
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/shop/product/add',methods=['GET', 'POST'])
def product_add():
    if request.method == 'POST':
        data = request.get_json()
        product = connection.Product()
        token = ''
        appkey = ''
        for key in data:
            if key == 'titile':
                product.titile = data['titile']
            if key == 'price':
                product.price = data['price']
            if key == 'sale':
                product.sale = data['sale']
            if key == 'overview':
                product.overview = data['overview']
            if key == 'saleinfo':
                product.saleinfo = data['saleinfo']
            if key == 'type':
                product.type = data['type']
            if key == 'imgs':
                product.imgs = data['imgs']
            if key == 'describe':
                product.describe = data['describe']
            if key == 'token':
                token = data['token']
            if key == 'buycount':
                product.buycount = data['buycount']
            if key == 'evaluate':
                product.evaluate = data['evaluate']
            if key == 'reserved_1':
                product.reserved_1 = data['reserved_1']
            if key == 'reserved_2':
                product.reserved_1 = data['reserved_2']
            if key == 'reserved_3':
                product.reserved_1 = data['reserved_3']
            if key == 'reserved_4':
                product.reserved_1 = data['reserved_4']
        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson() 
        else:
            resultTooken = tool.ruleToken(token)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0] 
        if product.titile and product.price:
            try:
                product.save()
                return  MySucceedResult().toJson()
            except Exception as e:
                return MyException(param.CHECK_FAILURE).toJson()
        else:
           return MyException(param.REGISTER_FAILURE).toJson()
  
    if request.method == 'GET':
        return param.PLEASE_USE_POST
    

'''
删除产品
{
    'del':'pid'
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/shop/product/del',methods=['GET', 'POST'])
def product_del():
    if request.method == 'POST':
        data = request.get_json()
        product = connection.Product()
        token = ''
        appkey = ''
        for key in data:
            if key == 'del':
                product.titile = ObjectId(data['del'])
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
        if product.titile and product.price:
            try:
                connection.product.find_and_modify({'_id':product['_id'],'del':0},{'$set':{"del":1}})
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
       titile : 'xx',
       'price': '' 
    },
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/shop/product/update',methods=['GET', 'POST'])
def product_update():
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
            connection.product.find_and_modify({'_id':data['_id'],'appkey':appkey,'del':0},{'$set':data['set']})
            product = connection.product.find_one({'_id':data['_id'],'appkey':appkey,'del':0},{'del':0})
            ptype = connection.Type.find_one({'_id':product.type,'appkey':appkey,'del':0},{'del':0})
            product['_id'] = str(product['_id'])
            product.type = ptype
            return MyResult(product).toJson()
        except Exception as e:
            return MyException(param.PARAM_FAILURE).toJson()
            
    if request.method == 'GET':
        return param.PLEASE_USE_POST


'''
根据id获取产品 
{
    '_id': 'xxxxxxx',
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/shop/product/get/id',methods=['GET', 'POST'])
def product_get_id():
    if request.method == 'POST':
        data = request.get_json()
        token = ''
        appkey = ''
        _id = ''
        for key in data:
            if key == '_id':
                _id = ObjectId(data['_id'])
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
        if _id == '' or not _id:
            return MyException(param.PARAM_FAILURE).toJson() 
        try:
            plist = [];
            products = connection.product.find({'_id':_id,'appkey':appkey,'del':0},{'del':0})
            for p in products:
                ptype = connection.Type.find_one({'_id':p.type,'appkey':appkey,'del':0},{'del':0})
                p['_id'] = str(p['_id'])
                p.type = ptype
                plist.append(p)
            return MyResult(plist).toJson()
        except Exception as e:
            return MyException(param.PARAM_FAILURE).toJson()
            
    if request.method == 'GET':
        return param.PLEASE_USE_POST

'''
获取type下的产品
{
    'type': 'xxxxxxx',
    'limit'10, 0 ,获取全部
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/shop/product/get/type',methods=['GET', 'POST'])
def product_get_type():
    if request.method == 'POST':
        data = request.get_json()
        token = ''
        appkey = ''
        ptype = ''
        limit = 0
        for key in data:
            if key == 'type':
                ptype = ObjectId(data['type'])
            if key == 'limit':
                limit = data['limit'] if data['limit'] >0 else 0
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
        if ptype == '' or not ptype:
            return MyException(param.PARAM_FAILURE).toJson() 
        try:
            plist = [];
            products = ''
            if limit == 0:
                products = connection.Product.find({'type':ptype,'appkey':appkey,'del':0},{'del':0})
            else:
                products = connection.Product.find({'type':ptype,'appkey':appkey,'del':0},{'del':0}).limit(limit)
            for p in products:
                ptype = connection.Type.find_one({'_id':p.type,'appkey':appkey,'del':0},{'del':0})
                p['_id'] = str(p['_id'])
                p.type = ptype
                plist.append(p)
            return MyResult(plist).toJson()
        except Exception as e:
            return MyException(param.PARAM_FAILURE).toJson()
            
    if request.method == 'GET':
        return param.PLEASE_USE_POST


'''
获取type 推荐下的产品
{
    'type': 'xxxxxxx',
    'recommend': 111  获取推荐值>111的数据
    'limit'10, 0 ,获取全部
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/shop/product/get/type/recommend',methods=['GET', 'POST'])
def product_get_type_recommend():
    if request.method == 'POST':
        data = request.get_json()
        token = ''
        appkey = ''
        ptype = ''
        recommend = ''
        limit = 0
        for key in data:
            if key == 'type':
                ptype = ObjectId(data['type'])
            if key == 'recommend':
                recommend = data['recommend'] 
            if key == 'limit':
                limit = data['limit'] if data['limit'] >0 else 0  
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
        if (ptype == '' or not ptype) and (recommend == '' or not recommend):
            return MyException(param.PARAM_FAILURE).toJson() 
        try:
            plist = [];
            products = ''
            if limit == 0:
                 products = connection.Product.find({'type':ptype,'recommend':{'$gt':recommend},'appkey':appkey,'del':0},{'del':0}).sort({'recommend':-1})
            else:
                 products = connection.Product.find({'type':ptype,'recommend':{'$gt':recommend},'appkey':appkey,'del':0},{'del':0}).sort({'recommend':-1}).limit(limit)
            for p in products:
                ptype = connection.Type.find_one({'_id':p.type,'appkey':appkey,'del':0},{'del':0})
                p['_id'] = str(p['_id'])
                p.type = ptype
                plist.append(p)
            return MyResult(plist).toJson()
        except Exception as e:
            return MyException(param.PARAM_FAILURE).toJson()
            
    if request.method == 'GET':
        return param.PLEASE_USE_POST








