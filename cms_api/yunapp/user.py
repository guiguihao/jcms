#!/usr/bin/python
#-*-coding:utf-8 -*-
from yunapp import app,result,connection,request,tool
from yunapp.model.shopModel import *
from yunapp.model.userModel import *
from yunapp.result import *
from yunapp import param
from bson.objectid import ObjectId



'''
注册用户,可以用户名,邮箱,手机号码注册, 密码必填选项
{
    'name':'xiaosan', #或phone email
    'password':'11122'
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/user/register',methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        data = request.get_json()
        user = connection.User()
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
            if key == 'qq':
                user.qq = data['qq']
            if key == 'wachat':
                user.wachat = data['wachat']
            if key == 'nickname':
                user.nickname = data['nickname']
            if key == 'address':
                user.address = data['address']
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
                fnuser = connection.User.find_one({'name':user.name,'appkey':appkey,'del':0})
                #print fnuser
                if fnuser: 
                    if fnuser.name: return MyException(param.USER_NAME_FAILURE).toJson()
                
                feuser = connection.User.find_one({'email':user.email,'appkey':appkey,'del':0})
                if feuser: 
                    if feuser.email: return MyException(param.USER_EMAIL_FAILURE).toJson()

                fpuser = connection.User.find_one({'phone':user.phone,'appkey':appkey,'del':0})
                #print fpuser
                if fpuser:
                    if fpuser.phone: return MyException(param.USER_PHONE_FAILURE).toJson()
                user.password = tool.md5(user.password)
                user.appkey = appkey
                user.save()
                userVip = connection.UserVip.find({'del':0}).sort('level',1)[0]
                #print userVip
                if(userVip): connection.User.find_and_modify({'_id':user['_id'],'del':0},{'$set':{"vip":str(userVip['_id'])}})
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
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/user/login',methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        data = request.get_json()
        user = connection.User()
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
            if key == 'qq':
                user.qq = data['qq']
            if key == 'wachat':
                user.wachat = data['wachat']
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
        if (user.name or user.phone or user.email or user.qq or user.wachat) and user.password:
            data['appkey'] = appkey
            data['del'] = 0
            data['password'] = tool.md5(data['password'])
            user = connection.User.find_one(data,{'del':0})
            if user:
                user['_id'] = str(user['_id'])
                userVip = connection.UserVip.find_one({'_id':ObjectId(user.vip),'del':0},{'del':0})
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
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/user/update',methods=['GET', 'POST'])
def user_update():
    if request.method == 'POST':
        data = request.get_json()
        token = ''
        appkey = ''
        for key in data:
            if key == '_id':
                data['_id'] = ObjectId(data['_id'])
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
            connection.User.find_and_modify({'_id':data['_id'],'appkey':appkey,'del':0},{'$set':data['set']})
            user = connection.User.find_one({'_id':data['_id'],'appkey':appkey,'del':0},{'del':0})
            user['_id'] = str(user['_id'])
            return MyResult(user).toJson()
        except Exception as e:
            return MyException(param.PARAM_FAILURE).toJson()
            
    if request.method == 'GET':
        return param.PLEASE_USE_POST


'''
添加或修改vip类型
{
    'level':0,
    'level_name':'一级会员',
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/user/vip/type/update',methods=['GET', 'POST'])
def user_vip_update():
    if request.method == 'POST':
        data = request.get_json()
        userVip = connection.UserVip()
        token = ''
        appkey = ''
        for key in data:
            if key == 'level':
                userVip.level = data['level']
            if key == 'level_name':
                userVip.level_name = data['level_name']
            if key == 'level_dec':
                userVip.level_dec = data['level_dec']
            if key == 'reserved_1':
                userVip.reserved_1 = data['reserved_1']
            if key == 'reserved_2':
                userVip.reserved_1 = data['reserved_2']
            if key == 'reserved_3':
                userVip.reserved_1 = data['reserved_3']
            if key == 'reserved_4':
                userVip.reserved_1 = data['reserved_4']
            if key == 'token':
                token = data['token']
                del data['token']
    if token == '' or not token:
        return MyException(param.APP_TOKEN_NULL).toJson() 
    else:
        resultTooken = tool.ruleToken(token)
        if resultTooken[0] != 1:
            appkey = token.split('&&')[0]
            return MyException(resultTooken).toJson()
        else:
            userVip.appkey = appkey
    try:
          if userVip.level  and userVip.level_name:
                fvip = connection.UserVip.find_one({'level':userVip.level,'appkey':appkey})
                if fvip:
                    connection.UserVip.find_and_modify({'level':userVip.level,'appkey':appkey},{'$set':data})
                else:
                    userVip.save()
                return  MySucceedResult().toJson()
          else:
                return MyException(param.PARAM_FAILURE).toJson()
    except Exception as e:
          return MyException(param.PARAM_FAILURE).toJson()
        
  
    if request.method == 'GET':
        return param.PLEASE_USE_POST


'''
获取所有vip类型
{
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/user/vip/type/get',methods=['GET', 'POST'])
def user_vip_get_all_viptype():
    if request.method == 'POST':
        data = request.get_json()
        userVip = connection.UserVip()
        token = ''
        appkey = ''
        for key in data:
            if key == 'level':
                userVip.level = data['level']
            if key == 'level_name':
                userVip.level_name = data['level_name']
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
          allVipType = connection.UserVip.find({'appkey':appkey,'del':0},{'del':0})
          vips = []
          for viptype in allVipType:
              viptype['_id'] = str(viptype['_id'])
              vips.append(viptype)
          return MyResult(vips).toJson()
    except Exception as e:
          return MyException(param.PARAM_FAILURE).toJson()
    if request.method == 'GET':
        return param.PLEASE_USE_POST
    
'''
删除vip类型
{
    'del'  : '类型_id'
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/user/vip/type/del',methods=['GET', 'POST'])
def user_vip_del_viptype():
    if request.method == 'POST':
        data = request.get_json()
        userVip = connection.UserVip()
        token = ''
        appkey = ''
        for key in data:
            if key == 'del':
                userVip['del'] = data['del']
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
          vip = connection.UserVip.find({'appkey':appkey,'_id':ObjectId(userVip['del']),'del':0})
          if not vip:
              return MyException(param.USER_VIP_FAILURE).toJson()
          connection.UserVip.find_and_modify({'appkey':appkey,'del':0},{'$set':{'del':1}})
          return MySucceedResult().toJson()
    except Exception as e:
          return MyException(param.PARAM_FAILURE).toJson()
    if request.method == 'GET':
        return param.PLEASE_USE_POST


