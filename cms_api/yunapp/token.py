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
