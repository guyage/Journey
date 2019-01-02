# coding=utf-8

from rest_framework import serializers
from db.models import *

class MySQLDatabaseSerializer(serializers.ModelSerializer):
    
    adminuser = serializers.CharField(write_only=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True,)
    class Meta:
        model = MySQLDatabase
        fields = ('id','dbname','host','port','adminuser','password','version','comment','is_enabled')