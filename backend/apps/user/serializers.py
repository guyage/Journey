# coding=utf-8

from rest_framework import serializers
from user.models import *


class UsersSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True,)
    class Meta:
        model = Users
        fields = ('id','username','password','last_name','first_name','is_active','group','email','mobile','webcat','accessdb','comment')
    

# class UserAccessDbSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = UserAccessDb
#         fields = ('username','accessdblist')
    