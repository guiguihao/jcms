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
获取收藏/购物车列表
{
    'pageSize': 10,
    'page':1
    filter = ''
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/app/productCollection/list', methods=['GET', 'POST'])
def get_products_collection():
    if request.method == 'POST':
        appkey = ''
        token = ''
        try:
            token = request.headers[config.AUTHORIZATION]
        except:
            return MyException(param.APP_TOKEN_NULL).toJson()
        data = request.get_json()
        user = connection.Collection()
        pageSize = 50
        page = 1
        filter = ''
        for key in data:
            if key == 'pageSize':
                pageSize = data['pageSize']
            if key == 'page':
                page = data['page']
            if key == 'filter':
                filter = data['filter']
        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson()
        else:
            resultTooken = tool.ruleToken(token,True)
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
                fnuser = connection.Collection.find(params,{'del':0}).sort([('_id', -1)])
                fdApp = connection.AppInfo.find_one({'appkey': appkey})
                for user in fnuser:
                    user['_id'] = str(user['_id'])
                    if user.userId:
                        fnuser1 = connection.APP_admin.find_one(
                            {'appkey': appkey, '_id': ObjectId(user.userId), 'del': 0})
                        if fnuser1:
                            fnuser1['_id'] = str(fnuser1['_id'])
                            user['user'] = fnuser1
                        fnuser2 = connection.APP_User.find_one(
                            {'appkey': appkey, '_id': ObjectId(user.userId), 'del': 0})
                        if fnuser2:
                            fnuser2['_id'] = str(fnuser2['_id'])
                            user['user'] = fnuser2
                    if user.productId:
                        product = connection.Product.find_one(
                            {'appkey': appkey, '_id': ObjectId(user.productId), 'del': 0})
                        if product:
                            product['_id'] = str(product['_id'])
                            product['oimgs'] = []
                            product['lstimgs'] = []  # 略缩图
                            for i in range(0, len(product['imgs'])):
                                product['oimgs'].append(fdApp.reserved_1 + '/upload/' +product['imgs'][i])
                                product['lstimgs'].append(
                                    fdApp.reserved_1 + '/upload/' + 'lsu/' + product['imgs'][i].split('/')[1])
                            user['product'] = product
                    user.date = user.date.strftime('%Y-%m-%d %H:%M:%S')
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
添加收藏/购物车
{
    'userId':
    'productsId':''
}
'''


@app.route('/app/productCollection/add', methods=['GET', 'POST'])
def add_product_collection():
    if request.method == 'POST':
        appkey = ''
        token = ''
        try:
            token = request.headers['Authorization']
        except:
            return MyException(param.APP_TOKEN_NULL).toJson()
        data = request.get_json()
        user = connection.Collection()
        for key in data:
            if data[key] == '':
                continue
            if key == 'userId':
                user.userId = data['userId']
            if key == 'type':
                user.type = data['type']
            if key == 'productId':
                user.productId = data['productId']
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
            resultTooken = tool.ruleToken(token, True)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0]
        if user.userId and user.productId:
            try:
                try:
                    if user.userId:
                        fnuser1 = connection.APP_admin.find_one(
                            {'appkey': appkey, '_id': ObjectId(user.userId), 'del': 0})
                        fnuser2 = connection.APP_User.find_one(
                            {'appkey': appkey, '_id': ObjectId(user.userId), 'del': 0})
                        if not fnuser1 and not fnuser2:
                            return MyException(param.APP_USER_NULL).toJson()
                    if user.productId:
                        c = connection.Collection.find_one(
                            {'appkey': appkey, 'productId': user.productId,'type': user.type, 'del': 0})
                        if c:
                            return MySucceedResult().toJson()
                except Exception, e:
                    return MyException(param.CHECK_FAILURE).toJson()
                user.appkey = appkey
                user.date = datetime.now()
                user.save()
                return MySucceedResult().toJson()
            except Exception as e:
                print  e
                return MyException(param.CHECK_FAILURE).toJson()
        else:
            return MyException(param.ARTICLE_COLLECTION__FAILURE).toJson()

    if request.method == 'GET':
        return param.PLEASE_USE_POST


'''
post  更新收藏/购物车信息
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


@app.route('/app/productCollection/update', methods=['GET', 'POST'])
def app_product_collection_update():
    if request.method == 'POST':
        appkey = ''
        token = ''
        try:
            token = request.headers[config.AUTHORIZATION]
        except:
            return MyException(param.APP_TOKEN_NULL).toJson()
        data = request.get_json()
        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson()
        else:
            resultTooken = tool.ruleToken(token,True)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0]
        try:
            user = connection.Collection.find_one({'appkey': appkey, '_id': ObjectId(data['_id'])})
            if user:
                user['del'] = int(user['del'])
                for key in data['set']:
                    if data['set'][key] == '':
                        continue
                    if key == 'productId':
                        user.productId = data['set']['productId']
                    if key == 'reserved_1':
                        user.reserved_1 = data['set']['reserved_1']
                    if key == 'reserved_2':
                        user.reserved_2 = data['set']['reserved_2']
                    if key == 'reserved_3':
                        user.reserved_3 = data['set']['reserved_3']
                    if key == 'reserved_4':
                        user.reserved_4 = data['set']['reserved_4']
                    if key == 'del':
                        user['del'] = data['set']['del']
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








