#!/usr/bin/python
#-*-coding:utf-8 -*-
from flask import Flask
from mongokit import Connection, Document
from yunapp import config
from yunapp import result
from flask import request


app = Flask(__name__)
app.config.from_object(config)

# connect to the database
connection = Connection(app.config['MONGODB_HOST'],
                        app.config['MONGODB_PORT'])
app.config['UPLOADS_DEFAULT_DEST'] = app.config['UPLOAD_FOLDER']


app.debug = True

from yunapp import shop
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
