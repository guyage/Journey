# coding=utf-8
from rest_framework import serializers
from db.models import *

class SQLQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = MySQLDatabase
        fields = ('id','dbname')