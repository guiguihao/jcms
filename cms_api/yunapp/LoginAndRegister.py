#!/usr/bin/python
#-*-coding:utf-8 -*-
from yunapp import app,result,connection,request,tool,config,sms,session
from yunapp.model.shopModel import *
from yunapp.model.userModel import *
from yunapp.result import *
from yunapp import param
from bson.objectid import ObjectId



'''
注册用户,可以用户名,邮箱,手机号码注册, 密码必填选项
{
    'name':'xiaosan', #或phone email
    'password':'11122'
    'token':'timestamp&&md5(timestamp && config.DEVELOPER_APPKEY)'
}
'''
@app.route('/app/register',methods=['GET', 'POST'])
def app_register():
    if request.method == 'POST':
        data = request.get_json()
        user = connection.APP_admin()
        tokenMd5 = ''
        timestamp = ''
        for key in data:
            if key == 'name':
                user.name = data['name']
            if key == 'password':
                user.password = data['password']
            if key == 'phone':
                user.phone = data['phone']
            if key == 'email':
                user.email = data['email']
            if key == 'qq':
                user.qq = data['qq']
            if key == 'wachat':
                user.wachat = data['wachat']
            if key == 'nickname':
                user.nickname = data['nickname']
            if key == 'info':
                user.info = data['info']
            if key == 'permission':
                user.permission = data['permission']
            if key == 'token':
                token = data['token']
                tokenParams = token.split('&&')
                tokenMd5 = tokenParams[1]
                timestamp = tokenParams[0]
            if key == 'reserved_1':
                user.reserved_1 = data['reserved_1']
            if key == 'reserved_2':
                user.reserved_1 = data['reserved_2']
            if key == 'reserved_3':
                user.reserved_1 = data['reserved_3']
            if key == 'reserved_4':
                user.reserved_1 = data['reserved_4']

        mymd5 = tool.md5(timestamp + '&&' + config.DEVELOPER_APPKEY)
        if tokenMd5 != tool.md5(timestamp + '&&' + config.DEVELOPER_APPKEY):
            return MyException(param.APP_TOKEN_ERROR).toJson()

        if (user.name or user.phone or user.email) and user.password:
            try:
                try:
                    if user.name:
                        fnuser = connection.APP_admin.find_one({'name':user.name,'del':0})
                        if fnuser:
                            if fnuser.name: return MyException(param.USER_NAME_FAILURE).toJson()
                    if user.email:
                        feuser = connection.APP_admin.find_one({'email':user.email,'del':0})
                        if feuser:
                            if feuser.email: return MyException(param.USER_EMAIL_FAILURE).toJson()
                    if user.phone:
                        fpuser = connection.APP_admin.find_one({'phone':user.phone,'del':0})
                        #print fpuser
                        if fpuser:
                            if fpuser.phone: return MyException(param.USER_PHONE_FAILURE).toJson()
                except Exception, e:
                    pass
                user.password = unicode(tool.md5(user.password))
                # user.appkey = user['_id']
                user.appsecret = unicode(tool.randomString(16),'utf-8')
                user.permission = (1,1,1,1,1,1,1,1)
                user.superadmin = 1
                user.save()
                connection.APP_admin.find_and_modify(user,{'$set':{"appkey":str(user['_id'])}})
                
                #设置应用信息
                appinfo = connection.AppInfo()
                appinfo.appkey = unicode(user['_id'])
                appinfo.status = 1
                appinfo.save()

                userVip = connection.UserType.find({'appkey':str(user['_id']),'del':0}).sort('level',1)
                if userVip.count()>0:
                    for vip in userVip:
                        if(userVip): connection.APP_admin.find_and_modify({'_id':str(user['_id']),'del':0},{'$set':{"vip":str(userVip['_id'])}})
                return  MySucceedResult().toJson()
            except Exception as e:
                print e
                return MyException(param.CHECK_FAILURE).toJson()
        else:
           return MyException(param.REGISTER_FAILURE).toJson()
  
    if request.method == 'GET':
        return param.PLEASE_USE_POST


'''
app管理员激活
get方式 /app/activate/<userid>
'''
@app.route('/app/activate/<userid>',methods=['GET'])
def app_active(userid):
    if request.method == 'GET':
        fnuser = connection.APP_admin.find_one({'_id':ObjectId(userid),'del':0})
        if fnuser:
            if fnuser.active == 1:
                return  MyException(param.APP_ACTIVE_ED_FAILURE).toJson()
            else:
                fnuser.active =1
                fnuser.save()
                return  MySucceedResult().toJson()
        else:
            return  MyException(param.APP_USER_NULL).toJson()

'''
支持用户名 手机号码  邮箱登陆
{
    'name':'xxx',
    'password':'xxxxx',  #md5(密码)
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
    { "_id" : ObjectId("5aa0e1ba4683e6051152f780"), "name" : "admin", "password" : "7fef6171469e80d32c0559f88b377245", "appkey" : "5aa0e1ba4683e6051152f780", "appsecret" : "jjjjddjjdjd", "del" : 0 }
}
'''
@app.route('/admin/login',methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        token = ''
        appkey = ''
        try:
            token = request.headers[config.AUTHORIZATION]
        except:
            return MyException(param.APP_TOKEN_NULL).toJson()
        data = request.get_json()
        user = connection.APP_admin()
        try:
            for key in data:
                if key == 'name':
                    user.name = data['name']
                if key == 'password':
                    user.password = data['password']
                if key == 'phone':
                    user.phone = data['phone']
                if key == 'email':
                    user.email = data['email']
                if key == 'qq':
                    user.qq = data['qq']
                if key == 'wachat':
                    user.wachat = data['wachat']
        except Exception, e:
            return MyException(param.PARAM_FAILURE).toJson() 
        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson() 
        else:
            resultTooken = tool.ruleToken(token,False)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0]
        # print user
        if (user.name or user.phone or user.email or user.qq or user.wachat) and user.password:
            myuser = ''
            if user.name:
                 myuser = connection.APP_admin.find_one({'appkey':appkey,'name':user.name,'del':0},{'userTypes':0,'appsecret':0,'del':0,})
            if user.phone:
                 myuser = connection.APP_admin.find_one({'appkey':appkey,'phone':user.phone,'del':0},{'userTypes':0,'appsecret':0,'del':0,})
            if user.email:
                 myuser = connection.APP_admin.find_one({'appkey':appkey,'email':user.email,'del':0},{'userTypes':0,'appsecret':0,'del':0,})
            if myuser and myuser['password'] == user['password']:
                myuser['_id'] = str(myuser['_id'])
                myuser.pop('password')
                if myuser.active != 1:
                    return MyExceptionWithResult(param.APP_ACTIVE_ERROR,myuser).toJson()
                # user['_id'] = str(user['_id'])
                # userVip = connection.UserVip.find_one({'appkey':appkey,'del':0},({'del':-1})
                # myuser.vip = userVip
                session[config.SESSION_KEY] = appkey
                return  MyResult(myuser).toJson()
            else:
                return  MyException(param.LONGIN_FAILURE).toJson()
        else:
            return      MyException(param.PARAM_FAILURE).toJson()
    if request.method == 'GET':
        return param.PLEASE_USE_POST

'''
退出
{
    'name':'xxx',
    'password':'xxxxx',  #md5(密码)
    'token':'appkey&&timestamp&&md5(appsecret&&timestamp)'
    { "_id" : ObjectId("5aa0e1ba4683e6051152f780"), "name" : "admin", "password" : "7fef6171469e80d32c0559f88b377245", "appkey" : "5aa0e1ba4683e6051152f780", "appsecret" : "jjjjddjjdjd", "del" : 0 }
}
'''
@app.route('/admin/logout',methods=['GET', 'POST'])
def admin_logout():
    if request.method == 'POST':
        token = ''
        appkey = ''
        try:
            token = request.headers[config.AUTHORIZATION]
        except:
            return MyException(param.APP_TOKEN_NULL).toJson()
        if token == '' or not token:
            return MyException(param.APP_TOKEN_NULL).toJson()
        else:
            resultTooken = tool.ruleToken(token,True)
            if resultTooken[0] != 1:
                return MyException(resultTooken).toJson()
            else:
                appkey = token.split('&&')[0]
        # print user
        session.pop(config.SESSION_KEY, None)
        return MySucceedResult().toJson()
    if request.method == 'GET':
        return param.PLEASE_USE_POST

'''
发送邮件api
{
    emial:''
    emialPassword:''
    title:''
    content:''
    toemail:''
    'token':'md5(timestamp&&appsecret)'
}
'''
@app.route('/app/sendmial',methods=['GET', 'POST'])
def sendmial():
    if request.method == 'POST':
        data = request.get_json()
        token = ''
        appkey = ''
        timestamp =''
        tokenMd5 = ''
        emial=''
        emialPassword=''
        content = ''
        toemail =''
        title=''
        try:
            for key in data:
                if key == 'token':
                    token = data['token']
                    tokenParams = token.split('&&')
                    tokenMd5 = tokenParams[1]
                    timestamp = tokenParams[0]
                if key == 'emial':
                    emial = data['emial']
                if key == 'emialPassword':
                    emialPassword = data['emialPassword']
                if key == 'content':
                    content = data['content']
                if key == 'toemail':
                    toemail = data['toemail']
                if key == 'title':
                    title = data['title']
        except Exception as e:
            pass
        if tokenMd5 != tool.md5(timestamp + '&&' + config.DEVELOPER_APPKEY):
                return MyException(param.APP_TOKEN_ERROR).toJson()
        else:
           result = sms.sendfuc(title,content,emial,emialPassword,toemail)
           if result == 1:
              return MySucceedResult().toJson()
           else:
              return MyException(param.APP_send_email_FAILURE).toJson()
    if request.method == 'GET':
        return param.PLEASE_USE_POST


'''
发送激活邮件
{
    toemail:''
    'token':'md5(timestamp&&appsecret)'
}
'''
@app.route('/app/sendmial/activate',methods=['GET', 'POST'])
def sendmial_activate():
    if request.method == 'POST':
        data = request.get_json()
        token = ''
        appkey = ''
        timestamp =''
        tokenMd5 = ''
        toemail=''
        content =  '来自云api的激活邮件,点击下方链接激活'
        try:
            for key in data:
                if key == 'token':
                    token = data['token']
                    tokenParams = token.split('&&')
                    tokenMd5 = tokenParams[1]
                    timestamp = tokenParams[0]
                if key == 'toemail':
                    toemail = data['toemail']
        except Exception as e:
            pass
        if tokenMd5 != tool.md5(timestamp + '&&' + config.DEVELOPER_APPKEY):
                return MyException(param.APP_TOKEN_ERROR).toJson()
        else:
            try:
                fnuser = connection.APP_admin.find_one({'email':toemail,'del':0})
                activeUrl = "%s/app/activate/%s" % (config.DOMAIN,str(fnuser['_id']))
                content += "<p><a href='%s'>点击激活</a></p>" % (activeUrl)
                content += "<p></p><p>%s</p>" % (activeUrl)
                result = sms.sendfuc('来自云api的激活邮件',content,'obghpj@163.com','jlmv38599',toemail)
                if result == 1:
                      return MySucceedResult().toJson()
                else:
                   return MyException(param.APP_send_email_FAILURE).toJson()
            except Exception, e:
                return MyException(param.PARAM_FAILURE).toJson()
       
    if request.method == 'GET':
        return param.PLEASE_USE_POST