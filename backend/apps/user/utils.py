import json

def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'username': user.username,
        'is_superuser': user.is_superuser,
        # 'group': user.group,
        # 'permissions_group': user.permissions_group,
    }