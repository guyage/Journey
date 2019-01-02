#/usr/bin/env python
# -*- coding: UTF-8 -*-
import smtplib  
import sys
#from email.mime.text import MIMEText  
from email.mime.text import MIMEText
from api.config import get_conf

# 邮件服务连接信息
mail_host = get_conf('mail','mail_host')
mail_user = get_conf('mail','mail_user')
mail_pass = get_conf('mail','mail_pass')
mail_postfix = get_conf('mail','mail_postfix')
# 平台域名
platform_domain = get_conf('domain_name','domain')

def send_mail_fun(to_list,sub,content):    
	# content = content.decode('utf8').encode('gbk') 
    me="monitor"+"<"+mail_user+"@"+mail_postfix+">"  
    msg = MIMEText(content,_subtype='plain',_charset='gbk')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host)  
        server.login(mail_user,mail_pass)  
        server.sendmail(me, to_list, msg.as_string())  
        server.close()  
        return True  
    except Exception as e:  
        print (str(e))
        return False

def send_mail(to_list,maildata=None,type=None):

    if type == 1:
        sub = '用户创建通知'
        content = '你好，SQL_Platform用户已创建，\
        用户名: %s \
        初始密码：%s \
        登陆地址：' % (maildata['username'], maildata['password'])
        content = content + platform_domain
        send_mail_fun(to_list,sub,content)
    elif (type == 2):
        sub = '密码修改通知'
        content = '你好，SQL_Platform用户密码已修改，\
        用户名: %s \
        密码：%s \
        登陆地址：' % (maildata['username'], maildata['password'])
        content = content + platform_domain
        send_mail_fun(to_list,sub,content)