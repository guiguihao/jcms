#!/usr/bin/python
# -*-coding:utf-8 -*-
from yunapp import app, result, connection, request, tool, config
from yunapp.result import *


'''
校验token
{
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''

@app.route('/app/checktoken/<token>', methods=['GET', 'POST'])
def CheckToken(token):
    if request.method == 'POST':
        print '```````````````````'
        token = request.form['token']
        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson()
        else:
            resultTooken = tool.ruleToken(token)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0]
        if appkey:
            return MySucceedResult().toJson()
        else:
            return MyException(resultTooken).toJson()

    if request.method == 'GET':
        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson()
        else:
            resultTooken = tool.ruleToken(token,False)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0]
        if appkey:
            return MySucceedResult().toJson()
        else:
            return MyException(resultTooken).toJson()


#获取tolen appsecret

@app.route('/app/get/appkeyAndSecret', methods=['GET', 'POST'])
def get_appkeyAndSecret():
    if request.method == 'POST':
        appkey = ''
        token = ''
        try:
            token = request.headers[config.AUTHORIZATION]
        except:
            return MyException(param.APP_TOKEN_NULL).toJson()
        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson()
        else:
            resultTooken = tool.ruleToken(token, True)
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
                    'superadmin':1,
                    'del': 0,
                }
                fnuser = connection.APP_admin.find(params, {'del': 0})
                for user in fnuser:
                    user['_id'] = str(user['_id'])
                    admins['data'].append(user)
                admins['count'] = fnuser.count()
                return MyResult(admins).toJson()
            except Exception as e:
                return MyException(param.CHECK_FAILURE).toJson()
        else:
            return MyException(param.REGISTER_FAILURE).toJson()

    if request.method == 'GET':
        return param.PLEASE_USE_POST