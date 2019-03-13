# coding=utf-8

from rest_framework import serializers
from db.models import *

class MySQLDatabaseSerializer(serializers.ModelSerializer):
    
    adminuser = serializers.CharField(write_only=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True,)
    class Meta:
        model = MySQLDatabase
        fields = ('id','dbname','host','port','adminuser','password','version','comment','is_enabled')

class MongodbInstSerializer(serializers.ModelSerializer):
    
    # manageuser = serializers.CharField(write_only=True)
    manageuserpwd = serializers.CharField(style={'input_type': 'password'}, write_only=True,)
    # readuser = serializers.CharField(write_only=True)
    readuserpwd = serializers.CharField(style={'input_type': 'password'}, write_only=True,)
    class Meta:
        model = MongodbInst
        fields = ('id','instname','host','port','manageuser','manageuserpwd','readuser','readuserpwd','version','comment','is_enabled')

class MongodbDBSerializer(serializers.ModelSerializer):
    
    mongodbinst_id = serializers.SlugRelatedField(many=False,read_only=True,slug_field='instname')
    # mongodbinst_id = serializers.HyperlinkedRelatedField(many=False,read_only=True,view_name='mongodbinst',lookup_field="id")
    class Meta:
        model = MongodbDB
        fields = ('id','mongodbinst_id','dbname','comment','is_enabled')

class RedisDBSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True,)
    class Meta:
        model = RedisDB
        fields = ('id','name','host','port','password','version','comment','is_enabled')
