#/usr/bin/env python
# -*- coding: UTF-8 -*-
import smtplib  
import sys
#from email.mime.text import MIMEText  
from email.mime.text import MIMEText
# from apps.conf.models import MailConfig
from conf.models import MailConfig

# 平台域名
platform_domain = 'http://journey.xs.jf'

def send_mail_fun(to_list,sub,content):
    mailconfig = MailConfig.objects.get(id=1)
    # 邮件服务连接信息
    mail_host = mailconfig.mail_host
    mail_port = mailconfig.mail_port
    mail_user = mailconfig.mail_user
    mail_pass = mailconfig.mail_pass    
	# content = content.decode('utf8').encode('gbk') 
    me="monitor"+"<"+mail_user+">"  
    msg = MIMEText(content,_subtype='plain',_charset='gbk')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host,mail_port)  
        server.login(mail_user,mail_pass)  
        server.sendmail(me, to_list, msg.as_string())  
        server.close()  
        return True  
    except Exception as e:  
        print (str(e))
        return False

def send_mail(to_list,type=None,maildata=None):
    if type == 1:
        sub = '用户创建通知'
        content = '你好，Journey DB 平台用户已创建，\
        用户名: %s \
        初始密码：%s \
        登陆地址：%s' % (maildata['username'], maildata['password'],platform_domain)
        content = content + platform_domain
        res = send_mail_fun(to_list,sub,content)
    elif (type == 2):
        sub = '密码修改通知'
        content = '你好，Journey DB 平台用户密码已修改，\
        用户名: %s \
        密码：%s \
        登陆地址：%s' % (maildata['username'], maildata['password'],platform_domain)
        content = content + platform_domain
        res = send_mail_fun(to_list,sub,content)
    elif (type == 3):
        sub = 'Journey DB测试邮件'
        content = 'Journey DB 平台测试邮件!'
        res = send_mail_fun(to_list,sub,content)
    
    return res