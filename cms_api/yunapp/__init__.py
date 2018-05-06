#!/usr/bin/python
#-*-coding:utf-8 -*-
from flask import Flask,session,abort
from mongokit import Connection, Document
from yunapp import config
from yunapp import result
from flask import request


app = Flask(__name__)
app.config.from_object(config)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT151fgfg'
# connect to the database
connection = Connection(app.config['MONGODB_HOST'],
                        app.config['MONGODB_PORT'])
app.config['UPLOADS_DEFAULT_DEST'] = app.config['UPLOAD_FOLDER']


app.debug = True

from yunapp import shop
from yunapp import ShopSale
from yunapp import admin
from yunapp import user
from yunapp import Type
from yunapp import appInfo
from yunapp import DeveloperUser
from yunapp import order
from yunapp import LoginAndRegister
from yunapp import Article
from yunapp import ImgManage
from yunapp import ShopReturnInfo
from yunapp import ShopSaleCode
from yunapp import Comment
from yunapp import ReceiveInfo
from yunapp import ShopFenXiao
from yunapp import token
from yunapp import ImgManage2