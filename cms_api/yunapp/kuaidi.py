#!/usr/bin/python
# -*-coding:utf-8 -*-
from yunapp import app, result, connection, request, tool, config
from yunapp.result import *
import urllib, urllib2
import json
from flask import jsonify
'''
获取快递信息
{
   
}
'''

@app.route('/app/getkuaidi', methods=['GET', 'POST'])
def getKuaiDi():
    if request.method == 'POST':
        data = request.get_json()
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
                rsl = kuaidi(data['type'],data['postid'])
                return jsonify(rsl)
            except Exception as e:
                return MyException(param.CHECK_FAILURE).toJson()
        else:
            return MyException(param.REGISTER_FAILURE).toJson()

    if request.method == 'GET':
        return param.PLEASE_USE_POST

def kuaidi(type,postid):
    url = 'https://www.kuaidi100.com/query?'
    textmod = {'type': type, 'postid':postid}
    textmod = urllib.urlencode(textmod)
    req = urllib2.Request(url='%s%s' % (url, textmod))
    res = urllib2.urlopen(req)
    res = res.read()
    return  json.loads(res)

