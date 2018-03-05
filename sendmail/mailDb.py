#!/usr/bin/python
#coding=utf-8
from mgdb import send_mail,receive_mail,record_mail

#发送邮箱批量写入数据库
def sendMailWirteDb(filename):
    file = open(filename)
    while 1:
        line = file.readline().strip()
        if not line:
            break
        list = line.split('----')
        mailcol = send_mail.find_one({'mail':list[0]})
        if not mailcol:
            send_mail.insert({'mail': list[0], 'pw': list[1]})
        print  '写入数据库' + str(list)
    file.close()

#读取发送邮箱
def readSenMail():
    cols = send_mail.find()
    return cols

# 读取接收邮箱
def readReceiveMail():
    # cols = receive_mail.find()
    cols = [{'data':'393314661@qq.com'}]
    return cols

#发送记录
def record(content):
    record_mail.insert({'data':content})


# sendMailWirteDb('mail_1.txt')
#readSenMail()