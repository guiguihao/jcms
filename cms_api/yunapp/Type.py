#!/usr/bin/python
#-*-coding:utf-8 -*-
from yunapp import app,result,connection,request,tool,config,sms
from yunapp.model.userModel import *
from yunapp.result import *
from yunapp import param
from bson.objectid import ObjectId
from datetime import datetime



'''
获取类型列表
{
    "type":"user", #article', u'shop', u'user'
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/app/type/list',methods=['GET', 'POST'])
def get_vips():
    if request.method == 'POST':
        data = request.get_json()
        mtype = ''
        appkey = ''
        for key in data:
            if key == 'token':
                token = data['token']
            if key == 'type':
                mtype = data['type']
        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson() 
        else:
            resultTooken = tool.ruleToken(token)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0]
        if appkey and mtype != '':
            try:
                types = []
                fnuser = connection.Type.find({'appkey':appkey,'del':0,'parentID':'','type':mtype},{'del':0})
                queryChildrenType(fnuser,types)
                return MyResult(types).toJson()
            except Exception as e:
                print e
                return MyException(param.CHECK_FAILURE).toJson()
        else:
           return MyException(param.PARAM_FAILURE).toJson()
  
    if request.method == 'GET':
        return param.PLEASE_USE_POST

def queryChildrenType(types,lists):
    for user in types:
        admins = {
           'type':'',
            'children':[],
        }
        user['_id'] = str(user['_id'])
        user.date = user.date.strftime('%Y-%m-%d %H:%M:%S')
        admins['type'] = user
        childrenTypes = connection.Type.find({'del':0,'parentID':user['_id']},{'del':0})
        lists.append(admins)
        queryChildrenType(childrenTypes,admins['children'])

      

'''
用户注册/添加
{
    'level':11
    'name':'11122',
    'dec':'11',
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/app/type/add',methods=['GET', 'POST'])
def add_vip():
    if request.method == 'POST':
        data = request.get_json()
        user = connection.Type()
        appkey = ''
        token = ''
        for key in data:
            if data['set'] == '':
                continue
            if key == 'level':
                user.level = data['level']
            if key == 'name':
                user.name = data['name']
            if key == 'dec':
                user.dec = data['dec']
            if key == 'parentID':
                user.parentID = data['parentID']
            if key == 'type':
                user.type = data['type']
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

        if user.name and user.type:
            try:
                try:
                    fnuser = connection.Type.find_one({'appkey':appkey,'name':user.name,'del':0})
                    if fnuser: 
                        if fnuser.name: return MyException(param.USER_VIP_REPEAT_FAILURE).toJson()
                except Exception, e:
                    pass
                user.appkey = appkey
                user.save()
                return  MySucceedResult().toJson()
            except Exception as e:
                print e
                return MyException(param.CHECK_FAILURE).toJson()
        else:
           return MyException(param.PARAM_FAILURE).toJson()
  
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
@app.route('/app/type/update',methods=['GET', 'POST'])
def app_vip_update():
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
            user = connection.Type.find_one({'appkey':appkey,'_id':ObjectId(data['_id'])})
            if user:
                user['del'] = int(user['del'])
                for key in data['set']:
                    if data['set'][key] == '':
                        continue
                    if key == 'parentID':
                        user.parentID = data['set']['parentID']
                    if key == 'level':
                        user.level = data['set']['level']
                    if key == 'name':
                        user.name = data['set']['name']
                    if key == 'dec':
                        user.dec = data['set']['dec']
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
                user['_id'] = str(user['_id'])
                return MyResult(user).toJson()
            else:
                return MyException(param.USER_VIP_FAILURE).toJson()
            
        except Exception as e:
            print e
            return MyException(param.PARAM_FAILURE).toJson()
            
    if request.method == 'GET':
        return param.PLEASE_USE_POST