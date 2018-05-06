#!/usr/bin/python
# -*-coding:utf-8 -*-
from yunapp import app, result, connection, request, tool, config
from yunapp.model.shopModel import *
from yunapp.result import *
from yunapp import param
from bson.objectid import ObjectId

'''
获取appinfo
{   
     ''
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''


@app.route('/app/admin/shopreturn/get', methods=['GET', 'POST'])
def shopreturn_get():
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
            fdApp = connection.ReturnGoodsinfo.find_one({'appkey': appkey})
            if fdApp:
                fdApp['_id'] = str(fdApp['_id'])
            return MyResult(fdApp).toJson()
        except Exception as e:
            return MyException(param.PARAM_FAILURE).toJson()

    if request.method == 'GET':
        return param.PLEASE_USE_POST


'''
添加或修改appinfo
{   
     'set':{}
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''


@app.route('/app/admin/shopreturn/update', methods=['GET', 'POST'])
def shopreturn_update():
    if request.method == 'POST':
        appkey = ''
        token = ''
        try:
            token = request.headers[config.AUTHORIZATION]
        except:
            return MyException(param.APP_TOKEN_NULL).toJson()
        data = request.get_json()
        appInfo = connection.ReturnGoodsinfo()
        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson()
        else:
            resultTooken = tool.ruleToken(token,True)
            appkey = token.split('&&')[0]
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appInfo.appkey = appkey
        try:
            fdApp = connection.ReturnGoodsinfo.find_one({'appkey': appkey})
            if fdApp:
                parse(fdApp, data)
                print fdApp
                fdApp.save()
            else:
                parse(appInfo, data)
                appInfo.save()
            return MySucceedResult().toJson()
        except Exception as e:
            print e
            return MyException(param.PARAM_FAILURE).toJson()

    if request.method == 'GET':
        return param.PLEASE_USE_POST


def parse(appinfo, data):
    for key in data['set']:
        if key == 'phone':
            appinfo['phone'] = data['set']['phone']
        if key == 'telephone':
            appinfo['telephone'] = data['set']['telephone']
        if key == 'address':
            appinfo['address'] = data['set']['address']
        if key == 'receiver':
            appinfo['receiver'] = data['set']['receiver']
        if key == 'code':
            appinfo['code'] = data['set']['code']
        if key == 'mark':
            appinfo['mark'] = data['set']['mark']



