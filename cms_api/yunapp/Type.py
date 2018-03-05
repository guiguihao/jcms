from yunapp import app,result,connection
from yunapp.model.typeModel import *
from yunapp.result import *

'''
添加或修改分类
{
    'name':'xx',
    'parentID':'xxx',  #parentID = 0为1级分类
    'sort':0  
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/type/update',methods=['GET', 'POST'])
def type_update():
    if request.method == 'POST':
        data = request.get_json()
        mytype = connection.Type()
        token = ''
        appkey = ''
        for key in data:
            if key == 'name':
                mytype.name = data['name']
            if key == 'sort':
                mytype.name = data['sort']
            if key == 'parentID':
                mytype.parentID = ObjectId(data['parentID'])
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
          if mytype.name  and mytype.parentID:
                fvip = connection.mytype.find_one({'name':mytype.name,'parentID':mytype.parentID,'appkey':appkey,'del':0})
                if fvip:
                    connection.mytype.find_and_modify({'name':mytype.name,'parentID':mytype.parentID,'appkey':appkey,'del':0},{'$set':data})
                else:
                    mytype.save()
                return  MySucceedResult().toJson()
          else:
                return MyException(param.PARAM_FAILURE).toJson()
    except Exception as e:
          return MyException(param.PARAM_FAILURE).toJson()
        
  
    if request.method == 'GET':
        return param.PLEASE_USE_POST

'''
删除分类
{
    'del':'_id',
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/type/update',methods=['GET', 'POST'])
def type_update():
    if request.method == 'POST':
        data = request.get_json()
        mytype = connection.Type()
        token = ''
        appkey = ''
        for key in data:
            if key == 'del':
                mytype['_id'] =ObjectId(data['del'])
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
          	    pid = mytype['_id'] == '0'?'0':str(mytype['_id'])
                connection.mytype.find_and_modify($or:[{'_id':mytype['_id'],'appkey':appkey,'del':0},{'parentID':pid),'appkey':appkey,'del':0}],{'$set':{'del':1}})
                return  MySucceedResult().toJson()
          else:
                return MyException(param.PARAM_FAILURE).toJson()
    except Exception as e:
          return MyException(param.PARAM_FAILURE).toJson()
        
  
    if request.method == 'GET':
        return param.PLEASE_USE_POST


'''
获取分类
{
    'type':'0',  # 'type':'0' 获取所有分类, 'type':'_id' 获取某个分类
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
}
'''
@app.route('/type/get',methods=['GET', 'POST'])
def type_update():
    if request.method == 'POST':
        data = request.get_json()
        mytype = connection.Type()
        token = ''
        appkey = ''
        for key in data:
            if key == 'type':
                mytype['_id'] = data['type']
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
          	    	cols = connection.mytype.group({key:{'type':true},initial:{'type':[]},reduce: function(cur,prev){prev.type.push({'name':cur.name})},condition:{'appkey':appkey,'del':0}})
                else:
                	cols = connection.mytype.group({key:{'type':true},initial:{'type':[]},reduce: function(cur,prev){prev.type.push({'name':cur.name})},condition:{'appkey':appkey,'del':0}}
                return  MyResult(cols).toJson()
          else:
                return MyException(param.PARAM_FAILURE).toJson()
    except Exception as e:
          return MyException(param.PARAM_FAILURE).toJson()
        
  
    if request.method == 'GET':
        return param.PLEASE_USE_POST

