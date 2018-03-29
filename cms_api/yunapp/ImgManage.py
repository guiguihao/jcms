#!/usr/bin/python
# -*-coding:utf-8 -*-
from yunapp import app, result, connection, request, tool, config
from yunapp.result import *
from yunapp import param
from bson.objectid import ObjectId
from datetime import datetime
from flask_uploads import UploadSet, IMAGES, configure_uploads, ALL
import os

files = UploadSet('POTO', ALL)
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
        filename = files.save(request.files['image'])
        print filename
        url = files.url(filename)
        return MySucceedResult().toJson()

    if request.method == 'GET':
        return param.PLEASE_USE_POST