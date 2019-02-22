# coding=utf-8

from django.shortcuts import render
from rest_framework import viewsets
from db.models import *
from db.serializers import *
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from rest_framework.views import APIView
from api.db_api import db_api
from django.db.models import Q
from rest_framework.response import Response

class MySQLDatabaseViewSet(viewsets.ModelViewSet):
    """
    数据库列表，分页，查找
    """
    queryset = MySQLDatabase.objects.all().order_by('id')
    serializer_class = MySQLDatabaseSerializer
    # pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('dbname','host','port','version')
    ordering_fields = ('id',)

class MysqlMetaViewSet(APIView):

    def post(self,request,format=None):
        dbapi = db_api()
        dbname = request.data['dbname']
        request_type = request.data['type']
        dbinfo = MySQLDatabase.objects.get(Q(dbname=dbname))
        # 获取连接信息
        connectinfo = {'conn_host':'','conn_port':'','conn_user':'','conn_passwd':'','conn_db':''}
        connectinfo['conn_host'] = dbinfo.host
        connectinfo['conn_port'] = dbinfo.port
        connectinfo['conn_user'] = dbinfo.adminuser
        connectinfo['conn_passwd'] = dbinfo.password
        connectinfo['conn_db'] = dbname
        # 查询关键字
        if ( str(request_type) == 'db'):
            col,results = dbapi.get_metadata(1,connectinfo,dbname)
        elif ( str(request_type) == 'table'):
            tablename = request.data['tablename']
            col,results = dbapi.get_metadata(2,connectinfo,dbname,tablename)
        elif ( str(request_type) == 'column'):
            tablename = request.data['tablename']
            col,results = dbapi.get_metadata(3,connectinfo,dbname,tablename)
        elif ( str(request_type) == 'index'):
            tablename = request.data['tablename']
            col,results = dbapi.get_metadata(4,connectinfo,dbname,tablename)
        re = { 'col': '', 'results': '',}
        re['col'] = col
        re['results'] = results
        return Response(re)

class MongodbInstViewSet(viewsets.ModelViewSet):
    """
    数据库列表，分页，查找
    """
    queryset = MongodbInst.objects.all().order_by('id')
    serializer_class = MongodbInstSerializer
    # pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('instname','host','port','version')
    ordering_fields = ('id',)

class MongodbDBViewSet(viewsets.ModelViewSet):
    """
    数据库列表，分页，查找
    """
    queryset = MongodbDB.objects.all().order_by('id')
    serializer_class = MongodbDBSerializer
    # pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('mongodbinst_id','dbname',)
    ordering_fields = ('id',)

