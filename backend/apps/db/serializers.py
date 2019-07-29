# coding=utf-8
from rest_framework import serializers
from db.models import *

class MySQLInstSerializer(serializers.ModelSerializer):
    
    manage_userpwd = serializers.CharField(style={'input_type': 'password'}, write_only=True,label='管理用户密码')
    read_userpwd = serializers.CharField(style={'input_type': 'password'}, write_only=True,label='只读用户密码')
    class Meta:
        model = MySQLInst
        fields = ('id','inst_name','inst_host','inst_port','manage_user','manage_userpwd','read_user','read_userpwd','role','services','version','is_enabled','comment')

class UserAccessMySQLSerializer(serializers.ModelSerializer):

    mysqlinst = serializers.SlugRelatedField(many=False,read_only=True,slug_field='inst_name')
    class Meta:
        model = UserAccessMySQL
        fields = ('id','username','mysqlinst','user_access_db','create_time','status','comment')

class MongoDBInstSerializer(serializers.ModelSerializer):
    
    manage_userpwd = serializers.CharField(style={'input_type': 'password'}, write_only=True,label='管理用户密码')
    read_userpwd = serializers.CharField(style={'input_type': 'password'}, write_only=True,label='只读用户密码')
    class Meta:
        model = MongoDBInst
        fields = ('id','inst_name','inst_host','inst_port','manage_user','manage_userpwd','read_user','read_userpwd','role','services','version','is_enabled','comment')

class UserAccessMongoDBSerializer(serializers.ModelSerializer):

    mongodbinst = serializers.SlugRelatedField(many=False,read_only=True,slug_field='inst_name')
    class Meta:
        model = UserAccessMongoDB
        fields = ('id','username','mongodbinst','create_time','status','comment')

class RedisInstSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True,label='密码')
    
    class Meta:
        model = RedisInst
        fields = ('id','inst_name','inst_host','inst_port','password','role','services','version','is_enabled','comment')

class UserAccessRedisSerializer(serializers.ModelSerializer):

    redisinst = serializers.SlugRelatedField(many=False,read_only=True,slug_field='inst_name')
    class Meta:
        model = UserAccessRedis
        fields = ('id','username','redisinst','create_time','status','comment')