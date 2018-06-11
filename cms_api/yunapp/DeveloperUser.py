#!/usr/bin/python
#-*-coding:utf-8 -*-
from yunapp import app,result,connection,request,tool,config
from yunapp.model.userModel import *
from yunapp.result import *
from yunapp import param
from bson.objectid import ObjectId



'''
获取appkey appsecret 
{
  name:'',
  password:'',
  token:'md5(password+MD5_KEy)'  
}
'''
@app.route('/app/developer/appkey/get',methods=['GET', 'POST'])
def appkey_get():
    if request.method == 'POST':
        data = request.get_json()
        user= connection.APP_admin()
        token = ''
        for key in data:
            if key == 'name':
                user.name = data['name']
            if key == 'password':
                user.password = data['password']
            if key == 'phone':
                user.phone = data['phone']
            if key == 'email':
                user.email = data['email']
            if key == 'token':
                token = data['token']
                user.token = token
        resultTooken = tool.ruleToken2(token,user.password,config.MD5_KEY)
        if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
        if (user.name or user.phone or user.email) and user.password:
            try:
                myuser = ''
                if user.name:
                     myuser = connection.APP_admin.find_one({'name':user.name,'del':0},{'del':0,})
                if user.phone:
                     myuser = connection.APP_admin.find_one({'phone':user.phone,'del':0},{'del':0,})
                if user.email:
                     myuser = connection.APP_admin.find_one({'email':user.email,'del':0},{'del':0,})
                if myuser and myuser['password'] == user['password']:
                    myuser['_id'] = str(myuser['_id'])
                    myuser.pop('password')
                    return  MyResult(myuser).toJson()
                else:
                    return  MyException(param.LONGIN_FAILURE).toJson()
            except Exception as e:
                return MyException(param.CHECK_FAILURE).toJson()
        else:
           return MyException(param.REGISTER_FAILURE).toJson()
  
    if request.method == 'GET':
        return param.PLEASE_USE_POST


'''
userid+MD5_KEy 校验 
{
  name:'',
  password:'',
  token:'md5(password+MD5_KEy)'  
}
'''
@app.route('/app/developer/user/add',methods=['GET', 'POST'])
def developer_add():
    if request.method == 'POST':
        data = request.get_json()
        user= connection.DeveloperUser()
        token = ''
        for key in data:
            if key == 'name':
                user.name = data['name']
            if key == 'password':
                user.password = data['password']
            if key == 'phone':
                user.phone = data['phone']
            if key == 'email':
                user.email = data['email']
            if key == 'token':
                token = data['token']
                user.token = token
        if token != tool.md5(user.password + config.MD5_KEY):
            return MyException(param.APP_TOKEN_ERROR).toJson()
        if (user.name or user.phone or user.email) and user.password:
            try:
                fnuser = connection.DeveloperUser.find_one({'name':user.name})
                #print fnuser
                if fnuser: 
                    if fnuser.name: return MyException(param.USER_NAME_FAILURE).toJson()
                
                feuser = connection.DeveloperUser.find_one({'email':user.email})
                if feuser: 
                    if feuser.email: return MyException(param.USER_EMAIL_FAILURE).toJson()

                fpuser = connection.DeveloperUser.find_one({'phone':user.phone})
                #print fpuser
                if fpuser:
                    if fpuser.phone: return MyException(param.USER_PHONE_FAILURE).toJson()
                user.password = tool.md5(user.password)
                user.save()
                userVip = connection.UserVip.find({'appkey':config.DEVELOPER_APPKEY,'del':0}).sort('level',1)[0]
                #print userVip
                if(userVip): connection.DeveloperUser.find_and_modify({'_id':user['_id'],'del':0},{'$set':{"vip":str(userVip['_id'])}})
                return  MySucceedResult().toJson()
            except Exception as e:
                return MyException(param.CHECK_FAILURE).toJson()
        else:
           return MyException(param.REGISTER_FAILURE).toJson()
  
    if request.method == 'GET':
        return param.PLEASE_USE_POST


'''
支持用户名 手机号码  邮箱登陆
{
    'name':'xxx',
    'password':'xxxxx',
    'token:'md5(password+MD5_KEy)'
}
'''
@app.route('/app/developer/user/login',methods=['GET', 'POST'])
def developer_login():
    if request.method == 'POST':
        data = request.get_json()
        user = connection.DeveloperUser()
        token = ''
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
            if key == 'token':
                token = data['token']
        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson() 
        else:
            if token != tool.md5(user.password + config.MD5_KEY):
                 return MyException(param.APP_TOKEN_ERROR).toJson()
        if (user.name or user.phone or user.email or user.qq or user.wachat) and user.password:
            data['password'] = tool.md5(data['password'])
            user = connection.DeveloperUser.find_one(data)
            if user:
                user['_id'] = str(user['_id'])
                userVip = connection.UserVip.find_one({'_id':ObjectId(user.vip)})
                userVip['_id'] = str(userVip['_id'])
                user.vip = userVip
                return  MyResult(user).toJson()
            else:
                return  MyException(param.LONGIN_FAILURE).toJson()
        else:
            return      MyException(param.PARAM_FAILURE).toJson()
    if request.method == 'GET':
        return param.PLEASE_USE_POST


'''
post 
{
    '_id': 'xxxxxxx',
    set:{
       设置需要更新的字段即可,如下,可多个字段,不能包含_id
       name : 'xx',
       'vip': 'vip类型_id', #通过获取所有vip类型可以获取_id  /user/vip/type/get 
    },
    'token:'md5(_id+MD5_KEy)'
}
'''
@app.route('/app/developer/user/update',methods=['GET', 'POST'])
def developer_user_update():
    if request.method == 'POST':
        data = request.get_json()
        token = ''
        for key in data:
            if key == '_id':
                data['_id'] = ObjectId(data['_id'])
            if key == 'token':
                token = data['token']
        if token != tool.md5(str(data['_id']) + config.MD5_KEY):
                 return MyException(param.APP_TOKEN_ERROR).toJson()
        try:
            connection.DeveloperUser.find_and_modify({'_id':data['_id']},{'$set':data['set']})
            user = connection.DeveloperUser.find_one({'_id':data['_id']})
            user['_id'] = str(user['_id'])
            return MyResult(user).toJson()
        except Exception as e:
            return MyException(param.PARAM_FAILURE).toJson()
            
    if request.method == 'GET':
        return param.PLEASE_USE_POST







