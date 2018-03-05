#!/usr/bin/python
#-*-coding:utf-8 -*-
from yunapp import app,result,connection,request,tool,config
from yunapp.model.shopModel import *
from yunapp.model.userModel import *
from yunapp.result import *
from yunapp import param
from bson.objectid import ObjectId





'''
userid+MD5_KEy 校验 
{
  userid:'',
  appicon:'',
  appname:'',
  token:'md5(userid+MD5_KEy)'  
}
'''
@app.route('/app/add',methods=['GET', 'POST'])
def app_add():
    if request.method == 'POST':
        data = request.get_json()
        myapp= connection.App()
        token = ''
        for key in data:
            if key == 'userid':
                myapp.userid = data['userid']
            if key == 'appicon':
                myapp.appicon = data['appicon']
            if key == 'appname':
                myapp.appname = data['appname']
            if key == 'token':
                token = data['token']
        if token != tool.md5(myapp.userid + config.MD5_KEY):
            return MyException(param.APP_TOKEN_ERROR).toJson()
        myapp.appsecret = unicode(tool.randomString(16),'utf-8')
        if myapp.userid:
            try:
                fnApp = connection.App.find_one({'appname':myapp.appname,'userid':myapp.userid})
                print fnApp
                if fnApp: 
                    if fnApp.appname: return MyException(param.APP_NAME_FAILURE).toJson()
                myapp.save()
                connection.App.find_and_modify({'_id':myapp['_id']},{'$set':{'appkey':str(myapp['_id'])}})
                return  MySucceedResult().toJson()
            except Exception as e:
                return MyException(param.PARAM_FAILURE).toJson()
        else:
           return MyException(param.PARAM_FAILURE).toJson()
  
    if request.method == 'GET':
        return param.PLEASE_USE_POST

'''
{
    'userid':'',
    'appkey':''
     token:'md5(userid+MD5_KEy)'  
}
'''
@app.route('/app/del',methods=['GET', 'POST'])
def app_del():
    if request.method == 'POST':
        data = request.get_json()
        myapp= connection.App()
        token = ''
        for key in data:
            if key == 'appkey':
                myapp['_id'] = ObjectId(data['appkey'])
            if key == 'userid':
                myapp.userid = data['userid']
            if key == 'token':
                token = data['token']
        if myapp['_id'] is None or myapp.userid is None:
            return MyException(param.PARAM_FAILURE).toJson()
        if token != tool.md5(myapp.userid + config.MD5_KEY):
            return MyException(param.APP_TOKEN_ERROR).toJson()
        try:
            connection.App.find_and_modify({'_id':myapp['_id']},{'$set':{'del':1}})
            return  MySucceedResult().toJson()
        except Exception as e:
            return MyException(param.PARAM_FAILURE).toJson()
  
    if request.method == 'GET':
        return param.PLEASE_USE_POST

'''
{
    'appkey':'',
    'userid':'',
    set:{
       appicon:''
       appname:''
    }
    token:'md5(userid+MD5_KEy)'  
}
'''
@app.route('/app/update',methods=['GET', 'POST'])
def add_update():
    if request.method == 'POST':
        data = request.get_json()
        myApp = connection.App()
        myset = {}
        token = ''
        for key in data:
            if key == 'appkey':
                myApp['_id'] = data['appkey']
            if key == 'userid':
                myApp.userid = data['userid']
            if key == 'set':
                myset = data['set']
                for k in myset:
                    if k == '_id' or k == 'del' or k == 'appkey' or k == 'appsecret':
                        MyException(param.PARAM_FAILURE).toJson()
            if key == 'token':
                token = data['token']
        if myapp['_id'] is None or myapp.userid is None:
            return MyException(param.PARAM_FAILURE).toJson()
        if token != tool.md5(myapp.userid + config.MD5_KEY):
            return MyException(param.APP_TOKEN_ERROR).toJson()
        try:
            connection.App.find_and_modify({'_id':myapp['_id']},{'$set':myset})
            return  MySucceedResult().toJson()
        except Exception as e:
            return MyException(param.PARAM_FAILURE).toJson()
    if request.method == 'GET':
        return param.PLEASE_USE_POST


'''
刷新appsecret, 
{
    'appkey':'',
    'userid':'',
    token:'md5(userid+MD5_KEy)'
}
'''
@app.route('/app/resecret',methods=['GET', 'POST'])
def app_resecret():
    if request.method == 'POST':
        data = request.get_json()
        myApp = connection.App()
        myapp.appsecret = tool.randomString(16)
        token = ''
        for key in data:
            if key == 'appkey':
                myApp.appkey = data['appkey']
            if key == 'userid':
                myApp.userid = data['userid']
            if key == 'token':
                token = data['token']
        if myapp.appkey is None or myapp.userid is None:
            return MyException(param.PARAM_FAILURE).toJson()
        if token != tool.md5(myapp.userid + config.MD5_KEY):
            return MyException(param.APP_TOKEN_ERROR).toJson()
        try:
            connection.App.find_and_modify({'appkey':myapp.appkey},{'$set':{'appsecret':myapp.appsecret}})
            newApp = connection.App.find_one({'appkey':myapp.appkey},{'del':0,'_id':0})
            return  MyResult(newApp).toJson()
        except Exception as e:
            return MyException(param.PARAM_FAILURE).toJson()
    if request.method == 'GET':
        return param.PLEASE_USE_POST


'''
获取用户下的所有app, 
{

    'userid':'',
    token:'md5(userid+MD5_KEy)'
}
'''
@app.route('/app/resecret',methods=['GET', 'POST'])
def app_get():
    if request.method == 'POST':
        data = request.get_json()
        myApp = connection.App()
        token = ''
        for key in data:
            if key == 'userid':
                myApp.userid = data['userid']
            if key == 'token':
                token = data['token']
        if myapp.userid is None:
            return MyException(param.PARAM_FAILURE).toJson()
        if token != tool.md5(myapp.userid + config.MD5_KEY):
            return MyException(param.APP_TOKEN_ERROR).toJson()
        try:
            newApps = connection.App.find({'userid':myapp.userid},{'del':0,'_id':0})
            applist = []
            for kapp in newApps:
                applist.append(kapp)
            return  MyResult(applist).toJson()
        except Exception as e:
            return MyException(param.PARAM_FAILURE).toJson()
    if request.method == 'GET':
        return param.PLEASE_USE_POST


        '''
获取appsecret, 
{
    'appkey':'',
    token:'md5(userid+MD5_KEy)'
}
'''
@app.route('/app/getsecret',methods=['GET', 'POST'])
def app_get_secret():
    if request.method == 'POST':
        data = request.get_json()
        myApp = connection.App()
        token = ''
        for key in data:
            if key == 'appkey':
                myApp.appkey = data['appkey']
            if key == 'token':
                token = data['token']
        if myapp.appkey is None:
            return MyException(param.PARAM_FAILURE).toJson()
        if token != tool.md5(myapp.userid + config.MD5_KEY):
            return MyException(param.APP_TOKEN_ERROR).toJson()
        try:
            newApp = connection.App.find_one({'appkey':myapp.appkey},{'del':0,'_id':0,'appkey':0,'appname':0,'appicon':0})
            return  MyResult(newApp).toJson()
        except Exception as e:
            return MyException(param.PARAM_FAILURE).toJson()
    if request.method == 'GET':
        return param.PLEASE_USE_POST


