#!/usr/bin/python
#-*-coding:utf-8 -*-
from yunapp import app,result,connection,request,tool,config,sms
from yunapp.model.shopModel import *
from yunapp.result import *
from yunapp import param
from bson.objectid import ObjectId
from datetime import datetime
import time

'''
获取优惠码列表
{
    'pageSize': 10,
    'page':1
    filter = ''
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''

@app.route('/app/productSaleCode/list', methods=['GET', 'POST'])
def get_products_sale_code():
    if request.method == 'POST':
        data = request.get_json()
        user = connection.saleCode()
        appkey = ''
        pageSize = 50
        page = 1
        filter = ''
        for key in data:
            if key == 'token':
                token = data['token']
            if key == 'pageSize':
                pageSize = data['pageSize']
            if key == 'page':
                page = data['page']
            if key == 'filter':
                filter = data['filter']
        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson()
        else:
            resultTooken = tool.ruleToken(token)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0]

        if appkey:
            try:
                admins = {
                    'count': 0,
                    'data': [],
                }
                params = {
                    'appkey': appkey,
                    'del': 0,
                }
                if isinstance(filter, dict):
                    for k in filter:
                            params[k] = filter[k]
                            if k == '_id':
                                params[k] = ObjectId(filter[k])
                fnuser = connection.saleCode.find(params,{'del':0}).limit(pageSize).skip((page - 1) * pageSize).sort(
                    [('_id', -1)])
                for user in fnuser:
                    user['_id'] = str(user['_id'])
                    try:
                        t = time.time()
                        if t >= tool.utc_to_local(user.validdate):
                            user['status'] = 0
                        else:
                            user['status'] = 1
                        user.validdate = tool.utc_to_localtime(user.validdate)
                    except Exception as e:
                        pass
                    admins['data'].append(user)
                admins['count'] = fnuser.count()
                return MyResult(admins).toJson()
            except Exception as e:
                print e
                return MyException(param.CHECK_FAILURE).toJson()
        else:
            return MyException(param.REGISTER_FAILURE).toJson()

    if request.method == 'GET':
        return param.PLEASE_USE_POST


'''
添加优惠码
{
    'name':'xiaosan', #或phone email
    'password':'11122',
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''


@app.route('/app/productSaleCode/add', methods=['GET', 'POST'])
def add_product_saleCode():
    if request.method == 'POST':
        data = request.get_json()
        user = connection.saleCode()
        appkey = ''
        token = ''
        for key in data:
            if data[key] == '':
                continue
            if key == 'salerange':
                user.salerange = data['salerange']
            if key == 'saleprice':
                user.saleprice = data['saleprice']
            if key == 'count':
                user.count = data['count']
            if key == 'usedcount':
                user.usedcount = data['usedcount']
            if key == 'products':
                user.products = data['products']
            if key == 'validdate':
                user.validdate = data['validdate']
            if key == 'token':
                token = data['token']
            if key == 'reserved_1':
                user.reserved_1 = data['reserved_1']
            if key == 'reserved_2':
                user.reserved_2 = data['reserved_2']
            if key == 'reserved_3':
                user.reserved_3 = data['reserved_3']
            if key == 'reserved_4':
                user.reserved_4 = data['reserved_4']

        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson()
        else:
            resultTooken = tool.ruleToken(token)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0]
        if (user.salerange or user.saleprice) and user.count>0 and user.validdate:
            try:
                code = tool.randomString(2)
                user.appkey = appkey
                user.code =unicode(code.upper())
                user.save()
                return MySucceedResult().toJson()
            except Exception as e:
                print  e
                return MyException(param.CHECK_FAILURE).toJson()
        else:
            return MyException(param.ARTICLE_MUST_TITLE_FAILURE).toJson()

    if request.method == 'GET':
        return param.PLEASE_USE_POST


'''
post  更新优惠码信息
{
    '_id':'xxx'
    set:{
       设置需要更新的字段即可,如下,可多个字段,不能包含_id
       name : 'xx',
       'vip': 'vip类型_id', #通过获取所有vip类型可以获取_id  /user/vip/type/get 
    },
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''


@app.route('/app/productSaleCode/update', methods=['GET', 'POST'])
def app_product_saleCode_update():
    if request.method == 'POST':
        data = request.get_json()
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
            user = connection.saleCode.find_one({'appkey': appkey, '_id': ObjectId(data['_id'])})
            if user:
                user['del'] = int(user['del'])
                for key in data['set']:
                    if data['set'][key] == '':
                        continue
                    if key == 'del':
                        user['del'] = data['set']['del']
                    if key == 'products':
                        user.products = data['set']['products']
                user.save()
                user['_id'] = str(user['_id'])
                # user.date = user.date.strftime('%Y-%m-%d %H:%M:%S')
                return MyResult(user).toJson()
            else:
                return MyException(param.PRODUCT_NULL).toJson()
        except Exception as e:
            print e
            return MyException(param.PARAM_FAILURE).toJson()

    if request.method == 'GET':
        return param.PLEASE_USE_POST


'''
post  添加优惠产品
{
    '_id':'xxx'
    products:[{
      
    }],
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/app/productSaleCode/products/add', methods=['GET', 'POST'])
def app_product_saleCode_product_add():
    if request.method == 'POST':
        data = request.get_json()
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
            user = connection.saleCode.find_one({'appkey': appkey, '_id': ObjectId(data['_id'])})
            if user:
                user['del'] = int(user['del'])
                for code in data['products']:
                    _id = code['_id']
                    col = connection.saleCode.find({'products._id':_id})
                    if col.count()>0:
                        return MyException(param.PRODUCT_RE_FAILURE).toJson()
                    user.products.append(code)
                user.save()
                user['_id'] = str(user['_id'])
                # user.date = user.date.strftime('%Y-%m-%d %H:%M:%S')
                return MyResult(user).toJson()
            else:
                return MyException(param.PRODUCT_NULL).toJson()
        except Exception as e:
            print e
            return MyException(param.PARAM_FAILURE).toJson()

    if request.method == 'GET':
        return param.PLEASE_USE_POST


'''
post  删除优惠产品
{
    '_id':'xxx'
    productId:,
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''


@app.route('/app/productSaleCode/products/del', methods=['GET', 'POST'])
def app_product_saleCode_product_del():
    if request.method == 'POST':
        data = request.get_json()
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
            user = connection.saleCode.find_one({'appkey': appkey, '_id': ObjectId(data['_id'])})
            if user:
                productId = data['productId']
                for p in user.products:
                    if p['_id'] ==  productId:
                        user['products'].remove(p)
                user.save()
                user['_id'] = str(user['_id'])
                # user.date = user.date.strftime('%Y-%m-%d %H:%M:%S')
                return MyResult(user).toJson()
            else:
                return MyException(param.PRODUCT_NULL).toJson()
        except Exception as e:
            print e
            return MyException(param.PARAM_FAILURE).toJson()

    if request.method == 'GET':
        return param.PLEASE_USE_POST



