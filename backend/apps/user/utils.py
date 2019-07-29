import json
# from .models import *
def get_user_permissionsgroup(user):
    permissionsgroup = []
    permissions_group = user.permissions_group.all()
    for i in permissions_group:
        permissionsgroup.append(i.permissions_name)
    return permissionsgroup

def get_user_group(user):
    usergroup = []
    user_group = user.group.all()
    for i in user_group:
        usergroup.append(i.group_name)
    return usergroup

def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'username': user.username,
        'is_superuser': user.is_superuser,
        'group': get_user_group(user),
        'permissions_group': get_user_permissionsgroup(user),
    }