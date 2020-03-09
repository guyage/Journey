# coding=utf-8
from rest_framework import serializers
from workorder.models.approvalgroup import *

class ApprovalGroupSerializer(serializers.ModelSerializer):

    hasuser = serializers.SerializerMethodField('get_approvergroup_hasuser')
    hasusername = serializers.SerializerMethodField('get_approvergroup_hasusername')
    class Meta:
        model = ApprovalGroup
        fields = ('id','approver_group_name','hasuser','hasusername')
    def get_approvergroup_hasuser(self,obj):
        userlist = []
        for user in obj.users.all():
            userlist.append(user.id)
        return userlist
    def get_approvergroup_hasusername(self,obj):
        usernamelist = []
        for user in obj.users.all():
            usernamelist.append(user.username)
        return usernamelist