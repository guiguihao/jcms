#!/usr/bin/python
#-*-coding:utf-8 -*-
from yunapp import app,result,connection,request,tool,config,sms,session
from yunapp.model.userModel import *
from yunapp.result import *
from yunapp import param
from bson.objectid import ObjectId
from datetime import datetime



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
                   'count':0,
                    'data':[],
                }
                params = {
                    'appkey': appkey,
                    'del': 0,
                }
                if isinstance(filter,dict):
                    for k in filter:
                        params[k] = filter[k]
                fnuser = connection.APP_User.find(params,{'del':0}).limit(pageSize).skip((page-1)*pageSize).sort([('_id',-1)])
                for user in fnuser:
                    user['_id'] = str(user['_id'])
                    user.date = user.date.strftime('%Y-%m-%d %H:%M:%S')
                    vip = connection.Type.one({'appkey':appkey,'_id':ObjectId(user['vip'])},{'del':0})
                    if vip:
                       vip['_id'] = str(vip['_id'])
                       user.vip = vip
                       vip.date = vip.date.strftime('%Y-%m-%d %H:%M:%S')
                    admins['data'].append(user)
                admins['count']=fnuser.count()
                return MyResult(admins).toJson()
            except Exception as e:
                print e
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
        appkey = ''
        token = ''
        try:
            token = request.headers[config.AUTHORIZATION]
        except:
            return MyException(param.APP_TOKEN_NULL).toJson()
        data = request.get_json()
        user = connection.APP_User()
        for key in data:
            if data[key] == '':
                continue
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
            if key == 'icon':
                user.icon = data['icon']
            if key == 'wachat':
                user.wachat = data['wachat']
            if key == 'nickname':
                user.nickname = data['nickname']
            if key == 'info':
                user.info = data['info']
            if key == 'vip':
                user.vip = data['vip']
            if key == 'referee':
                user.referee = data['referee']
            if key == 'reserved_1':
                user.reserved_1 = data['reserved_1']
            if key == 'reserved_2':
                user.reserved_1 = data['reserved_2']
            if key == 'reserved_3':
                user.reserved_1 = data['reserved_3']
            if key == 'reserved_4':
                user.reserved_1 = data['reserved_4']
            if key == 'reserved_5':
                user.reserved_1 = data['reserved_5']
            if key == 'reserved_6':
                user.reserved_1 = data['reserved_6']

        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson() 
        else:
            resultTooken = tool.ruleToken(token,True)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0]
        if ((user.name or user.email) and user.password) or user.phone:
            try:
                try:
                    fnuser = connection.APP_User.find_one({'appkey':appkey,'name':user.name,'del':0})
                    if fnuser: 
                        if fnuser.name: return MyException(param.USER_NAME_FAILURE).toJson()
                    
                    feuser = connection.APP_User.find_one({'appkey':appkey,'email':user.email,'del':0})
                    if feuser: 
                        if feuser.email: return MyException(param.USER_EMAIL_FAILURE).toJson()

                    fpuser = connection.APP_User.find_one({'appkey':appkey,'phone':user.phone,'del':0})
                    # print fpuser
                    if fpuser:
                        if fpuser.phone: return MyException(param.USER_PHONE_FAILURE).toJson()
                except Exception, e:
                    return MyException(param.CHECK_FAILURE).toJson()
                vips = connection.Type.find({'appkey': appkey}).sort([('level',1)])
                if vips.count()>0:
                     user.vip = unicode(vips[0]['_id'])
                if user.password:
                    user.password = unicode(tool.md5(user.password))
                user.appkey = appkey
                user.date = datetime.now()
                if not user.name:
                    if user.email: user.name = user.email
                    if user.phone: user.name = user.phone
                user.save()
                return  MySucceedResult().toJson()
            except Exception as e:
                print  e
                return MyException(param.CHECK_FAILURE).toJson()
        else:
           return MyException(param.REGISTER_FAILURE).toJson()
  
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
@app.route('/app/user/update',methods=['GET', 'POST'])
def app_user_update():
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
            user = connection.APP_User.find_one({'appkey':appkey,'_id':ObjectId(data['_id'])})
            if user:
                user['del'] = int(user['del'])
                for key in data['set']:
                    if data['set'][key] == '':
                        continue
                    if key == 'name':
                        user.name = data['set']['name']
                    if key == 'password':
                        user.password = data['set']['password']
                    if key == 'phone':
                        user.phone = data['set']['phone']
                    if key == 'status':
                        user.status = data['set']['status']
                    if key == 'email':
                        user.email = data['set']['email']
                    if key == 'qq':
                        user.qq = data['set']['qq']
                    if key == 'icon':
                        user.icon = data['set']['icon']
                    if key == 'wachat':
                        user.wachat = data['set']['wachat']
                    if key == 'vip':
                        user.vip = data['set']['vip']
                    if key == 'integral':
                        user.integral = data['set']['integral']
                    if key == 'nickname':
                        user.nickname = data['set']['nickname']
                    if key == 'reserved_1':
                        user.reserved_1 = data['set']['reserved_1']
                    if key == 'reserved_2':
                        user.reserved_2 = data['set']['reserved_2']
                    if key == 'reserved_3':
                       user.reserved_3 = data['set']['reserved_3']
                    if key == 'reserved_4':
                        user.reserved_4 = data['set']['reserved_4']
                    if key == 'reserved_5':
                       user.reserved_5 = data['set']['reserved_5']
                    if key == 'reserved_6':
                        user.reserved_6 = data['set']['reserved_6']
                    if key == 'del':
                        user['del'] = data['set']['del']
                    if key == 'permission':
                        user.permission = data['set']['permission']
                user.save()
                user['_id'] = str(user['_id'])
                return MyResult(user).toJson()
            else:
                MyException(param.APP_USER_NULL).toJson()
        except Exception as e:
            print e
            return MyException(param.PARAM_FAILURE).toJson()
            
    if request.method == 'GET':
        return param.PLEASE_USE_POST


'''
支持用户名 手机号码  邮箱登陆
{
    'name':'xxx',
    'password':'xxxxx',  #md5(密码)
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
    { "_id" : ObjectId("5aa0e1ba4683e6051152f780"), "name" : "admin", "password" : "7fef6171469e80d32c0559f88b377245", "appkey" : "5aa0e1ba4683e6051152f780", "appsecret" : "jjjjddjjdjd", "del" : 0 }
}
'''
@app.route('/app/user/login',methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        token = ''
        appkey = ''
        try:
            token = request.headers[config.AUTHORIZATION]
        except:
            return MyException(param.APP_TOKEN_NULL).toJson()
        data = request.get_json()
        user = connection.APP_User()
        try:
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
        except Exception, e:
            return MyException(param.PARAM_FAILURE).toJson()
        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson()
        else:
            resultTooken = tool.ruleToken(token,False)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0]
        # print user
        if ((user.name or user.email) and user.password) or  user.phone or user.wachat or user.qq:
            myuser = ''
            if user.name:
                 myuser = connection.APP_User.find_one({'appkey':appkey,'name':user.name,'del':0},{'userTypes':0,'appsecret':0,'del':0,})
            if user.phone:
                 myuser = connection.APP_User.find_one({'appkey':appkey,'phone':user.phone,'del':0},{'userTypes':0,'appsecret':0,'del':0,})
            if user.qq:
                 myuser = connection.APP_User.find_one({'appkey':appkey,'qq':user.qq,'del':0},{'userTypes':0,'appsecret':0,'del':0,})
            if user.wachat:
                myuser = connection.APP_User.find_one({'appkey': appkey, 'wachat': user.wachat, 'del': 0},{'userTypes': 0, 'appsecret': 0, 'del': 0, })
            if user.email:
                 myuser = connection.APP_User.find_one({'appkey':appkey,'email':user.email,'del':0},{'userTypes':0,'appsecret':0,'del':0,})

            if myuser == None:
                return MyException(param.APP_USER_NULL).toJson()
            if (myuser and myuser['password'] == user['password']) or  (user.phone and myuser != '' and myuser):
                myuser['_id'] = str(myuser['_id'])
                myuser.pop('password')
                # user['_id'] = str(user['_id'])
                # userVip = connection.UserVip.find_one({'appkey':appkey,'del':0},({'del':-1})
                # myuser.vip = userVip
                session[config.SESSION_KEY] = appkey
                return  MyResult(myuser).toJson()
            else:
                return  MyException(param.LONGIN_FAILURE).toJson()
        else:
            return      MyException(param.PARAM_FAILURE).toJson()
    if request.method == 'GET':
        return param.PLEASE_USE_POST

'''
退出
{
    'name':'xxx',
    'password':'xxxxx',  #md5(密码)
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
    { "_id" : ObjectId("5aa0e1ba4683e6051152f780"), "name" : "admin", "password" : "7fef6171469e80d32c0559f88b377245", "appkey" : "5aa0e1ba4683e6051152f780", "appsecret" : "jjjjddjjdjd", "del" : 0 }
}
'''
@app.route('/app/user/logout',methods=['GET', 'POST'])
def user_logout():
    if request.method == 'POST':
        token = ''
        appkey = ''
        try:
            token = request.headers[config.AUTHORIZATION]
        except:
            return MyException(param.APP_TOKEN_NULL).toJson()
        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson()
        else:
            resultTooken = tool.ruleToken(token,True)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0]
        # print user
        session.pop(config.SESSION_KEY, None)
        return MySucceedResult().toJson()
    if request.method == 'GET':
        return param.PLEASE_USE_POST