# coding=utf-8
from rest_framework import serializers
from workorder.models.autoorder import *
from django.db.models import Q

class AutoOrderTypeSerializer(serializers.ModelSerializer):

    hasstep = serializers.SerializerMethodField('get_ordertype_hasstep')
    stepscount = serializers.SerializerMethodField('get_ordertype_stepscount')
    class Meta:
        model = AutoOrderType
        fields = ('id','ordertype','formconfig','remotefuncs','script','hasstep','stepscount')
    def get_ordertype_hasstep(self,obj):
        steps = []
        for step in obj.ordertype_step.all().order_by('step_id'):
            step_approver_group = step.approver_group
            if (step_approver_group):
                approver_group_name = step_approver_group.approver_group_name
                approver_group_id = step_approver_group.id
                steps.append({'id':step.id,'step_id':step.step_id,'step_name':step.step_name,'approver_group_id':approver_group_id,'approver_group_name':approver_group_name})
            else:
                steps.append({'id':step.id,'step_id':step.step_id,'step_name':step.step_name,'approver_group_name':''})
        return steps
    def get_ordertype_stepscount(self,obj):
        stepscount = obj.ordertype_step.all().count()
        return stepscount

# class ApprovalGroupSerializer(serializers.ModelSerializer):

#     hasuser = serializers.SerializerMethodField('get_approvergroup_hasuser')
#     hasusername = serializers.SerializerMethodField('get_approvergroup_hasusername')
#     class Meta:
#         model = ApprovalGroup
#         fields = ('id','approver_group_name','hasuser','hasusername')
#     def get_approvergroup_hasuser(self,obj):
#         userlist = []
#         for user in obj.users.all():
#             userlist.append(user.id)
#         return userlist
#     def get_approvergroup_hasusername(self,obj):
#         usernamelist = []
#         for user in obj.users.all():
#             usernamelist.append(user.username)
#         return usernamelist

class AutoOrderStepSerializer(serializers.ModelSerializer):

    approver_group = serializers.SlugRelatedField(many=False,read_only=True,slug_field='approver_group_name')
    class Meta:
        model = AutoOrderStep
        fields = ('id','ordertype','step_name','approver_group','step_id',)

class AutoOrderSerializer(serializers.ModelSerializer):

    autoorderstate = serializers.SerializerMethodField('get_autoorder_state')
    ordertypename = serializers.SerializerMethodField('get_ordertype_name')
    class Meta:
        model = AutoOrder
        fields = ('id','title','status','classify','autoorderstate','ordertype','ordertypename','content','creator','operator','create_time','update_time')
    def get_autoorder_state(self,obj):
        autoorder_state = []
        states = obj.state_autoorder_id.all()
        for state in states:
            autoorder_state.append({'step_id':state.step,'action':state.action,'operator':state.operator,'update_time':state.update_time})
        return autoorder_state
    def get_ordertype_name(self,obj):
        if (obj.ordertype):
            ordertypename = obj.ordertype.ordertype
        else:
            ordertypename = ''
        return ordertypename
