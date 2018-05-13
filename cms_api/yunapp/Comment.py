#!/usr/bin/python
# -*-coding:utf-8 -*-
from yunapp import app, result, connection, request, tool, config, sms
from yunapp.model.commentModel import *
from yunapp.result import *
from yunapp import param
from bson.objectid import ObjectId
from datetime import datetime

'''
获取评论列表
{
    'pageSize': 10,
    'page':1
    filter = ''
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''


@app.route('/app/comment/list', methods=['GET', 'POST'])
def get_comments():
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
            fnuser = connection.Comment.find(params, {'del': 0}).limit(pageSize).skip((page - 1) * pageSize).sort(
                [('_id', -1)])
            for user in fnuser:
                user['_id'] = str(user['_id'])
                user.date = user.date.strftime('%Y-%m-%d %H:%M:%S')
                author = connection.APP_admin.one({'appkey': appkey, '_id':ObjectId(user['userId'])},
                                                  {'del': 0, 'permission': 0, 'password': 0, 'superadmin': 0, 'vip': 0,
                                                   'appsecret': 0})
                if author:
                    author['_id'] = str(author['_id'])
                    user['user'] = author
                author1 = connection.APP_User.one({'appkey': appkey, '_id':ObjectId(user['userId'])}, {'del': 0})
                if author1:
                    author1['_id'] = str(author1['_id'])
                    user['user'] = author
                admins['data'].append(user)
            admins['count'] = fnuser.count()
            return MyResult(admins).toJson()
        except Exception as e:
            print e
            return MyException(param.CHECK_FAILURE).toJson()


    if request.method == 'GET':
        return param.PLEASE_USE_POST


'''
添加评论
{
    'name':'xiaosan', #或phone email
    'password':'11122',
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''


@app.route('/app/comment/add', methods=['GET', 'POST'])
def add_comment():
    if request.method == 'POST':
        appkey = ''
        token = ''
        try:
            token = request.headers[config.AUTHORIZATION]
        except:
            return MyException(param.APP_TOKEN_NULL).toJson()
        data = request.get_json()
        user = connection.Comment()
        for key in data:
            if data[key] == '':
                continue
            if key == 'oid':
                user.oid = data['oid']
            if key == 'level':
                user.level = data['level']
            if key == 'content':
                user.content = data['content']
            if key == 'imgs':
                user.imgs = data['imgs']
            if key == 'type':
                user.type = data['type']
            if key == 'userId':
                user.userId = data['userId']
            if key == 'answer':
                user.answer = data['answer']
            if key == 'reserved_1':
                user.reserved_1 = data['reserved_1']
            if key == 'reserved_2':
                user.reserved_2 = data['reserved_2']
            if key == 'reserved_3':
                user.reserved_3 = data['reserved_3']
            if key == 'reserved_4':
                user.reserved_4 = data['reserved_4']
        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson()
        else:
            resultTooken = tool.ruleToken(token,True)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0]
        if user.oid and user.content:
            try:
                user.appkey = appkey
                user.date = datetime.now()
                user.save()
                return MySucceedResult().toJson()
            except Exception as e:
                print  e
                return MyException([param.CHECK_FAILURE[0], unicode(e)]).toJson()
        else:
            return MyException(param.ARTICLE_MUST_TITLE_FAILURE).toJson()

    if request.method == 'GET':
        return param.PLEASE_USE_POST


'''
post  更新评论信息
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


@app.route('/app/comment/update', methods=['GET', 'POST'])
def app_comment_update():
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
            user = connection.Comment.find_one({'appkey': appkey, '_id': ObjectId(data['_id'])})
            if user:
                user['del'] = int(user['del'])
                for key in data['set']:
                    if data['set'][key] == '':
                        continue
                    if key == 'oid':
                        user.oid = data['set']['oid']
                    if key == 'level':
                        user.level = data['set']['level']
                    if key == 'content':
                        user.content = data['set']['content']
                    if key == 'imgs':
                        user.imgs = data['set']['imgs']
                    if key == 'del':
                        user['del'] = data['set']['del']
                    if key == 'type':
                        user.type = data['set']['type']
                    if key == 'userId':
                        user.userId = data['set']['userId']
                    if key == 'answer':
                        user.answer = data['set']['answer']
                    if key == 'reserved_1':
                        user.reserved_1 = data['set']['reserved_1']
                    if key == 'reserved_2':
                        user.reserved_2 = data['set']['reserved_2']
                    if key == 'reserved_3':
                        user.reserved_3 = data['set']['reserved_3']
                    if key == 'reserved_4':
                        user.reserved_4 = data['set']['reserved_4']
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