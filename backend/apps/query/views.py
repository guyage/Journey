from django.shortcuts import render
from django.core import serializers
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from api.db_api import db_api
import json,datetime,time
from db.models import *
from conf.models import *

class QuerySqlViewSet(APIView):

    def post(self,request,format=None):
        try:
            limitinfo = QueryLimit.objects.get(Q(query_type='mysql'))
        except:
            limitinfo = None
        if (limitinfo):
            default_limit = str(limitinfo.query_limit)
        else:
            default_limit = '100'
        dbapi = db_api()
        instid = request.data['instid']
        dbname = request.data['dbname']
        instinfo = MySQLInst.objects.get(Q(id=instid))
        connectinfo = {'conn_host':'','conn_port':'','conn_user':'','conn_passwd':'','conn_db':''}
        connectinfo['conn_host'] = instinfo.inst_host
        connectinfo['conn_port'] = instinfo.inst_port
        connectinfo['conn_user'] = instinfo.read_user
        connectinfo['conn_passwd'] = instinfo.read_userpwd
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
            username = request.data['username']
            execsqltables = dbapi.extract_table_name_from_sql(sql)
            try:
                white_table = DumpWhiteList.objects.get(Q(white_user=username)).white_table
            except:
                white_table = None
            if (white_table):
                whitelist_tables = set(white_table.split(","))
                difftables = execsqltables - whitelist_tables
                if (len(difftables) > 0):
                    col,results = dbapi.mysql_query(connectinfo,limit_sql,default_limit)
                else:
                    col,results = dbapi.mysql_query(connectinfo,limit_sql)
            else:
                col,results = dbapi.mysql_query(connectinfo,limit_sql,default_limit)
            # whitelist_tables = set(dump_white_list.split(","))
            # difftables = execsqltables - whitelist_tables
            # if (len(difftables) > 0):
            #     col,results = dbapi.mysql_query(connectinfo,limit_sql,islimit)
            # else:
            #     col,results = dbapi.mysql_query(connectinfo,limit_sql)
        elif (exectype == 'explain'):
            explain_sql = 'explain %s' % sql
            col,results = dbapi.mysql_query(connectinfo,explain_sql)
        re = { 'col': '', 'results': '',}      
        re['col'] = col
        re['results'] = results
        return Response(re)
