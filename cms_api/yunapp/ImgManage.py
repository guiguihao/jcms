#!/usr/bin/python
# -*-coding:utf-8 -*-
from yunapp import app, result, connection, request, tool, config
from yunapp.result import *
from yunapp import param
from bson.objectid import ObjectId
from datetime import datetime
from flask_uploads import UploadSet, IMAGES, configure_uploads, ALL
import os

files = UploadSet('image', ALL)
configure_uploads(app, files)

'''
获取文章列表
{
    'pageSize': 10,
    'page':1
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in config.ALLOWED_EXTENSIONS

@app.route('/app/save/img', methods=['GET', 'POST'])
def save_img():
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
            filename = files.save(request.files['image'])
            url = files.url(filename)
            return MyResult({'url':url}).toJson()
        else:
            return MyException(resultTooken).toJson()

    if request.method == 'GET':
        return param.PLEASE_USE_POST


@app.route('/app/save/img2', methods=['GET', 'POST'])
def save_img2():
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
            filename = files.save(request.files['file'])
            url = files.url(filename)
            return MyResult({'url':url}).toJson()
        else:
            return MyException(resultTooken).toJson()

    if request.method == 'GET':
        return param.PLEASE_USE_POST

@app.route('/app/del/img', methods=['GET', 'POST'])
def del_img():
    if request.method == 'POST':
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
            imgname = request.form['imgname']
            if imgname:
                filename = config.UPLOAD_FOLDER + '/image/' + request.form['imgname']
                delFile = os.path.join(filename)
                if os.path.exists(delFile):
                    os.remove(delFile)
                    return MySucceedResult().toJson()
                else:
                    return MyException(param.FILE_DEl_FAILURE).toJson()
            else:
                MyException(param.PARAM_FAILURE).toJson()
        else:
            return MyException(resultTooken).toJson()

    if request.method == 'GET':
        return param.PLEASE_USE_POST