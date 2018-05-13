#!/usr/bin/python
#-*-coding:utf-8 -*-
from yunapp import app,result,connection,request,tool,config,sms
from yunapp.model.shopModel import *
from yunapp.model.userModel import *
from yunapp.result import *
from yunapp import param
from bson.objectid import ObjectId


'''
获取管理员列表
{
    'pageSize': 10,
    'page':1
    filter = ''
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/app/admin/list',methods=['GET', 'POST'])
def get_admins():
    if request.method == 'POST':
        appkey = ''
        token = ''
        try:
            token = request.headers[config.AUTHORIZATION]
        except:
            return MyException(param.APP_TOKEN_NULL).toJson()
        data = request.get_json()
        user = connection.APP_admin()
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
                if isinstance(filter, dict):
                    for k in filter:
                        params[k] = filter[k]
                fnuser = connection.APP_admin.find(params,{'active':0,'appsecret':0,'del':0}).limit(pageSize).skip((page-1)*pageSize)
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
添加管理员
{
    'name':'xiaosan', #或phone email
    'password':'11122',
    'permission':()
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/app/admin/add',methods=['GET', 'POST'])
def add_admin():
    if request.method == 'POST':
        appkey = ''
        token = ''
        try:
            token = request.headers[config.AUTHORIZATION]
        except:
            return MyException(param.APP_TOKEN_NULL).toJson()
        data = request.get_json()
        user = connection.APP_admin()
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
            if key == 'icon':
                user.icon = data['icon']
            if key == 'info':
                user.info = data['info']
            if key == 'permission':
                user.permission = data['permission']
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

        if (user.name or user.phone or user.email) and user.password:
            try:
                try:
                    fnuser = connection.APP_admin.find_one({'name':user.name,'del':0})
                    if fnuser: 
                        if fnuser.name: return MyException(param.USER_NAME_FAILURE).toJson()
                    
                    feuser = connection.APP_admin.find_one({'email':user.email,'del':0})
                    if feuser: 
                        if feuser.email: return MyException(param.USER_EMAIL_FAILURE).toJson()

                    fpuser = connection.APP_admin.find_one({'phone':user.phone,'del':0})
                    #print fpuser
                    if fpuser:
                        if fpuser.phone: return MyException(param.USER_PHONE_FAILURE).toJson()
                except Exception, e:
                    pass
                user.password = unicode(tool.md5(user.password))
                user.appkey = appkey
                user.active = 1
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
@app.route('/app/admin/update',methods=['GET', 'POST'])
def app_update():
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
            user = connection.APP_admin.find_one({'appkey':appkey,'_id':ObjectId(data['_id'])})
            user['del'] = int(user['del'])

            for key in data['set']:
                if key == 'name':
                    user.password = data['set']['password']
                if key == 'phone':
                    user.phone = data['set']['phone']
                if key == 'email':
                    user.email = data['set']['email']
                if key == 'qq':
                    user.qq = data['set']['qq']
                if key == 'wachat':
                    user.wachat = data['set']['wachat']
                if key == 'nickname':
                    user.nickname = data['set']['nickname']
                if key == 'icon':
                    user.icon = data['set']['icon']
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


'''
添加或修改vip类型
{
    'level':0,
    'level_name':'一级会员',
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/user/vip/type/add',methods=['GET', 'POST'])
def user_vip_add():
    if request.method == 'POST':
        appkey = ''
        token = ''
        try:
            token = request.headers[config.AUTHORIZATION]
        except:
            return MyException(param.APP_TOKEN_NULL).toJson()
        data = request.get_json()
        userVip = connection.UserVip()
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
        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson()
        else:
            resultTooken = tool.ruleToken(token,True)
            appkey = token.split('&&')[0]
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                userVip.appkey = appkey
        try:
              del data['token']
              if userVip.level >-1 and userVip.level_name:
                    fvip = connection.UserVip.find_one({'level_name':userVip.level_name,'appkey':appkey})
                    if fvip:
                        return MyException(param.APP_VIPTYPE_NAME_FAILURE).toJson()
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
@app.route('/user/vip/type',methods=['GET', 'POST'])
def user_vip_get_all_viptype():
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
更新 vip
{
    set:{
       '_id':xx,  #vipid
       level_name : 'xx',
       "del":1  #删除
    },
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/user/vip/type/set',methods=['GET', 'POST'])
def user_vip_set():
    if request.method == 'POST':
        token = ''
        appkey = ''
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
                vipId = data['set']['_id']
                if len(vipId)<0:
                    return MyException(param.PARAM_FAILURE).toJson()
                user = connection.UserVip.find_one({'_id':ObjectId(vipId)})
                if user:
                    user['del'] = int(user['del'])
                    for key in data['set']:
                        if key == 'level':
                            user.level = data['set']['level']
                        if key == 'level_name':
                            user.level_name = data['set']['level_name']
                        if key == 'level_dec':
                            user.level_dec = data['set']['level_dec']
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
                    # connection.APP_admin.find_and_modify({'appkey':appkey,'del':0},{'$set':data['set']})
                    # user = connection.APP_admin.find_one({'appkey':appkey,'del':0},{'del':0,'appsecret':0})
                    user['_id'] = str(user['_id'])
                    return MyResult(user).toJson()
                else:
                    MyException(param.USER_VIP_FAILURE).toJson()
        except Exception as e:
              return MyException(param.PARAM_FAILURE).toJson()
    if request.method == 'GET':
        return param.PLEASE_USE_POST
