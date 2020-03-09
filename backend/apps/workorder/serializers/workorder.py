# coding=utf-8
from rest_framework import serializers
from workorder.models.sqlorder import *

class AllWorkOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=128)
    classify = serializers.CharField(max_length=50)
    status = serializers.IntegerField()
    creator = serializers.CharField(max_length=50)
    operator = serializers.CharField(max_length=50)
    create_time = serializers.DateTimeField()
    update_time = serializers.DateTimeField()

