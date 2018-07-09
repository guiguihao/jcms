#!/usr/bin/python
#-*-coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header
#msg_from='j8855@vip.qq.com'                                 #发送方邮箱
#passwd='gbsiprmbcxcvbhhj'                                   #填入发送方邮箱的授权码
#msg_to='393314661@qq.com'                                  #收件人邮箱
                            
#subject="分析报告"                                     #主题

def sendfuc(subject,content,msg_from,passwd,msg_to):
	result = 0
	msg = MIMEText(content,'html','utf-8')
	msg["Accept-Language"]="zh-CN"
	msg["Accept-Charset"]="ISO-8859-1,utf-8" 
	msg['Subject'] = subject
	# msg['From'] = msg_from
	msg['To'] = msg_to
	msg['From'] = Header("ROOTOPEN.COM", 'utf-8')
	try:
	    s = smtplib.SMTP_SSL("smtp.163.com",994)               #邮件服务器及端口号
	    s.login(msg_from, passwd)
	    s.sendmail(msg_from, msg_to, msg.as_string())
	    result = 1
	except:
	    result = 0
	finally:
		try:
			s.quit()
		except:
			pass
	return result


# sendfuc("多福多寿biaoti",'ceshi来说地方',"dtadhm@163.com",'he088063','jiangguishun@126.com')






