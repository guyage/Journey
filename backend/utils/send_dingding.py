#/usr/bin/env python
# -*- coding: UTF-8 -*-
from rest_framework.views import APIView
from user.models import Users
import requests,json
from django.http import HttpResponse
#发送钉钉消息接口
class SendDingTalk(APIView):
    def post(self,request,format=None):
        msg = request.data['message']
        create_user = request.data['creator']
        title = request.data['title']
        all_info = Users.objects.filter(username=create_user).first()
        mobile = all_info.mobile
        '''
        data:
        {'edit_user': 'admin', 'title': '【工单有新回复】222', 'message': '指派人: admin\n工单地址: http://127.0.0.1:8080/#/viewworkticket/2'}
        '''
        # print('=====',msg)
        url = 'http://skyeye.xs.jf/micro/eye/dingtalk/d010/sendSystemMessage'
        value = {
            'mobile': mobile,
            'title': title,
            'message': msg
        }
        # value = json.dumps(value)
        result = requests.post(url,value)
        print('----------------------------')
        print(result.text)       
        return HttpResponse('ok')


class SendAll(APIView):
    def post(self,request,format=None):
        msg = request.data['message']
        url = 'https://oapi.dingtalk.com/robot/send?access_token=c58513e584c8f961dc7d195e81573f41406bd92e0d74a53ddcbecf40e25a79f6'
        HEADERS = {
        "Content-Type": "application/json" ,
        "charset":"utf-8"
        }
        value = {
            "msgtype": "text",
            "text": {
                'content':msg
                },
        }
        value = json.dumps(value)
        value = value.encode("utf-8")
        result = requests.post(url=url,data=value,headers=HEADERS)
        
        return HttpResponse('ok')

class SendOp(APIView):
    def post(self,request,format=None):
        print ('--------------------------------------------')
        msg = request.data['message']
        print('============================================')
        # all_info = Users.objects.filter(username=create_user).first()
        # mobile = all_info.mobile
        # url = 'https://oapi.dingtalk.com/robot/send?access_token=d7c1544dd56050ebf7e7fc57048069782540ec9b1d2027423bebb5341914243b'
        url = 'https://oapi.dingtalk.com/robot/send?access_token=c6e64590c9209518e054a27518ce575f47721f2ade85a71f5f1d0590cff3cf61'
        HEADERS = {
        "Content-Type": "application/json" ,
        "charset":"utf-8"
        }
        value = {
            "msgtype": "text",
            "text": {
                "content":msg 
                    # "title": title,
                    # '创建者':create_user,
                    # 'msg':msg
                },
        }
        value = json.dumps(value)
        value = value.encode("utf-8")
        result = requests.post(url=url,data=value,headers=HEADERS)
        print(result.content)
        # print(result.text)
        
        return HttpResponse('ok')