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
import json




default_limit = get_conf('sqllimit', 'limit')
dump_white_list = get_conf('dump_white_list', 'white_list')

class SQLQueryViewSet(APIView):
    def post(self,request,format=None):
        dbapi = db_api()
        dbname = request.data['dbname']
        dbinfo = MySQLDatabase.objects.get(Q(dbname=dbname))
        instinfo = dbinfo.mysqlinst_id
        connectinfo = {'conn_host':'','conn_port':'','conn_user':'','conn_passwd':'','conn_db':''}
        connectinfo['conn_host'] = instinfo.host
        connectinfo['conn_port'] = instinfo.port
        connectinfo['conn_user'] = instinfo.manageuser
        connectinfo['conn_passwd'] = instinfo.manageuserpwd
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
            islimit = 1
            execsqltables = dbapi.extract_table_name_from_sql(sql)
            whitelist_tables = set(dump_white_list.split(","))
            difftables = execsqltables - whitelist_tables
            if (len(difftables) > 0):
                col,results = dbapi.mysql_query(connectinfo,limit_sql,islimit)
            else:
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
        instinfo = dbinfo.mysqlinst_id
        dsn = instinfo.manageuser + ':' + instinfo.manageuserpwd + '@' + instinfo.host + ':' + str(instinfo.port) + '/' + dbname
        if (soartype == 'optimize'):
            soar_results = dbapi.sql_soar(1,sql,dsn,username)
            re = {'results':soar_results}
        return Response(re)

class MongodbQueryViewSet(APIView):
    def post(self,request,format=None):
        dbapi = db_api()
        exectype = request.data['exectype']
        dbname = request.data['dbname']
        dbinfo = MongodbDB.objects.get(Q(dbname=dbname))
        instinfo = dbinfo.mongodbinst_id
        # instinfo = MongodbInst.objects.get(Q(id=instid))
        connectinfo = {'conn_host':'','conn_port':'','conn_user':'','conn_passwd':'','conn_db':''}
        connectinfo['conn_host'] = instinfo.host
        connectinfo['conn_port'] = instinfo.port
        connectinfo['conn_user'] = instinfo.readuser
        connectinfo['conn_passwd'] = instinfo.readuserpwd
        connectinfo['conn_db'] = dbname
        if (exectype == 'table'):
            query_results = dbapi.mongodb_query(1, connectinfo)
        elif (exectype == 'sql'):
            # username = request.data['username']
            sql = request.data['sql']
            query_results = dbapi.mongodb_query(2, connectinfo, sql)
        # query_results = dbapi.mongodb_query(1, connectinfo)
        re = {'results':query_results}
        return Response(re)

class RedisdbQueryViewSet(APIView):
    def post(self,request,format=None):
        dbapi = db_api()
        exectype = request.data['exectype']
        redisname = request.data['selectredis']
        selectdb = request.data['selectdb']
        rediskey = request.data['rediskey']
        dbinfo = RedisDB.objects.get(Q(name=redisname))
        connectinfo = {'conn_host':'','conn_port':'','conn_passwd':'','conn_db':''}
        connectinfo['conn_host'] = dbinfo.host
        connectinfo['conn_port'] = dbinfo.port
        connectinfo['conn_passwd'] = dbinfo.password
        connectinfo['conn_db'] = selectdb

        if (exectype == 'getkey'):
            query_results = dbapi.redis_query(1, connectinfo, rediskey)
        re = {'results':query_results}
        return Response(re)
