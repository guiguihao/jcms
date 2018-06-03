#!/usr/bin/python
#-*-coding:utf-8 -*-
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
from yunapp import app, result, connection, request, tool, config, sms
from yunapp.result import *
from yunapp import param
import random

appid = 1400094599
appkey = "d5bb1a67c7ae11ed1c42296f81774711"
template_id = 124494


def sendCode(code,phone_number):
    ssender = SmsSingleSender(appid, appkey)
    phone_number = str(phone_number)
    try:
        result = ssender.send(0, 86, phone_number,
        '你的验证码为：' + code + '，请于5分钟内填写。如非本人操作，请忽略本短信。')
    except HTTPError as e:
        print(e)
    except Exception as e:
        print(e)

    print(result)
    return result['result']



'''
发送验证码
{
   code
   phone_number
}
'''
@app.route('/app/sendCode', methods=['GET', 'POST'])
def send_code():
    if request.method == 'POST':
        appkey = ''
        token = ''
        try:
            token = request.headers[config.AUTHORIZATION]
        except:
            return MyException(param.APP_TOKEN_NULL).toJson()
        data = request.get_json()
        phone_number = ''
        for key in data:
            if data[key] == '':
                continue
            if key == 'phone_number':
                phone_number = data['phone_number']
        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson()
        else:
            resultTooken = tool.ruleToken(token,True)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0]
        if phone_number and phone_number != '':
            try:
                code = str(random.randint(1000, 9999))
                result = sendCode(code,phone_number)
                if result == 0:
                    return MyResult({'code':int(code)<<10}).toJson()
                else:
                    return MyException(param.CODE_ERROR).toJson()
            except Exception as e:
                print  e
                return MyException([param.CHECK_FAILURE[0], unicode(e)]).toJson()
        else:
            return MyException(param.CODE_PHONE_NULL).toJson()

    if request.method == 'GET':
        return param.PLEASE_USE_POST