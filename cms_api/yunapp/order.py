#!/usr/bin/python
# -*-coding:utf-8 -*-
from yunapp import app, result, connection, request, tool, config, sms
from yunapp.model.shopModel import *
from yunapp.model.userModel import *
from yunapp.result import *
from yunapp import param
from bson.objectid import ObjectId
from datetime import datetime

'''
获取订单列表
{
    'pageSize': 10,
    'page':1
    filter = ''
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''


@app.route('/app/order/list', methods=['GET', 'POST'])
def get_orders():
    if request.method == 'POST':
        appkey = ''
        token = ''
        try:
            token = request.headers[config.AUTHORIZATION]
        except:
            return MyException(param.APP_TOKEN_NULL).toJson()
        data = request.get_json()
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
                            try:
                               params[k] = ObjectId(filter[k])
                            except Exception as e:
                                params[k] =  ObjectId('5ad4acd21fe63712a04a1111')
                fnuser = connection.Order.find(params, {'del': 0}).limit(pageSize).skip((page - 1) * pageSize).sort(
                    [('_id', -1)])
                fdApp = connection.AppInfo.find_one({'appkey': appkey})
                for user in fnuser:
                    user['_id'] = str(user['_id'])
                    for p in user.product:
                        p['oimgs'] = []
                        for i in range(0, len(p['imgs'])):
                            p['oimgs'].append(fdApp.reserved_1 + '/upload/' + p['imgs'][i])
                    user.date = user.date.strftime('%Y-%m-%d %H:%M:%S')
                    author1 = connection.APP_User.one({'appkey': appkey, '_id': ObjectId(user.user)}, {'del': 0,'password':0})
                    if author1:
                        author1['_id'] = str(author1['_id'])
                        user.user = author1
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
添加订单
{
    'name':'xiaosan', #或phone email
    'password':'11122',
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''


@app.route('/app/order/add', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        appkey = ''
        token = ''
        try:
            token = request.headers[config.AUTHORIZATION]
        except:
            return MyException(param.APP_TOKEN_NULL).toJson()
        data = request.get_json()
        user = connection.Order()
        for key in data:
            if data[key] == '':
                continue
            if key == 'user':
                user.user = data['user']
            if key == 'price':
                user.price = data['price']
            if key == 'product':
                for product in data['product']:
                    newProduct = {
                        'imgs':[],
                    }
                    for subkey in product:
                        if subkey == '_id':
                            newProduct['_id'] = product['_id']
                        if subkey == 'costprice':
                            newProduct['costprice'] = product['costprice']
                        if subkey == 'title':
                            newProduct['title'] = product['title']
                        if subkey == 'imgs':
                            newProduct['imgs'] = product['imgs']
                        if subkey == 'price':
                            newProduct['price'] = product['price']
                        if subkey == 'saleprice':
                            newProduct['saleprice'] = product['saleprice']
                        if subkey == 'saleCode':
                            newProduct['saleCode'] = product['saleCode']
                        if subkey == 'colour':
                            newProduct['colour'] = product['colour']
                        if subkey == 'size':
                            newProduct['size'] = product['size']
                        if subkey == 'count':
                            newProduct['count'] = product['count']
                    if(len(newProduct)>0):
                        user.product.append(newProduct)
            if key == 'receiveinfo':
                for subkey in data['receiveinfo']:
                    if subkey == 'name':
                        user.receiveinfo.name = data['receiveinfo']['name']
                    if subkey == 'phone':
                        user.receiveinfo.phone = data['receiveinfo']['phone']
                    if subkey == 'address':
                        user.receiveinfo.address = data['receiveinfo']['address']
                    if subkey == 'code':
                        user.receiveinfo.code = data['receiveinfo']['code']
                    if subkey == 'remake':
                        user.receiveinfo.remake = data['receiveinfo']['remake']
            if key == 'express':
                for subkey in data['express']:
                    if subkey == 'name':
                        user.express['name'] = data['express']['name']
                    if subkey == 'code':
                        user.express['code'] = data['express']['code']
            if key == 'status':
                user.status = data['status']
            if key == 'remake':
                user.remake = data['remake']
            if key == 'reserved_1':
                user.reserved_1 = data['reserved_1']
            if key == 'reserved_2':
                user.reserved_1 = data['reserved_2']
            if key == 'reserved_3':
                user.reserved_1 = data['reserved_3']
            if key == 'reserved_4':
                user.reserved_1 = data['reserved_4']

        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson()
        else:
            resultTooken = tool.ruleToken(token,True)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0]
        if user.user and user.price and user.product and user.receiveinfo:
            try:
                try:
                       fnuser2 = connection.APP_User.find_one({'appkey': appkey, '_id': ObjectId(user.user), 'del': 0})
                       if not fnuser2:
                             return MyException(param.ORDER_USERID_ERROR).toJson()
                except Exception, e:
                    return MyException([param.PARAM_FAILURE[0],unicode(e)]).toJson()
                user.appkey = appkey
                user.date = datetime.now()
                user.save()
                user['_id'] = str(user['_id'])
                return MyResult(user).toJson()
            except Exception as e:
                print  e
                return MyException([param.CHECK_FAILURE[0],unicode(e)]).toJson()
        else:
            return MyException(param.PARAM_FAILURE).toJson()

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


@app.route('/app/order/update', methods=['GET', 'POST'])
def app_order_update():
    if request.method == 'POST':
        appkey = ''
        token = ''
        try:
            token = request.headers[config.AUTHORIZATION]
        except:
            return MyException(param.APP_TOKEN_NULL).toJson()
        data = request.get_json()
        fxIndex = 0
        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson()
        else:
            resultTooken = tool.ruleToken(token,True)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0]
        try:
            user = connection.Order.find_one({'appkey': appkey, '_id': ObjectId(data['_id'])})
            if user:
                user['del'] = int(user['del'])
                for key in data['set']:
                    if data['set'][key] == '':
                        continue
                    if key == 'price':
                        if (user.status>1):
                            return MyException(param.ORDER_PRICE_ERROR).toJson()
                        user.price = data['set']['price']
                    if key == 'receiveinfo':
                        if (user.status>2):
                            return MyException(param.ORDER_ADDRESS_ERROR).toJson()
                        user.receiveinfo = data['set']['receiveinfo']
                        for subkey in data['set']['receiveinfo']:
                            if data['set']['receiveinfo'][subkey] == '' and data['set']['receiveinfo'][subkey] == None:
                                continue
                            if subkey == 'name':
                                user.receiveinfo['name'] = data['set']['receiveinfo']['name']
                            if subkey == 'phone':
                                user.receiveinfo['phone'] = data['set']['receiveinfo']['phone']
                            if subkey == 'address':
                                user.receiveinfo['address'] = data['set']['receiveinfo']['address']
                            if subkey == 'code':
                                user.receiveinfo['code'] = data['set']['receiveinfo']['code']
                            if subkey == 'remake':
                                user.receiveinfo['remake'] = data['set']['receiveinfo']['remake']
                    if key == 'status':
                        user.status = data['set']['status']
                        if user.status == 3:
                            fxIndex = 1
                    if key == 'express':
                        for subkey in data['set']['express']:
                             if subkey == 'name':
                                 user.express['name'] = data['set']['express']['name']
                             if subkey == 'code':
                                 user.express['code'] = data['set']['express']['code']
                    if key == 'remake':
                        user.remake = data['set']['remake']
                    if key == 'refund':
                        for subkey in data['set']['refund']:
                            if data['set']['refund'][subkey] == '' and data['set']['refund'][subkey] == None:
                                continue
                            if subkey == 'status':
                                if (user.status == 0 and user.status == 4 and data['set']['refund']['status']==1):
                                     return MyException(param.ORDER_REFUND_PRICE_ERROR).toJson()
                                if user.refund['status'] == 4:
                                    return MyException(param.ORDER_REFUND_STATUS_DONE_ERROR).toJson()
                                if user.refund['status'] == 4 and data['set']['refund']['status'] == 5:
                                    return MyException(param.ORDER_REFUND_STATUS_ERROR1).toJson()
                                user.refund['status'] = data['set']['refund']['status']
                            if subkey == 'remake':
                                user.refund['remake'].append(data['set']['refund']['remake'])
                            if subkey == 'price':
                                if data['set']['refund']['price'] > user.price :
                                    return MyException(param.ORDER_REFUND_PRICE_GT_ERROR).toJson()
                                user.refund['price'] = data['set']['refund']['price']
                            if subkey == 'products':
                                user.refund['products'] = data['set']['refund']['products']
                            if subkey == 'express':
                                for expresskey in data['set']['refund']['express']:
                                    if expresskey == 'name':
                                        user.refund['express']['name'] = data['set']['refund']['express']['name']
                                    if expresskey == 'code':
                                        user.refund['express']['code'] = data['set']['refund']['express']['code']
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
                user.date = user.date.strftime('%Y-%m-%d %H:%M:%S')
                #交易完成 计算分销所得
                if fxIndex == 1:
                    jsfx(appkey,user)
                return MyResult(user).toJson()
            else:
                return MyException(param.ARTICLE_NULL).toJson()
        except Exception as e:
            print e
            return MyException([param.PARAM_FAILURE[0],unicode(e)]).toJson()

    if request.method == 'GET':
        return param.PLEASE_USE_POST

#计算分销所得
#togetherProfit 总利润
def jsfx(appkey,order):
    if order.user:
        #计算订单总利润
        togetherProfit = 0  # 总利润
        togetherCost = 0    #总成本
        for product in order.product:
            togetherCost += product['costprice']
        togetherProfit = order.price - togetherCost
        if togetherProfit<= 0:
            return
        my = connection.APP_User.find_one({"_id": ObjectId(order.user)})
        #获取分销设置
        fxset = connection.Fenxiao.find_one({"appkey": appkey})
        # 获取一级分销
        if my.referee and fxset.status == 1:
            fx1 = connection.APP_User.find_one({"_id": ObjectId(my.referee)})
            profit = togetherProfit * fxset.fx1
            fx1.integral = profit
            fx1.save()
            # 获取二级分销
            if fx1.referee:
                fx2 = connection.APP_User.find_one({"_id": ObjectId(fx1.referee)})
                profit = togetherProfit * fxset.fx2
                fx2.integral = profit
                fx2.save()
                # 获取三级分销
                if fx2.referee:
                    fx3 = connection.APP_User.find_one({"_id": ObjectId(fx2.referee)})
                    profit = togetherProfit * fxset.fx3
                    fx3.integral = profit
                    fx3.save()
