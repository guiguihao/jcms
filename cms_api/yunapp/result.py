#!/usr/bin/python
#-*-coding:utf-8 -*-
from flask import jsonify
from yunapp import param

class MyException:
    '异常提示'
    def __init__(self,param):
        self.param = param
    def toJson(self):
         return jsonify({'code':self.param[0],'msg':self.param[1]})

class MyExceptionWithResult:
    '异常提示+返回值'
    def __init__(self,param,data):
        self.param = param
        self.data = data
    def toJson(self):
         return jsonify({'code':self.param[0],'msg':self.param[1],'data':self.data})


class MySucceedResult:
    '正常提示'
    def toJson(self):
        return jsonify({'code':param.SUCCEED[0],'msg':param.SUCCEED[1]})


    '正常返回'
class MyResult:
    def __init__(self,data):
        self.data = data
    def toJson(self):
         return jsonify({'code':param.SUCCEED[0],'msg':param.SUCCEED[1],'data':self.data})