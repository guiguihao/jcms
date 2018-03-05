#!/usr/bin/python
#coding=utf-8
import time
from  mailDb import readSenMail,readReceiveMail,record,sendMailWirteDb
from  sms import sendfuc

subject="剧场爆笑之逗！"   #主题
content = """
昨晚大半夜的
"""
def run():
    sIndex = 0
    sendMails = readSenMail()
    for receiveMail in  readReceiveMail():
        sendmail =  sendMails[7]
        try:
           sendfuc(subject,content,sendmail['mail'],sendmail['pw'],receiveMail['data'])
        except:
            pass
        if sIndex>=sendMails.count()-1:
            sIndex = 0
        else:
            sIndex += 1
        time.sleep(1)


if __name__ == '__main__':
    sendMailWirteDb('mail_1.txt')
    run()

