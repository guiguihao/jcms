#!/usr/bin/python
# -*-coding:utf-8 -*-
from yunapp import app, result, connection, request, tool, config, sms
from yunapp.model.ArticleModel import *
from yunapp.result import *
from yunapp import param
from bson.objectid import ObjectId
from datetime import datetime

'''
获取万能块列表
{
    'pageSize': 10,
    'page':1
    filter = ''
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''


@app.route('/app/wanneng/list', methods=['GET', 'POST'])
def get_wanengs():
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
        sort = '_id'
        for key in data:
            if key == 'pageSize':
                pageSize = data['pageSize']
            if key == 'page':
                page = data['page']
            if key == 'filter':
                filter = data['filter']
            if key == 'sort':
                sort = data['sort']
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
                    'count': 0,
                    'data': [],
                }
                params = {
                    'appkey': appkey,
                    'del': 0,
                }
                if isinstance(filter, dict):
                    for k in filter:
                        params[k] = filter[k]
                        if k == '_id':
                            params[k] = ObjectId(filter[k])
                fnuser = connection.WanNeng.find(params, {'del': 0}).limit(pageSize).skip((page - 1) * pageSize).sort(
                    [(sort, -1)])
                for user in fnuser:
                    user['_id'] = str(user['_id'])
                    user.date = user.date.strftime('%Y-%m-%d %H:%M:%S')
                    admins['data'].append(user)
                admins['count'] = fnuser.count()
                return MyResult(admins).toJson()
            except Exception as e:
                print e
                return MyException(param.CHECK_FAILURE).toJson()
        else:
            return MyException(param.REGISTER_FAILURE).toJson()

    if request.method == 'GET':
        return param.PLEASE_USE_POST


'''
添加万能块
{
    'name':'xiaosan', #或phone email
    'password':'11122',
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''


@app.route('/app/wanneng/add', methods=['GET', 'POST'])
def add_wanneng():
    if request.method == 'POST':
        appkey = ''
        token = ''
        try:
            token = request.headers[config.AUTHORIZATION]
        except:
            return MyException(param.APP_TOKEN_NULL).toJson()
        data = request.get_json()
        user = connection.WanNeng()
        for key in data:
            if data[key] == '':
                continue
            if key == 'w1':
                user.w1 = data['w1']
            if key == 'w2':
                user.w2 = data['w2']
            if key == 'w3':
                user.w3 = data['w3']
            if key == 'w4':
                user.w4 = data['w4']
            if key == 'w5':
                user.w5 = data['w5']
            if key == 'w6':
                user.w6 = data['w6']
            if key == 'w7':
                user.w7 = data['w7']
            if key == 'w8':
                user.w8 = data['w8']
            if key == 'w9':
                user.w9 = data['w9']
            if key == 'w10':
                user.w10 = data['w10']
            if key == 'w11':
                user.w11 = data['w11']
            if key == 'w12':
                user.w12 = data['w12']
            if key == 'w13':
                user.w13 = data['w13']
            if key == 'w14':
                user.w14 = data['w14']
            if key == 'w15':
                user.w15 = data['w15']
            if key == 'w16':
                user.w16 = data['w16']
            if key == 'w17':
                user.w17 = data['w17']

        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson()
        else:
            resultTooken = tool.ruleToken(token,True)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0]
        if appkey:
            user.appkey = appkey
            user.date = datetime.now()
            user.save()
            return MySucceedResult().toJson()
        else:
            return MyException(param.ARTICLE_MUST_TITLE_FAILURE).toJson()

    if request.method == 'GET':
        return param.PLEASE_USE_POST


'''
post  更新万能信息
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


@app.route('/app/wanneng/update', methods=['GET', 'POST'])
def app_wanneng_update():
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
            user = connection.WanNeng.find_one({'appkey': appkey, '_id': ObjectId(data['_id'])})
            if user:
                user['del'] = int(user['del'])
                for key in data['set']:
                    if data['set'][key] == '':
                        continue
                    if key == 'w1':
                        user.w1 = data['set']['w1']
                    if key == 'w2':
                        user.w2 = data['set']['w2']
                    if key == 'w3':
                        user.w3 = data['set']['w3']
                    if key == 'w4':
                        user.w4 = data['set']['w4']
                    if key == 'w5':
                        user.w5 = data['set']['w5']
                    if key == 'w6':
                        user.w6 = data['set']['w6']
                    if key == 'w7':
                        user.w7 = data['set']['w7']
                    if key == 'w8':
                        user.w8 = data['set']['w8']
                    if key == 'w9':
                        user.w9 = data['set']['w9']
                    if key == 'w10':
                        user.w10 = data['set']['w10']
                    if key == 'w11':
                        user.w11 = data['set']['w11']
                    if key == 'w12':
                        user.w12 = data['set']['w12']
                    if key == 'w13':
                        user.w13 = data['set']['w13']
                    if key == 'w14':
                        user.w14 = data['set']['w14']
                    if key == 'w15':
                        user.w15 = data['set']['w15']
                    if key == 'w16':
                        user.w16 = data['set']['w16']
                    if key == 'w17':
                        user.w17 = data['set']['w17']
                    if key == 'del':
                        user['del'] = data['set']['del']
                user.save()
                user['_id'] = str(user['_id'])
                user.date = user.date.strftime('%Y-%m-%d %H:%M:%S')
                return MyResult(user).toJson()
            else:
                return MyException(param.ARTICLE_NULL).toJson()
        except Exception as e:
            print e
            return MyException(param.PARAM_FAILURE).toJson()

    if request.method == 'GET':
        return param.PLEASE_USE_POST