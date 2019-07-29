from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import filters
from user.models import *
from user.serializers import *
from user.user_api import *
from api.send_mail import send_mail

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
    """
    queryset = UserGroup.objects.all().order_by('id')
    serializer_class = UserGroupSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('group_name','comment',)
    ordering_fields = ('id',)

    def create(self, request, *args, **kwargs):
        userselected = request.data['userselected']
        group_name = request.data['group_name']
        del request.data['userselected']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        if (len(userselected) > 0):
            for user_id in userselected:
                # django models 多对多添加
                usergroup_add_user(group_name,user_id)
        return Response(request.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        userselected = request.data['userselected']
        group_name = request.data['group_name']
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        # django models 多对多清空
        instance.user_group_join.clear()
        if (len(userselected) > 0):
            for user_id in userselected:
                # django models 多对多添加
                usergroup_add_user(group_name,user_id)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # django models 多对多清空
        instance.user_group_join.clear()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class PermissionsGroupViewSet(viewsets.ModelViewSet):
    """
    list:
        权限组列表.
    create:
        创建权限组.
    delete:
        删除权限组.
    update:
        修改权限组.
    """
    queryset = PermissionsGroup.objects.all().order_by('id')
    serializer_class = PermissionsGroupSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('permissions_name','comment',)
    ordering_fields = ('id',)

    def create(self, request, *args, **kwargs):
        userselected = request.data['userselected']
        permissions_name = request.data['permissions_name']
        del request.data['userselected']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        if (len(userselected) > 0):
            for user_id in userselected:
                # django models 多对多添加
                permissionsgroup_add_user(permissions_name,user_id)
        return Response(request.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        userselected = request.data['userselected']
        permissions_name = request.data['permissions_name']
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        # django models 多对多清空
        instance.user_permissions_join.clear()
        if (len(userselected) > 0):
            for user_id in userselected:
                # django models 多对多添加
                permissionsgroup_add_user(permissions_name,user_id)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # django models 多对多清空
        instance.user_permissions_join.clear()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

# Create your views here.
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
    """
    queryset = Users.objects.all().order_by('id')
    serializer_class = UsersSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('username','email','mobile','webcat',)
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
            group_name = request.data['group']
            usergroup_add_user(group_name,userinfo.id)
            maildata = {}
            maildata['username'] = username
            maildata['password'] = password
            send_mail(mailtolist,1,maildata)
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
            if ('group' in request.data.keys()):
                group_name = request.data['group']
                usergroup_add_user(group_name,userinfo.id)
            send_mail(mailtolist,2,maildata)
        else:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            if ('group' in request.data.keys()):
                username = request.data['username']
                userinfo = Users.objects.get(username=username)
                group_name = request.data['group']
                usergroup_add_user(group_name,userinfo.id)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
        return Response(serializer.data)

