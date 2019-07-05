# coding=utf-8

from django.shortcuts import render
from rest_framework import viewsets
from conf.models import *
from conf.serializers import *
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import filters
from rest_framework.response import Response
from api.send_mail import send_mail

# Create your views here.
class MailConfigViewSet(viewsets.ModelViewSet):
    """
    邮箱配置列表，分页，查找
    """
    queryset = MailConfig.objects.all().order_by('id')
    serializer_class = MailConfigSerializer
    # pagination_class = PageNumberPagination
    ordering_fields = ('id',)

class QueryLimitViewSet(viewsets.ModelViewSet):
    """
    QueryLimit列表，分页，查找
    """
    queryset = QueryLimit.objects.all().order_by('id')
    serializer_class = QueryLimitSerializer
    # pagination_class = PageNumberPagination
    ordering_fields = ('id',)

class DumpWhiteListViewSet(viewsets.ModelViewSet):
    """
    QueryLimit列表，分页，查找
    """
    queryset = DumpWhiteList.objects.all().order_by('-id')
    serializer_class = DumpWhiteListSerializer
    # pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('white_user',)
    ordering_fields = ('id',)

class MailTestViewSet(APIView):
    def post(self,request,format=None):
        mailtolist = []
        testmail = request.data['testmail']
        mailtolist.append(testmail)
        results = send_mail(mailtolist,3)
        if (results):
            send_stat = 'sucess'
        else:
            send_stat = 'fail'
        return Response({'status': send_stat}, status=status.HTTP_200_OK)