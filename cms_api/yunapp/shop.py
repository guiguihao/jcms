#!/usr/bin/python
#-*-coding:utf-8 -*-
from yunapp import app,result,connection,request,tool,config,sms
from yunapp.model.shopModel import *
from yunapp.result import *
from yunapp import param
from bson.objectid import ObjectId
from datetime import datetime


'''
获取文章列表
{
    'pageSize': 10,
    'page':1
    filter = ''
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''

def getSubTypes(appkey,parentId,types):
     types.append(parentId)
     ftype = connection.Type.find({'appkey': appkey, 'del': 0, 'parentID': parentId}, {'del': 0})
     for mtype in ftype:
         mtypeid = str(mtype['_id'])
         getSubTypes(appkey,mtypeid,types)


@app.route('/app/product/list', methods=['GET', 'POST'])
def get_products():
    if request.method == 'POST':
        appkey = ''
        token = ''
        try:
            token = request.headers[config.AUTHORIZATION]
        except:
            return MyException(param.APP_TOKEN_NULL).toJson()
        data = request.get_json()
        pageSize = 50
        page = 1
        filter = ''
        for key in data:
            if key == 'token':
                token = data['token']
            if key == 'pageSize':
                pageSize = data['pageSize']
            if key == 'page':
                page = data['page']
            if key == 'filter':
                filter = data['filter']
        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson()
        else:
            resultTooken = tool.ruleToken(token,True)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0]

        if appkey:
            try:
                typeid = ''
                types = []
                admins = {
                    'count': 0,
                    'data': [],
                }
                params = {
                    'appkey': appkey,
                    'del': 0,
                }
                if isinstance(filter, dict):
                    for k in filter:
                        if k == 'type':
                            typeid = filter[k]
                        else:
                            params[k] = filter[k]
                            if k == '_id':
                                params[k] = ObjectId(filter[k])
                if (len(typeid)>0):
                    getSubTypes(appkey,typeid,types)
                if(len(types)>0):
                    params['type'] = {'$in':types}
                fnuser = connection.Product.find(params,{'del':0}).limit(pageSize).skip((page - 1) * pageSize).sort(
                    [('_id', -1)])
                for user in fnuser:
                    user['_id'] = str(user['_id'])
                    user.date = user.date.strftime('%Y-%m-%d %H:%M:%S')
                    type = connection.Type.one({'appkey': appkey, '_id': ObjectId(user['type'])}, {'del': 0})
                    if type:
                        type['_id'] = str(type['_id'])
                        user.type = type
                        type.date = type.date.strftime('%Y-%m-%d %H:%M:%S')
                    recommendID = ObjectId(user['recommend'])
                    recommend = connection.Type.one({'appkey': appkey, '_id': recommendID},
                                                      {'del': 0, 'date':0})
                    if recommend:
                        recommend['_id'] = str(recommend['_id'])
                        user.recommend = recommend
                    authorId = ObjectId(user['author'])
                    author = connection.APP_admin.one({'appkey': appkey, '_id': authorId}, {'del': 0,'permission':0,'password':0,'superadmin':0,'vip':0,'appsecret':0})
                    if author:
                        author['_id'] = str(author['_id'])
                        user.author = author
                    author1 = connection.APP_User.one({'appkey': appkey, '_id': authorId}, {'del': 0})
                    if author1:
                        author1['_id'] = str(author1['_id'])
                        user.author = author1
                    admins['data'].append(user)
                admins['count'] = fnuser.count()
                return MyResult(admins).toJson()
            except Exception as e:
                print e
                return MyException(param.CHECK_FAILURE).toJson()
        else:
            return MyException(param.REGISTER_FAILURE).toJson()

    if request.method == 'GET':
        return param.PLEASE_USE_POST


'''
添加文章
{
    'name':'xiaosan', #或phone email
    'password':'11122',
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''


@app.route('/app/product/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        appkey = ''
        token = ''
        try:
            token = request.headers['Authorization']
        except:
            return MyException(param.APP_TOKEN_NULL).toJson()
        data = request.get_json()
        user = connection.Product()
        for key in data:
            if data[key] == '':
                continue
            if key == 'title':
                user.title = data['title']
            if key == 'price':
                user.price = data['price']
            if key == 'costprice':
                user.costprice = data['costprice']
            if key == 'overview':
                user.overview = data['overview']
            if key == 'sale':
                user.sale = data['sale']
            if key == 'colour':
                user.colour = data['colour']
            if key == 'size':
                user.size = data['size']
            if key == 'repertory':
                user.repertory = data['repertory']
            if key == 'type':
                user.type = data['type']
            if key == 'imgs':
                user.imgs = data['imgs']
            if key == 'describe':
                user.describe = data['describe']
            if key == 'recommend':
                user.recommend = data['recommend']
            if key == 'buycount':
                user.buycount = data['buycount']
            if key == 'author':
                user.author = data['author']
            if key == 'status':
                user.status = data['status']
            if key == 'reserved_1':
                user.reserved_1 = data['reserved_1']
            if key == 'reserved_2':
                user.reserved_2 = data['reserved_2']
            if key == 'reserved_3':
                user.reserved_3 = data['reserved_3']
            if key == 'reserved_4':
                user.reserved_4 = data['reserved_4']

        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson()
        else:
            resultTooken = tool.ruleToken(token,True)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0]
        if user.title:
            try:
                try:
                    if user.author:
                       fnuser1 = connection.APP_admin.find_one({'appkey': appkey, '_id': ObjectId(user.author), 'del': 0})
                       fnuser2 = connection.APP_User.find_one({'appkey': appkey, '_id': ObjectId(user.author), 'del': 0})
                       if not fnuser1 and not fnuser2:
                             return MyException(param.PRODUCT_AUTHOR_NULL).toJson()
                except Exception, e:
                    return MyException(param.CHECK_FAILURE).toJson()
                user.appkey = appkey
                user.date = datetime.now()
                user.save()
                return MySucceedResult().toJson()
            except Exception as e:
                print  e
                return MyException(param.CHECK_FAILURE).toJson()
        else:
            return MyException(param.ARTICLE_MUST_TITLE_FAILURE).toJson()

    if request.method == 'GET':
        return param.PLEASE_USE_POST


'''
post  更新用户信息
{
    '_id':'xxx'
    set:{
       设置需要更新的字段即可,如下,可多个字段,不能包含_id
       name : 'xx',
       'vip': 'vip类型_id', #通过获取所有vip类型可以获取_id  /user/vip/type/get 
    },
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''


@app.route('/app/product/update', methods=['GET', 'POST'])
def app_product_update():
    if request.method == 'POST':
        appkey = ''
        token = ''
        try:
            token = request.headers['Authorization']
        except:
            return MyException(param.APP_TOKEN_NULL).toJson()
        data = request.get_json()
        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson()
        else:
            resultTooken = tool.ruleToken(token,True)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0]
        try:
            user = connection.Product.find_one({'appkey': appkey, '_id': ObjectId(data['_id'])})
            if user:
                user['del'] = int(user['del'])
                for key in data['set']:
                    if data['set'][key] == '':
                        continue
                    if key == 'title':
                        user.title = data['set']['title']
                    if key == 'price':
                        user.price = data['set']['price']
                    if key == 'costprice':
                        user.costprice = data['set']['costprice']
                    if key == 'overview':
                        user.overview = data['set']['overview']
                    if key == 'type':
                        user.type = data['set']['type']
                    if key == 'colour':
                        user.colour = data['set']['colour']
                    if key == 'size':
                        user.size = data['set']['size']
                    if key == 'repertory':
                        user.repertory = data['set']['repertory']
                    if key == 'imgs':
                        user.imgs = data['set']['imgs']
                    if key == 'describe':
                        user.describe = data['set']['describe']
                    if key == 'recommend':
                        user.recommend = data['set']['recommend']
                    if key == 'buycount':
                        user.buycount = data['set']['buycount']
                    if key == 'author':
                        user.author = data['set']['author']
                    if key == 'status':
                        user.status = data['set']['status']
                    if key == 'reserved_1':
                        user.reserved_1 = data['set']['reserved_1']
                    if key == 'reserved_2':
                        user.reserved_2 = data['set']['reserved_2']
                    if key == 'reserved_3':
                        user.reserved_3 = data['set']['reserved_3']
                    if key == 'reserved_4':
                        user.reserved_4 = data['set']['reserved_4']
                    if key == 'del':
                        user['del'] = data['set']['del']
                user.save()
                user['_id'] = str(user['_id'])
                user.date = user.date.strftime('%Y-%m-%d %H:%M:%S')
                return MyResult(user).toJson()
            else:
                return MyException(param.PRODUCT_NULL).toJson()
        except Exception as e:
            print e
            return MyException(param.PARAM_FAILURE).toJson()

    if request.method == 'GET':
        return param.PLEASE_USE_POST








