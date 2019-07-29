# coding=utf-8

from rest_framework import serializers
from workflow.models import *

class WorkOrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WorkOrder
        fields = ('id','order_prefix','order_type','title','status','content','describe','creator','operation_group','operator','create_time','update_time','comment')

class WorkOrderStateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WorkOrderState
        fields = ('id','gitwordorder_id','action','operator','create_time','update_time','comment')

class WorkOrderStepSerializer(serializers.Serializer):
    
    step = serializers.IntegerField(read_only=True)
    action = serializers.CharField(read_only=True)
    operator = serializers.CharField(read_only=True)
    create_time = serializers.CharField(read_only=True)
    comment = serializers.CharField(read_only=True)
    