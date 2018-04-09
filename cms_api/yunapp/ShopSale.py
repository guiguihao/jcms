#!/usr/bin/python
#-*-coding:utf-8 -*-
from yunapp import app,result,connection,request,tool,config,sms
from yunapp.model.shopModel import *
from yunapp.result import *
from yunapp import param
from bson.objectid import ObjectId
from datetime import datetime


'''
获取活动列表
{
    'pageSize': 10,
    'page':1
    filter = ''
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''

def getSubTypes(appkey,parentId,types):
     types.append(parentId)
     ftype = connection.Type.find({'appkey': appkey, 'del': 0, 'parentID': parentId}, {'del': 0})
     for mtype in ftype:
         mtypeid = str(mtype['_id'])
         getSubTypes(appkey,mtypeid,types)


@app.route('/app/productSale/list', methods=['GET', 'POST'])
def get_products_sale():
    if request.method == 'POST':
        data = request.get_json()
        user = connection.Sale()
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
                typeid = ''
                types = []
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
                fnuser = connection.Sale.find(params,{'del':0})
                for user in fnuser:
                    user['_id'] = str(user['_id'])
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
添加活动
{
    'name':'xiaosan', #或phone email
    'password':'11122',
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''


@app.route('/app/productSale/add', methods=['GET', 'POST'])
def add_product_sale():
    if request.method == 'POST':
        data = request.get_json()
        user = connection.Sale()
        appkey = ''
        token = ''
        for key in data:
            if data[key] == '':
                continue
            if key == 'title':
                user.title = data['title']
            if key == 'describe':
                user.describe = data['describe']
            if key == 'startdate':
                user.startdate = data['startdate']
            if key == 'enddate':
                user.enddate = data['enddate']
            if key == 'products':
                user.products = data['products']
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
        if user.title:
            try:
                user.appkey = appkey
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
post  更新用户信息
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


@app.route('/app/productSale/update', methods=['GET', 'POST'])
def app_product_sale_update():
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
            user = connection.Product.find_one({'appkey': appkey, '_id': ObjectId(data['_id'])})
            if user:
                user['del'] = int(user['del'])
                for key in data['set']:
                    if data['set'][key] == '':
                        continue
                    if key == 'title':
                        user.title = data['set']['title']
                    if key == 'describe':
                        user.describe = data['set']['describe']
                    if key == 'startdate':
                        user.startdate = data['set']['startdate']
                    if key == 'enddate':
                        user.enddate = data['set']['enddate']
                    if key == 'products':
                        user.products = data['set']['products']
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








