from django.shortcuts import render
# Create your views here.
from django.core import serializers
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from api.db_api import db_api
from db.models import *
import json,datetime,time
from api.config import get_conf

default_limit = get_conf('sqllimit', 'limit')

class SQLQueryViewSet(APIView):

    def post(self,request,format=None):
        dbapi = db_api()
        dbname = request.data['dbname']
        dbinfo = MySQLDatabase.objects.get(Q(dbname=dbname))
        connectinfo = {'conn_host':'','conn_port':'','conn_user':'','conn_passwd':'','conn_db':''}
        connectinfo['conn_host'] = dbinfo.host
        connectinfo['conn_port'] = dbinfo.port
        connectinfo['conn_user'] = dbinfo.adminuser
        connectinfo['conn_passwd'] = dbinfo.password
        connectinfo['conn_db'] = dbname
        # sql = 'select * from student;'
        exectype = request.data['exectype']
        sql = request.data['sql']
        if 'limit' in sql.lower():
            limit_sql = sql
        else:
            sql_end = sql[len(sql)-1]
            if sql_end == ';':
                limit = ' limit ' + default_limit + ';'
                limit_sql =  sql.replace(';',limit)
            else:
                limit_sql = sql + ' limit ' + default_limit + ';'
        if (exectype == 'exec'):
            col,results = dbapi.mysql_query(connectinfo,limit_sql)
        elif (exectype == 'explain'):
            explain_sql = 'explain %s' % limit_sql
            col,results = dbapi.mysql_query(connectinfo,explain_sql)

        re = { 'col': '', 'results': '',}      
        re['col'] = col
        re['results'] = results
        return Response(re)

class SQLSoarViewSet(APIView):
    def post(self,request,format=None):
        dbapi = db_api()
        username = request.data['username']
        dbname = request.data['dbname']
        sql = request.data['sql']
        soartype = request.data['soartype']
        dbinfo = MySQLDatabase.objects.get(Q(dbname=dbname))
        dsn = dbinfo.adminuser + ':' + dbinfo.password + '@' + dbinfo.host + ':' + str(dbinfo.port) + '/' + dbname
        if (soartype == 'optimize'):
            soar_results = dbapi.sql_soar(1,sql,dsn,username)
            re = {'results':soar_results}
        return Response(re)
