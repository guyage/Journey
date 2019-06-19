# coding=utf-8
from rest_framework import serializers
from conf.models import *

class MailConfigSerializer(serializers.ModelSerializer):
    
    mail_pass = serializers.CharField(style={'input_type': 'password'}, write_only=True,label='邮箱用户密码')
    class Meta:
        model = MailConfig
        fields = ('id','mail_host','mail_port','mail_user','mail_pass','create_time','update_time','comment')

