from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from django.db.models import Q
from rest_framework import filters
from user.models import *
from user.serializers import *
from user.permissions import CustomerPremission
import random, string

def random_str(randomlength=10):
    a = list(string.ascii_letters)
    random.shuffle(a)
    return ''.join(a[:randomlength])

class UserGroupViewSet(viewsets.ModelViewSet):
    """
    list:
        用户组列表.
    create:
        创建用户组.
    delete:
        删除用户组.
    update:
        修改用户组.
    retrieve:
        查看用户组详情.
    partial_update:
        更新当前用户组部分记录.
    """

    # 权限相关
    permission_classes = [CustomerPremission,]
    module_perms = ['user:usergroup']
    
    queryset = UserGroup.objects.all().order_by('id')
    serializer_class = UserGroupSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('group','comment',)
    ordering_fields = ('id',)
    

    def update(self, request, *args, **kwargs):
        """
        用户组修改，多对多同时更新与用户表关联
        """
        partial = kwargs.pop('partial', False)
        userselected = request.data['userselected']
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        userlist = Users.objects.filter(Q(id__in=userselected))
        instance.user_group.set(userlist,bulk=True)
        return Response(serializer.data)

class MenuViewSet(viewsets.ModelViewSet):
    """
    list:
        菜单路由列表.
    create:
        创建菜单路由.
    delete:
        删除菜单路由.
    update:
        修改菜单路由.
    retrieve:
        查看菜单路由详情.
    partial_update:
        更新当前菜单路由部分记录.
    """
    # 权限相关
    permission_classes = [CustomerPremission,]
    module_perms = ['user:menu']

    queryset = Menu.objects.all().order_by('id')
    serializer_class = MenuSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    # search_fields = ('mtype',)
    ordering_fields = ('id',)
    
    def list(self, request, *args, **kwargs):
        results = []
        queryset = self.filter_queryset(self.get_queryset())
        for i in queryset.filter(Q(mtype=0)):
            results.append({'id':i.id,'name':i.name,'parent_id':i.parent_id,'url':i.url,'mtype':i.mtype,'icon':i.icon,'del_flag':i.del_flag,'children':[]})
        for item in results:
            for i in queryset.filter(Q(mtype__in=[1,2])&Q(parent_id=item['id'])):
                item['children'].append({'id':i.id,'name':i.name,'parent_id':i.parent_id,'url':i.url,'mtype':i.mtype,'icon':i.icon,'del_flag':i.del_flag})
        # for item in results:
        #     if (len(item['children']) > 0):
        #         for node in item['children']:
        #             for i in queryset.filter(Q(mtype=2)&Q(parent_id=node['id'])):
        #                 node['children'].append({'id':i.id,'name':i.name,'parent_id':i.parent_id,'url':i.url,'perms':i.perms,'mtype':i.mtype,'icon':i.icon,'del_flag':i.del_flag})
        # serializer = self.get_serializer(queryset, many=True)
        return Response(results)


class PermsViewSet(viewsets.ModelViewSet):
    """
    list:
        接口权限列表.
    create:
        创建接口权限.
    delete:
        删除接口权限.
    update:
        修改接口权限.
    """

    # 权限相关
    permission_classes = [CustomerPremission,]
    module_perms = ['user:perms']

    queryset = Perms.objects.all().order_by('id')
    serializer_class = PermsSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('module_perms','api')
    ordering_fields = ('id',)

    def list(self, request, *args, **kwargs):
        results = []
        queryset = self.filter_queryset(self.get_queryset())
        api_list = Perms.objects.values('api').distinct()
        for api in api_list:
            for i in (queryset.filter(Q(api=api['api']),Q(perms=''))):
                results.append({'id':i.id,'name':i.name,'api':i.api,'perms':i.perms,'children':[]})
        for item in results:
            for api_perms in queryset.filter(Q(api=item['api']),~Q(perms='')):
                item['children'].append({'id':api_perms.id,'perms':api_perms.perms,'del_flag':api_perms.del_flag})
        return Response(results)

    def create(self, request, *args, **kwargs):
        name = request.data['name']
        api = request.data['api']
        module_perms = request.data['module_perms']
        api_types = request.data['api_type']
        del_flag = request.data['del_flag']
        creator = request.data['creator']
        try:
            Perms.objects.create(name=name,api=api,module_perms=module_perms,del_flag=del_flag,creator=creator)
            for api_type in api_types:
                request.data['api_type'] = api_type
                perms = module_perms + ':' + api_type
                Perms.objects.create(api=api,module_perms=module_perms,perms=perms,del_flag=del_flag,creator=creator)
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        del_ids = Perms.objects.filter(Q(api=instance.api)).values('id')
        del_id = []
        for id in del_ids:
            del_id.append(id['id'])
        try:
            Perms.objects.filter(Q(id__in=del_id)).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RoleViewSet(viewsets.ModelViewSet):
    """
    list:
        角色列表.
    create:
        创建角色.
    delete:
        删除角色.
    update:
        修改角色.
    retrieve:
        查看角色详情.
    partial_update:
        更新当前角色部分记录.
    """

    # 权限相关
    permission_classes = [CustomerPremission,]
    module_perms = ['user:role']

    queryset = Role.objects.all().order_by('id')
    serializer_class = RoleSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('name')
    ordering_fields = ('id',)
    

    def update(self, request, *args, **kwargs):
        edittype = request.data['type']
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if (edittype == 'role_menu'):
            menuselected = request.data['menuselected']
            instance.menu.set(menuselected)
        elif (edittype == 'role_perms'):
            permsselected = request.data['permsselected']
            instance.perms.set(permsselected)
        elif (edittype == 'role_users'):
            userselected = request.data['userselected']
            instance.user_role.set(userselected)
        return Response(serializer.data)

class UsersViewSet(viewsets.ModelViewSet):
    """
    list:
        用户列表.
    create:
        创建用户.
    delete:
        删除用户.
    update:
        修改用户.
    retrieve:
        查看用户详情.
    partial_update:
        更新当前用户部分记录.
    """

    # 权限相关
    permission_classes = [CustomerPremission,]
    module_perms = ['user:user']
    
    queryset = Users.objects.all().order_by('id')
    serializer_class = UsersSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('username','email',)
    ordering_fields = ('id',)
    

    def create(self, request, *args, **kwargs):
        if (len(request.data['password']) == 0):
            mailtolist = []
            request.data['password'] = random_str()
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            username = request.data['username']
            password = request.data['password']
            useremail = request.data['email']
            mailtolist.append(useremail)
            userinfo = Users.objects.get(username=username)
            userinfo.set_password(password)
            userinfo.save()
            headers = self.get_success_headers(serializer.data)
            # maildata = {}
            # maildata['username'] = username
            # maildata['password'] = password
            # send_mail(mailtolist,1,maildata)
        return Response(request.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        if ('password' in request.data.keys()):
            mailtolist = []
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            username = request.data['username']
            password = request.data['password']
            useremail = request.data['email']
            #邮件内容
            maildata = {}
            maildata['username'] = username
            maildata['password'] = password
            #发送用户邮箱
            mailtolist.append(useremail)
            userinfo = Users.objects.get(username=username)
            userinfo.set_password(password)
            userinfo.save()
            
            # send_mail(mailtolist,2,maildata)
        else:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
        return Response(serializer.data)
