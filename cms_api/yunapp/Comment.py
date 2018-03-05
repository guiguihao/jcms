from yunapp import app,result,connection
from yunapp.model.commentModel import *
from yunapp.result import *

'''
添加评论/评价
{
    'pid':'pid'
    'level':1-5
    ''
    ''
    ...
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/comment/add',methods=['GET', 'POST'])
def comment_add():
    if request.method == 'POST':
        data = request.get_json()
        comment = connection.Comment()
        token = ''
        appkey = ''
        for key in data:
            if key == 'pid':
                comment.pid = data['pid']
            if key == 'level':
                comment.level = data['level']
            if key == 'content':
                comment.content = data['content']
            if key == 'token':
                token = data['token']
            if key == 'reserved_1':
                comment.reserved_1 = data['reserved_1']
            if key == 'reserved_2':
                comment.reserved_1 = data['reserved_2']
            if key == 'reserved_3':
                comment.reserved_1 = data['reserved_3']
            if key == 'reserved_4':
                comment.reserved_1 = data['reserved_4']
        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson() 
        else:
            resultTooken = tool.ruleToken(token)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0] 
                comment.appkey = appkey
        if comment.titile and comment.price
            try:
                comment.save()
                return  MySucceedResult().toJson()
            except Exception as e:
                return MyException(param.CHECK_FAILURE).toJson()
        else:
           return MyException(param.REGISTER_FAILURE).toJson()
  
    if request.method == 'GET':
        return param.PLEASE_USE_POST
    

'''
删除评论
{
    'del':'pid'
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/comment/del',methods=['GET', 'POST'])
def comment_del():
    if request.method == 'POST':
        data = request.get_json()
        comment = connection.omment()
        token = ''
        appkey = ''
        for key in data:
            if key == 'del':
                comment.titile = ObjectId data['del']
            if key == 'token':
                token = data['token']
        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson() 
        else:
            resultTooken = tool.ruleToken(token)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0] 
        if comment.titile and comment.price
            try:
                connection.Comment.find_and_modify({'_id':comment['_id'],'del':0},{'$set':{"del":1}})
                return  MySucceedResult().toJson()
            except Exception as e:
                return MyException(param.CHECK_FAILURE).toJson()
        else:
           return MyException(param.REGISTER_FAILURE).toJson()
  
    if request.method == 'GET':
        return param.PLEASE_USE_POST




'''
post 
{
    '_id': 'xxxxxxx',
    set:{
       设置需要更新的字段即可,如下,可多个字段,不能包含_id
       titile : 'xx',
       'price': '' 
    },
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/comment/update',methods=['GET', 'POST'])
def comment_update():
    if request.method == 'POST':
        data = request.get_json()
        token = ''
        appkey = ''
        for key in data:
            if key == '_id':
                data['_id'] = ObjectId(data['_id'])
            if key == 'token':
                token = data['token']
        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson() 
        else:
            resultTooken = tool.ruleToken(token)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0]
        try:
            connection.Comment.find_and_modify({'_id':data['_id'],'appkey':appkey,'del':0},{'$set':data['set']})
            return MyResult(comment).toJson()
        except Exception as e:
            return MyException(param.PARAM_FAILURE).toJson()
            
    if request.method == 'GET':
        return param.PLEASE_USE_POST


'''
获取评论
{
    'pid':'0',  # 'pid':'0' 获取所有评论, 'pid':'_id' 获取某个产品或文章或..评论
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/type/get',methods=['GET', 'POST'])
def type_update():
    if request.method == 'POST':
        data = request.get_json()
        mytype = connection.Comment()
        token = ''
        appkey = ''
        for key in data:
            if key == 'pid':
                mytype['_id'] = data['pid']
            if key == 'token':
                token = data['token']
                del data['token']
    if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson() 
    else:
            resultTooken = tool.ruleToken(token)
            if resultTooken[0] != 1:
                appkey = token.split('&&')[0]
                return MyException(resultTooken).toJson()
            else:
                mytype.appkey = appkey
    try:
          if mytype['_id']:
                cols = ''
                if mytype['_id'] == '0':
                    cols = connection.Comment.find({'appkey':appkey,'del':0})
                else:
                    cols = connection.Comment.find({'appkey':appkey,'del':0,'pid':mytype['_id']})
                return  MyResult(cols).toJson()
          else:
                return MyException(param.PARAM_FAILURE).toJson()
    except Exception as e:
          return MyException(param.PARAM_FAILURE).toJson()
        
  
    if request.method == 'GET':
        return param.PLEASE_USE_POST


