# coding: utf-8

from user.models import *
import random, string

def random_str(randomlength=10):
    a = list(string.ascii_letters)
    random.shuffle(a)
    return ''.join(a[:randomlength])

def group_add_user(group_name, user_id=None):
    """
    用户组中添加用户
    """
    if user_id:
        user = Users.objects.get(id=user_id)
    if user:
        usergroup = UserGroup.objects.get(group_name=group_name)
        user.group.add(usergroup)

