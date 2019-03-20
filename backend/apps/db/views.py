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
    search_fields = ('dbname','service','comment',)
    ordering_fields = ('id',)

class MysqlMetaViewSet(APIView):

    def post(self,request,format=None):
        dbapi = db_api()
        dbname = request.data['dbname']
        request_type = request.data['type']
        dbinfo = MySQLDatabase.objects.get(Q(dbname=dbname))
        instinfo = dbinfo.mysqlinst_id
        # 获取连接信息
        connectinfo = {'conn_host':'','conn_port':'','conn_user':'','conn_passwd':'','conn_db':''}
        connectinfo['conn_host'] = instinfo.host
        connectinfo['conn_port'] = instinfo.port
        connectinfo['conn_user'] = instinfo.manageuser
        connectinfo['conn_passwd'] = instinfo.manageuserpwd
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

class MysqlUserViewSet(APIView):

    def post(self,request,format=None):
        dbapi = db_api()
        instname = request.data['instname']
        request_type = request.data['type']
        # dbinfo = MySQLDatabase.objects.get(Q(dbname=dbname))
        instinfo = MySQLInst.objects.get(Q(instname=instname))
        instid = instinfo.id
        dblistinfo = MySQLDatabase.objects.filter(Q(mysqlinst_id=instid))
        dblist = []
        for i in dblistinfo:
            dblist.append(i.dbname)
        # 获取连接信息
        connectinfo = {'conn_host':'','conn_port':'','conn_user':'','conn_passwd':'','conn_db':''}
        connectinfo['conn_host'] = instinfo.host
        connectinfo['conn_port'] = instinfo.port
        connectinfo['conn_user'] = instinfo.manageuser
        connectinfo['conn_passwd'] = instinfo.manageuserpwd
        connectinfo['conn_db'] = 'mysql'
        # 查询关键字
        if ( str(request_type) == 'showusers'):
            col,results = dbapi.get_metadata(5,connectinfo)
        elif ( str(request_type) == 'showuserpri'):
            user = request.data['user']
            sql = 'show grants for ' + user + ';'
            col,result = dbapi.mysql_query(connectinfo,sql)
            results = []
            for i in result:
                for value in i.values():
                    results.append(value)
        elif (str(request_type) == 'adduserlist'):
            col = ''
            results = ''
        elif (str(request_type) == 'adduser'):
            grantuser = request.data['grantuser']
            userpri = ','.join(grantuser['userpri'])
            grantsql = "grant %s on %s.* to %s@'%s' identified by '%s';" % (userpri,grantuser['userpridb'],grantuser['username'],grantuser['userip'],grantuser['userpwd'])
            col,results = dbapi.mysql_query(connectinfo,grantsql)
        elif (str(request_type) == 'dropuser'):
            user = request.data['user']
            dropusersql = "drop user %s;" % (user)
            col,results = dbapi.mysql_query(connectinfo,dropusersql)
        re = { 'col': '', 'results': '','dblist': ''}
        re['col'] = col
        re['results'] = results
        re['dblist'] = dblist
        print (re)
        return Response(re)

class MySQLInstViewSet(viewsets.ModelViewSet):
    """
    数据库列表，分页，查找
    """
    queryset = MySQLInst.objects.all().order_by('id')
    serializer_class = MySQLInstSerializer
    # pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('instname','host','port','version')
    ordering_fields = ('id',)

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

class RedisDBViewSet(viewsets.ModelViewSet):
    """
    RedisDB列表，分页，查找
    """
    queryset = RedisDB.objects.all().order_by('id')
    serializer_class = RedisDBSerializer
    # pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('name','host','port','version')
    ordering_fields = ('id',)

