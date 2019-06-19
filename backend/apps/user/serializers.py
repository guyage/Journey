# coding=utf-8

from rest_framework import serializers
from user.models import *

class UserGroupSerializer(serializers.ModelSerializer):
    
    usercount = serializers.SerializerMethodField('get_group_usercount')
    userlist = serializers.SerializerMethodField('get_group_userlist')
    class Meta:
        model = UserGroup
        fields = ('id','group_name','comment','usercount','userlist')

    def get_group_usercount(self,obj):
        # django models ManyToManyField Query(多对多反向查询)
        return obj.user_group_join.all().count()
    def get_group_userlist(self,obj):
        userlist = []
        for user in obj.user_group_join.all():
            userlist.append(user.id)
        return userlist


class PermissionsGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = PermissionsGroup
        fields = ('id','permissions_name','comment')

class UsersSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True,)
    group = serializers.SlugRelatedField(many=True,read_only=True,slug_field='group_name')
    class Meta:
        model = Users
        fields = ('id','username','group','password','last_name','first_name','is_superuser','is_active','permissions_group','email','mobile','webcat','comment')

