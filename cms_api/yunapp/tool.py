#!/usr/bin/python
#-*-coding:utf-8 -*-
from yunapp import abort,session,config
from yunapp.model.userModel import *
import hashlib
import os
import time
from yunapp import connection,Document
from yunapp import param
import pytz
from datetime import datetime


def useSession(appkey):
    appinfo = connection.AppInfo.find_one({'appkey': appkey})
    if appinfo and appinfo.session == 1:
        if config.SESSION_KEY in session:
            if session[config.SESSION_KEY]:
                pass
            else:
                return abort(401)
        else:
            return abort(401)
    if not appinfo:
        return abort(401)

def md5(str):
    m = hashlib.md5()   
    m.update(str)
    return m.hexdigest()

def randomString(n):
    return ''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(n)))[0:16]


def ruleToken(token,issession):
        tokenParams = token.split('&&')
        user = connection.APP_admin.find_one({"appkey":tokenParams[0],"superadmin":1})
        if issession:
            useSession(tokenParams[0])
        if not user:
            return param.APP_TOKEN_ERROR
        timeStamp = time.time()
        tktime = float(tokenParams[1])
        tkmd5 = tokenParams[2]
        if timeStamp-tktime <= 9000000 and timeStamp-tktime >= -9000000:
            if tkmd5 == md5(user.appsecret+'&&'+tokenParams[1]):
                return param.SUCCEED
            else:
                  return param.APP_TOKEN_RULE_ERROR
        else:
            return param.APP_TOKEN_TIME_ERROR

def ruleToken2(token,pw,md5key):
        timeStamp = time.time()
        tokenParams = token.split('&&')
        tktime = float(tokenParams[0])
        tkmd5 = tokenParams[1]
        print token,pw,md5key
        print tkmd5
        if timeStamp-tktime <= 900000 and timeStamp-tktime >= -900000:
            if tkmd5 == md5(pw + '&&' + md5key + tokenParams[0]):
                return param.SUCCEED
            else:
                  return param.APP_TOKEN_RULE_ERROR
        else: 
            return param.APP_TOKEN_TIME_ERROR

# UTCS时间转换为时间戳 2016-07-31T16:00:00Z
def utc_to_local(utc_time_str, utc_format='%Y-%m-%dT%H:%M:%S.%fZ'):
    local_tz = pytz.timezone('Asia/Chongqing')
    local_format = "%Y-%m-%d %H:%M"
    utc_dt = datetime.strptime(utc_time_str, utc_format)
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    time_str = local_dt.strftime(local_format)
    return int(time.mktime(time.strptime(time_str, local_format)))

# UTCS时间转换为本地时间 2016-07-31T16:00:00Z
def utc_to_localtime(utc_time_str, utc_format='%Y-%m-%dT%H:%M:%S.%fZ'):
    local_tz = pytz.timezone('Asia/Chongqing')
    local_format = "%Y-%m-%d %H:%M"
    utc_dt = datetime.strptime(utc_time_str, utc_format)
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    time_str = local_dt.strftime(local_format)
    return time_str
