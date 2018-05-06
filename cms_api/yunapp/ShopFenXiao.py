#!/usr/bin/python
#-*-coding:utf-8 -*-
from yunapp import app,result,connection,request,tool,config
from yunapp.model.shopModel import *
from yunapp.result import *
from yunapp import param
from bson.objectid import ObjectId




'''
获取fenxiao
{   
     ''
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/app/shop/fenxiao/get',methods=['GET', 'POST'])
def app_fenxiao_get():
    if request.method == 'POST':
        appkey = ''
        token = ''
        try:
            token = request.headers[config.AUTHORIZATION]
        except:
            return MyException(param.APP_TOKEN_NULL).toJson()
        data = request.get_json()
        appInfo = connection.Fenxiao()
        for key in data:
            if key == 'token':
                token = data['token']
                # del data['token']
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
            fdApp = connection.Fenxiao.find_one({'appkey':appkey})
            if fdApp:
                fdApp['_id'] = str(fdApp['_id'])
            return MyResult(fdApp).toJson()
        except Exception as e:
              return MyException(param.PARAM_FAILURE).toJson()

    if request.method == 'GET':
        return param.PLEASE_USE_POST



'''
添加或修改fenxiao
{   
     'set':{}
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/app/shop/fenxiao/update',methods=['GET', 'POST'])
def app_fenxiao_update():
    if request.method == 'POST':
        appkey = ''
        token = ''
        try:
            token = request.headers[config.AUTHORIZATION]
        except:
            return MyException(param.APP_TOKEN_NULL).toJson()
        data = request.get_json()
        appInfo = connection.Fenxiao()
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
            fdApp = connection.Fenxiao.find_one({'appkey':appkey})
            if fdApp:
                parse(fdApp,data)
                if fdApp.fx1 + fdApp.fx2 + fdApp.fx3 >1:
                    return MyException(param.FENXIAO_FENCHENG_ERROR1).toJson()
                fdApp.save()
            else:
                parse(appInfo,data)
                if fdApp.fx1 + fdApp.fx2 + fdApp.fx3 > 1:
                    return MyException(param.FENXIAO_FENCHENG_ERROR1).toJson()
                appInfo.save()
            return  MySucceedResult().toJson()
        except Exception as e:
              print e
              return MyException(param.PARAM_FAILURE).toJson()
    if request.method == 'GET':
        return param.PLEASE_USE_POST



def parse(appinfo,data):
    for key in data['set']:
          if key == 'status':
              appinfo['status'] = data['set']['status']
          if key == 'fx1':
              appinfo['fx1'] = data['set']['fx1']
          if key == 'fx2':
              appinfo['fx2'] = data['set']['fx2']
          if key == 'fx3':
              appinfo['fx3'] = data['set']['fx3']


