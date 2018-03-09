#!/usr/bin/python
#-*-coding:utf-8 -*-
import hashlib
import os
import time
from yunapp import connection,Document
from yunapp import param

def md5(str):
    m = hashlib.md5()   
    m.update(str)
    return m.hexdigest()

def randomString(n):
	return ''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(n)))[0:16]


def ruleToken(token):
        tokenParams = token.split('&&')
        user = connection.APP_admin.find_one({"appkey":tokenParams[0]})
        if not user:
            return param.APP_TOKEN_ERROR
    	timeStamp = time.time()
        tktime = float(tokenParams[1])
        tkmd5 = tokenParams[2]
        if timeStamp-tktime <= 90000 and timeStamp-tktime >= -90000:
        	if tkmd5 == md5(user.appsecret+'&&'+tokenParams[1]):
        		return param.SUCCEED
        	else:
                  return param.APP_TOKEN_RULE_ERROR
        else: 
        	return param.APP_TOKEN_TIME_ERROR


