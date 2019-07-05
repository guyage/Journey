# coding=utf-8
from rest_framework import serializers
from conf.models import *

class MailConfigSerializer(serializers.ModelSerializer):
    
    mail_pass = serializers.CharField(style={'input_type': 'password'}, write_only=True,label='邮箱用户密码')
    class Meta:
        model = MailConfig
        fields = ('id','mail_host','mail_port','mail_user','mail_pass','create_time','update_time','comment')

class QueryLimitSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = QueryLimit
        fields = ('id','query_type','query_limit','comment')

class DumpWhiteListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DumpWhiteList
        fields = ('id','white_user','white_table')

