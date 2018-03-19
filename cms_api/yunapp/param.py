#!/usr/bin/python
#-*-coding:utf-8 -*-
PLEASE_USE_POST = '请使用post请求'

SUCCEED = (1,'成功')
PARAM_FAILURE = (2,'参数错误')
CHECK_FAILURE = (101,'字段校验失败,请检查字段的值是否符合校验规则')
REGISTER_FAILURE = (102,'用户名或手机号码必须填写一个,密码必须填写')
LONGIN_FAILURE = (103,'密码或用户名错误')
UPDATAE_USER_FAILURE = (104,'更新用户信息失败,请检查传递参数')
USER_NAME_FAILURE = (105,'用户名已存在')
USER_EMAIL_FAILURE = (106,'email已存在')
USER_PHONE_FAILURE = (107,'手机号码已存在')
USER_VIP_FAILURE = (109,'vip类型不存在')
APP_NAME_FAILURE = (108,'应用名称重复')
APP_USER_NULL = (110,'此用户不存在')
APP_TOKEN_NULL = (201,'token不可为空')
APP_TOKEN_ERROR = (202,'token错误')
APP_TOKEN_TIME_ERROR = (203,'时间过期')
APP_TOKEN_RULE_ERROR = (204,'appsecret和时间戳MD5校验错误')
APP_VIPTYPE_NAME_FAILURE = (301,'会员类型名称重复')
APP_send_email_FAILURE = (351,'发送邮件验证码失败')
APP_ACTIVE_ED_FAILURE = (352,'您已经激活无需再激活')