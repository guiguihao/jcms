#!/usr/bin/python
# -*-coding:utf-8 -*-
from yunapp import app, result, connection, request, tool, config, sms
from yunapp.model.ImgModel import *
from yunapp.result import *
from yunapp import param
from bson.objectid import ObjectId
from datetime import datetime

'''
获取图片列表
{
    'pageSize': 10,
    'page':1
    filter = ''
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''


@app.route('/app/img2/list', methods=['GET', 'POST'])
def get_img2s():
    if request.method == 'POST':
        appkey = ''
        token = ''
        try:
            token = request.headers[config.AUTHORIZATION]
        except:
            return MyException(param.APP_TOKEN_NULL).toJson()
        data = request.get_json()
        user = connection.Img2()
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
            fnuser = connection.Img2.find(params, {'del': 0}).limit(pageSize).skip((page - 1) * pageSize).sort(
                [('_id', -1)])
            fdApp = connection.AppInfo.find_one({'appkey': appkey})
            for user in fnuser:
                user['_id'] = str(user['_id'])
                user.date = user.date.strftime('%Y-%m-%d %H:%M:%S')
                user['ourl'] = fdApp.domian  + '/upload/' + user.url
                admins['data'].append(user)
            admins['count'] = fnuser.count()
            return MyResult(admins).toJson()
        except Exception as e:
            print e
            return MyException(param.CHECK_FAILURE).toJson()


    if request.method == 'GET':
        return param.PLEASE_USE_POST


'''
添加图片
{
    'name':'xiaosan', #或phone email
    'password':'11122',
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''


@app.route('/app/img2/add', methods=['GET', 'POST'])
def add_img2():
    if request.method == 'POST':
        user = connection.Img2()
        user.url = request.form['url']
        user.size = request.form['size']
        user.pf = request.form['pf']
        user.userid = request.form['userid']
        user.name = request.form['name']
        token = request.form['token']
        appkey = ''
        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson()
        else:
            resultTooken = tool.ruleToken(token,False)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0]
        if user.url and user.pf:
            try:
                queryImg = connection.Img2.find_one({'url':request.form['url'],'del':0,'appkey':appkey})
                if queryImg:
                    queryImg.url = request.form['url']
                    queryImg.size = request.form['size']
                    queryImg.pf = request.form['pf']
                    queryImg.userid = request.form['userid']
                    queryImg.date = datetime.now()
                    queryImg.save()
                    return MySucceedResult().toJson()
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


@app.route('/app/img2/del', methods=['GET', 'POST'])
def app_img2_update():
    if request.method == 'POST':
        url = request.form['url']
        token = request.form['token']
        appkey = ''
        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson()
        else:
            resultTooken = tool.ruleToken(token,False)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0]
        try:
            user = connection.Img2.find_one({'appkey': appkey, 'url': url,'del':0})
            if user:
                user['del'] = 1
                user.save()
                user['_id'] = str(user['_id'])
                user.date = user.date.strftime('%Y-%m-%d %H:%M:%S')
                return MyResult(user).toJson()
            else:
                return MyException(param.PICTURE_NULL).toJson()
        except Exception as e:
            print e
            return MyException(param.PARAM_FAILURE).toJson()

    if request.method == 'GET':
        return param.PLEASE_USE_POST