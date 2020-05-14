# coding=utf-8

from rest_framework import serializers
from user.models import *

class UserGroupSerializer(serializers.ModelSerializer):
    
    hasuser = serializers.SerializerMethodField('get_usergroup_hasuser')
    class Meta:
        model = UserGroup
        fields = ('id','group','comment','hasuser')
    
    def get_usergroup_hasuser(self,obj):
        userlist = []
        for user in obj.user_group.all():
            userlist.append(user.id)
        return userlist

class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = ('id','name','parent_id','url','mtype','icon','creator','modifier','del_flag','create_time','update_time','comment')

class PermsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Perms
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):

    hasmenu = serializers.SerializerMethodField('get_role_hasmenu')
    hasuser = serializers.SerializerMethodField('get_role_hasuser')
    hasperms = serializers.SerializerMethodField('get_role_hasperms')
    class Meta:
        model = Role
        fields = ('id','name','hasmenu','hasuser','hasperms')

    def get_role_hasmenu(self,obj):
        hasmenulist = []
        for menu in obj.menu.all():
            hasmenulist.append(menu.id)
        return hasmenulist
    def get_role_hasuser(self,obj):
        userlist = []
        for user in obj.user_role.all():
            userlist.append(user.id)
        return userlist
    def get_role_hasperms(self,obj):
        haspermslist = []
        for perm in obj.perms.all():
            haspermslist.append(perm.id)
        return haspermslist

class UsersSerializer(serializers.ModelSerializer):

    password = serializers.CharField(style={'input_type': 'password'}, write_only=True,)
    group = serializers.SlugRelatedField(read_only=True,slug_field='group')
    roles = serializers.SlugRelatedField(many=True,read_only=True,slug_field='name')
    class Meta:
        model = Users
        fields = ('id','username','password','email','is_superuser','is_active','last_name','first_name','group','roles','comment')