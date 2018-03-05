#!/usr/bin/python
#coding=utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from  mailDb import record
#msg_from='j8855@vip.qq.com'                                 #发送方邮箱
#passwd='gbsiprmbcxcvbhhj'                                   #填入发送方邮箱的授权码
#msg_to='393314661@qq.com'                                  #收件人邮箱
                            
#subject="分析报告"                                     #主题

def sendfuc(subject,content,msg_from,passwd,msg_to):
	msg = MIMEText(content,'html','utf-8')
	msg['Subject'] = subject
	msg['From'] = msg_from
	msg['To'] = msg_to
	# msg['From'] = Header("每日笑话", 'utf-8')
	try:
	    s = smtplib.SMTP_SSL("smtp.163.com",994)               #邮件服务器及端口号
	    s.login(msg_from, passwd)
	    s.sendmail(msg_from, msg_to, msg.as_string())
	    print "发送成功"
	except s.SMTPException,e:
	    print "发送失败"
	finally:
		try:
			s.quit()
		except:
			pass







