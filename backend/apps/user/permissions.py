# coding=utf-8
from rest_framework import permissions
from user.utils import init_permissions

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

class CustomerPremission(permissions.DjangoModelPermissions):
    
    message = 'No Permission to Access.'
    
    def has_permission(self, request, view):
        patch_map = 'edit'
        deletel_map = 'del'
        post_map = 'add'
        need_perms = ''
        module_perms = view.module_perms
        user_perms = init_permissions(request.user,'perms')
        if (request.user.is_superuser):
            return True
        else:
            if (request.method in SAFE_METHODS):
                return True
            else:
                if (request.method == 'PATCH'):
                    need_perms = module_perms[0] + ':' + patch_map
                elif (request.method == 'POST'):
                    need_perms = module_perms[0] + ':' + post_map
                elif (request.method == 'DELETE'):
                    need_perms = module_perms[0] + ':' + deletel_map
                if (need_perms in user_perms):
                    return True
                else:
                    return False

