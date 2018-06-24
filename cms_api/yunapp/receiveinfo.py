#!/usr/bin/python
# -*-coding:utf-8 -*-
from yunapp import app, result, connection, request, tool, config, sms
from yunapp.model.commentModel import *
from yunapp.result import *
from yunapp import param
from bson.objectid import ObjectId
from datetime import datetime

'''
获取收货地址列表
{
    'pageSize': 10,
    'page':1
    filter = ''
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''


@app.route('/app/receive/list', methods=['GET', 'POST'])
def get_receiveinfos():
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
            fnuser = connection.Receiveinfo.find(params, {'del': 0}).limit(pageSize).skip((page - 1) * pageSize).sort(
                [('_id', -1)])
            for user in fnuser:
                user['_id'] = str(user['_id'])
                if user.userid:
                    fnuser1 = connection.APP_admin.find_one(
                        {'appkey': appkey, '_id': ObjectId(user.userid), 'del': 0})
                    if fnuser1:
                        fnuser1['_id'] = str(fnuser1['_id'])
                        user['user'] = fnuser1
                    fnuser2 = connection.APP_User.find_one(
                        {'appkey': appkey, '_id': ObjectId(user.userid), 'del': 0})
                    if fnuser2:
                        fnuser2['_id'] = str(fnuser2['_id'])
                        user['user'] = fnuser2
                admins['data'].append(user)
            admins['count'] = fnuser.count()
            return MyResult(admins).toJson()
        except Exception as e:
            print e
            return MyException(param.CHECK_FAILURE).toJson()


    if request.method == 'GET':
        return param.PLEASE_USE_POST


'''
添加收货地址
{
    'name':'xiaosan', #或phone email
    'password':'11122',
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''


@app.route('/app/receive/add', methods=['GET', 'POST'])
def add_receive():
    if request.method == 'POST':
        appkey = ''
        token = ''
        try:
            token = request.headers[config.AUTHORIZATION]
        except:
            return MyException(param.APP_TOKEN_NULL).toJson()
        data = request.get_json()
        user = connection.Receiveinfo()
        for key in data:
            if data[key] == '':
                continue
            if key == 'userid':
                user.userid = data['userid']
            if key == 'mphone':
                user.mphone = data['mphone']
            if key == 'phone':
                user.phone = data['phone']
            if key == 'province':
                user.province = data['province']
            if key == 'city':
                user.city = data['city']
            if key == 'area':
                user.area = data['area']
            if key == 'address':
                user.address = data['address']
            if key == 'default':
                user.default = data['default']
            if key == 'name':
                user.name = data['name']
        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson()
        else:
            resultTooken = tool.ruleToken(token,True)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0]
        if user.userid and user.mphone:
            try:
                user.appkey = appkey
                user.save()
                return MySucceedResult().toJson()
            except Exception as e:
                print  e
                return MyException([param.CHECK_FAILURE[0],unicode(e)]).toJson()
        else:
            return MyException(param.PARAM_FAILURE).toJson()

    if request.method == 'GET':
        return param.PLEASE_USE_POST


'''
post  更新收货地址信息
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


@app.route('/app/receive/update', methods=['GET', 'POST'])
def app_receive_update():
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
            user = connection.Receiveinfo.find_one({'appkey': appkey, '_id': ObjectId(data['_id'])})
            if user:
                user['del'] = int(user['del'])
                for key in data['set']:
                    if data['set'][key] == '':
                        continue
                    if key == 'mphone':
                        user.mphone = data['set']['mphone']
                    if key == 'phone':
                        user.phone = data['set']['phone']
                    if key == 'province':
                        user.province = data['set']['province']
                    if key == 'city':
                        user.city = data['set']['city']
                    if key == 'area':
                        user.area = data['set']['area']
                    if key == 'address':
                        user.address = data['set']['address']
                    if key == 'default':
                        user.default = data['set']['default']
                    if key == 'name':
                        user.name = data['set']['name']
                    if key == 'del':
                        user['del'] = data['set']['del']
                if(user.default == 1):
                    connection.Receiveinfo.find_and_modify({'userid':user.userid,'del':0},{'$set':{'default':0}})
                user.save()
                user['_id'] = str(user['_id'])
                return MyResult(user).toJson()
            else:
                return MyException(param.ARTICLE_NULL).toJson()
        except Exception as e:
            print e
            return MyException(param.PARAM_FAILURE).toJson()

    if request.method == 'GET':
        return param.PLEASE_USE_POST