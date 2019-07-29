# coding: utf-8

from user.models import *
import random, string

def random_str(randomlength=10):
    a = list(string.ascii_letters)
    random.shuffle(a)
    return ''.join(a[:randomlength])

def usergroup_add_user(group_name, user_id=None):
    """
    用户组中添加用户
    """
    if user_id:
        user = Users.objects.get(id=user_id)
    if user:
        usergroup = UserGroup.objects.get(group_name=group_name)
        user.group.add(usergroup)

def permissionsgroup_add_user(permissions_name, user_id=None):
    """
    权限组中添加用户
    """
    if user_id:
        user = Users.objects.get(id=user_id)
    if user:
        permissionsgroup = PermissionsGroup.objects.get(permissions_name=permissions_name)
        user.permissions_group.add(permissionsgroup)

