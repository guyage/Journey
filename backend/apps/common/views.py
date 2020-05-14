# coding=utf-8

from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
import uuid
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from rest_framework_jwt.utils import jwt_decode_handler,jwt_payload_handler,jwt_encode_handler
from user.utils import jwt_response_payload_handler
# Create your views here.

class LogoutViewSet(viewsets.ViewSet):

    def logout(self, request):
        request.user.jwt_secret = uuid.uuid4()
        request.user.save()
        return Response({'status': 'ok'}, status=status.HTTP_200_OK) 

class LdapAuthViewSet(APIView):
    # jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
    authentication_classes = []
    permission_classes = []
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
