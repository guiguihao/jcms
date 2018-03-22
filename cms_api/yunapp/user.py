#!/usr/bin/python
#-*-coding:utf-8 -*-
from yunapp import app,result,connection,request,tool,config,sms
from yunapp.model.shopModel import *
from yunapp.model.userModel import *
from yunapp.result import *
from yunapp import param
from bson.objectid import ObjectId



'''
获取用户列表
{
    'pageSize': 10,
    'page':1
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/app/user/list',methods=['GET', 'POST'])
def get_users():
    if request.method == 'POST':
        data = request.get_json()
        user = connection.APP_User()
        appkey = ''
        pageSize = 50
        page = 1
        for key in data:
            if key == 'token':
                token = data['token']
            if key == 'pageSize':
                pageSize = data['pageSize']
            if key == 'page':
                page = data['page']
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
                   'count':0,
                    'data':[],
                }
                fnuser = connection.APP_User.find({'appkey':appkey,'del':0},{'del':0}).limit(pageSize).skip((page-1)*pageSize)
                for user in fnuser:
                    user['_id'] = str(user['_id'])
                    admins['data'].append(user)
                admins['count']=fnuser.count()
                return MyResult(admins).toJson()
            except Exception as e:
                return MyException(param.CHECK_FAILURE).toJson()
        else:
           return MyException(param.REGISTER_FAILURE).toJson()
  
    if request.method == 'GET':
        return param.PLEASE_USE_POST

'''
用户注册/添加
{
    'name':'xiaosan', #或phone email
    'password':'11122',
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/app/user/add',methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        data = request.get_json()
        user = connection.APP_User()
        appkey = ''
        for key in data:
            if key == 'name':
                user.name = data['name']
            if key == 'password':
                user.password = data['password']
            if key == 'phone':
                user.phone = data['phone']
            if key == 'email':
                user.email = data['email']
            if key == 'qq':
                user.qq = data['qq']
            if key == 'wachat':
                user.wachat = data['wachat']
            if key == 'nickname':
                user.nickname = data['nickname']
            if key == 'info':
                user.info = data['info']
            if key == 'permission':
                user.permission = data['permission']
            if key == 'token':
                token = data['token']
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
            resultTooken = tool.ruleToken(token)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0]

        if (user.name or user.phone or user.email) and user.password:
            try:
                try:
                    fnuser = connection.APP_User.find_one({'appkey':appkey,'name':user.name,'del':0})
                    if fnuser: 
                        if fnuser.name: return MyException(param.USER_NAME_FAILURE).toJson()
                    
                    feuser = connection.APP_User.find_one({'appkey':appkey,'email':user.email,'del':0})
                    if feuser: 
                        if feuser.email: return MyException(param.USER_EMAIL_FAILURE).toJson()

                    fpuser = connection.APP_User.find_one({'appkey':appkey,'phone':user.phone,'del':0})
                    #print fpuser
                    if fpuser:
                        if fpuser.phone: return MyException(param.USER_PHONE_FAILURE).toJson()
                except Exception, e:
                    pass
                user.password = unicode(tool.md5(user.password))
                user.appkey = appkey
                user.save()
                return  MySucceedResult().toJson()
            except Exception as e:
                print e
                return MyException(param.CHECK_FAILURE).toJson()
        else:
           return MyException(param.REGISTER_FAILURE).toJson()
  
    if request.method == 'GET':
        return param.PLEASE_USE_POST

'''
post  更新管理员
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
@app.route('/app/user/update',methods=['GET', 'POST'])
def app_user_update():
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
            user = connection.APP_admin.find_one({'appkey':appkey,'_id':ObjectId(data['_id'])})
            if user:
            	user['del'] = int(user['del'])
	            for key in data['set']:
	                if key == 'name':
	                    user.password = data['set']['password']
	                if key == 'phone':
	                    user.phone = data['set']['phone']
	                if key == 'status':
	                    user.status = data['set']['status']    
	                if key == 'email':
	                    user.email = data['set']['email']
	                if key == 'qq':
	                    user.qq = data['set']['qq']
	                if key == 'wachat':
	                    user.wachat = data['set']['wachat']
	                if key == 'nickname':
	                    user.nickname = data['set']['nickname']
	                if key == 'appsecret':
	                    user.appsecret = data['set']['appsecret']   
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
	                    if user.superadmin == 1 and user['del'] == 1:
	                        return MyException(param.APP_USER_DEL_NULL).toJson()
	                if key == 'permission':
	                    user.permission = data['set']['permission']    
	            user.save()
	            # connection.APP_admin.find_and_modify({'appkey':appkey,'del':0},{'$set':data['set']})
	            # user = connection.APP_admin.find_one({'appkey':appkey,'del':0},{'del':0,'appsecret':0})
	            user['_id'] = str(user['_id'])
	            return MyResult(user).toJson()
            
        except Exception as e:
            print e
            return MyException(param.PARAM_FAILURE).toJson()
            
    if request.method == 'GET':
        return param.PLEASE_USE_POST