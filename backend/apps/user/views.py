# coding=utf-8

from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from user.models import *
from rest_framework.views import APIView
from user.serializers import *
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from api.send_mail import send_mail
from api.config import get_conf
from api.config import random_str
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_decode_handler,jwt_payload_handler,jwt_encode_handler
from user.utils import jwt_response_payload_handler
import jwt, time, uuid
# from django.contrib import auth


class UsersViewSet(viewsets.ModelViewSet):
    """
    用户列表，分页，查找
    """
    queryset = Users.objects.all().order_by('id')
    serializer_class = UsersSerializer
    # pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('username','email','mobile','webcat','group')
    ordering_fields = ('id',)

    def create(self, request, *args, **kwargs):
        # if len(request.data['password']) == 0:
        #     # default_passwd = 'aaa111'
        #     default_passwd = get_conf('userinfo', 'default_passwd')
        #     request.data['password'] = default_passwd
        if len(request.data['password']) == 0:
            mailtolist = []
            # default_passwd = get_conf('userinfo', 'default_passwd')
            default_passwd = random_str()
            request.data['password'] = default_passwd
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
            maildata = {}
            maildata['username'] = username
            maildata['password'] = password
            send_mail(mailtolist,maildata,1)
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
            send_mail(mailtolist,maildata,2)
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

class UserInfoViewSet(generics.GenericAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'username'

    def get(self,resuest,username):
        userinfo = self.get_object()
        serializer = self.get_serializer(userinfo)
        return Response(data=serializer.data)

# class UserAccessDbViewSet(viewsets.ModelViewSet):
#     """
#     用户访问数据库列表，查找
#     """
#     queryset = UserAccessDb.objects.all().order_by('id')
#     serializer_class = UserAccessDbSerializer
#     lookup_field = 'username'

#     def get(self,resuest,username):
#         userinfo = self.get_object()
#         serializer = self.get_serializer(userinfo)
#         return Response(data=serializer.data)

class LdapAuthViewSet(APIView):
    # jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
    authentication_classes = ()
    permission_classes = ()
    def post(self,request,format=None):
        username = request.data['username']
        password = request.data['password']
        usergo = authenticate(username=username,password=password)
        if usergo is not None:
            # auth_login(request,usergo)
            if usergo.is_active:
                payload = jwt_payload_handler(usergo)
                token = jwt_encode_handler(payload)
                response_data = jwt_response_payload_handler(token,usergo)
                return Response(response_data,status=status.HTTP_200_OK)
            else:
                content = {"non_field_errors":["用户账户已禁用。"]}
                return Response(content,status=status.HTTP_400_BAD_REQUEST)
        else:
            content = {"non_field_errors":["无法使用提供的认证信息登录。"]}
            return Response(content,status=status.HTTP_400_BAD_REQUEST)

class LogoutViewSet(viewsets.ViewSet):

    def logout(self, request):
        request.user.jwt_secret = uuid.uuid4()
        request.user.save()
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)       
        
