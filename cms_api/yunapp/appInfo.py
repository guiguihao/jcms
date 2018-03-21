#!/usr/bin/python
#-*-coding:utf-8 -*-
from yunapp import app,result,connection,request,tool,config
from yunapp.model.shopModel import *
from yunapp.model.userModel import *
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
@app.route('/app/admin/info/get',methods=['GET', 'POST'])
def app_info_get():
    if request.method == 'POST':
        data = request.get_json()
        appInfo = connection.AppInfo()
        token = ''
        appkey = ''
        for key in data:
            if key == 'token':
                token = data['token']
                # del data['token']
    if token == '' or not token:
        return MyException(param.APP_TOKEN_NULL).toJson() 
    else:
        resultTooken = tool.ruleToken(token)
        appkey = token.split('&&')[0]
        if resultTooken[0] != 1:
            return MyException(resultTooken).toJson()
        else:
            appInfo.appkey = appkey
    try:
        fdApp = connection.AppInfo.find_one({'appkey':appkey})
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
@app.route('/app/admin/info/update',methods=['GET', 'POST'])
def app_info_update():
    if request.method == 'POST':
        data = request.get_json()
        appInfo = connection.AppInfo()
        token = ''
        appkey = ''
        for key in data:
            if key == 'token':
                token = data['token']
                # del data['token']
    if token == '' or not token:
        return MyException(param.APP_TOKEN_NULL).toJson() 
    else:
        resultTooken = tool.ruleToken(token)
        appkey = token.split('&&')[0]
        if resultTooken[0] != 1:
            return MyException(resultTooken).toJson()
        else:
            appInfo.appkey = appkey
    try:
        fdApp = connection.AppInfo.find_one({'appkey':appkey})
        if fdApp:
            parse(fdApp,data)
            print fdApp
            fdApp.save()
        else:
            parse(appInfo,data)
            appInfo.save()
        return  MySucceedResult().toJson()               
    except Exception as e:
          print e
          return MyException(param.PARAM_FAILURE).toJson()
        
  
    if request.method == 'GET':
        return param.PLEASE_USE_POST



def parse(appinfo,data):
    for key in data['set']:
          if key == 'domian':
              appinfo['domian'] = data['set']['domian']
          if key == 'status':
              appinfo['status'] = data['set']['status']
          if key == 'name':
              appinfo['name'] = data['set']['name']
          if key == 'email':
              appinfo['email'] = data['set']['email']
          if key == 'phone':
              appinfo['phone'] = data['set']['phone']
          if key == 'beian':
              appinfo['beian'] = data['set']['beian']
          if key == 'reserved_1':
              appinfo['reserved_1'] = data['set']['reserved_1']
          if key == 'reserved_2':
              appinfo['reserved_2'] = data['set']['reserved_2']
          if key == 'reserved_3':
              appinfo['reserved_3'] = data['set']['reserved_3']
          if key == 'reserved_4':
              appinfo['reserved_4'] = data['set']['reserved_4']



