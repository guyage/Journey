from django.shortcuts import render
from django.core import serializers
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import viewsets
from utils.db_api import db_api
import json,datetime,time
from db.models import *
from conf.models import *
from query.models import *
from query.serializers import *
import re
from utils.cryption import decypt
from user.permissions import CustomerPremission
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
import logging
# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)
# 生成一个名为collect的logger实例
collect_logger = logging.getLogger("collect")


class QuerySqlLogViewSet(viewsets.ModelViewSet):
    """
    list:
        SQL查询日志表.
    """
    # 权限相关
    permission_classes = [CustomerPremission,IsAuthenticated]
    module_perms = ['query:querysqllog']
    
    queryset = QuerySqlLog.objects.all().order_by('id')
    serializer_class = QuerySqlLogSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('operator','dbname','sql')
    ordering_fields = ('id',)

class QuerySqlViewSet(APIView):
    """
        QuerySql.
    """

    # 权限相关
    permission_classes = [CustomerPremission,IsAuthenticated]
    module_perms = ['query:querysql']
    def post(self,request,format=None):
        de = decypt(saltkey=None)
        userinfo = self.request.user
        username = userinfo.username
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
        connectinfo['conn_passwd'] = de.decryptV(instinfo.read_userpwd)
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
                    QuerySqlLog.objects.create(operator=username,mysqlinst=instinfo,dbname=dbname,sql=limit_sql)
                else:
                    col,results = dbapi.mysql_query(connectinfo,limit_sql)
                    QuerySqlLog.objects.create(operator=username,mysqlinst=instinfo,dbname=dbname,sql=limit_sql)
            else:
                col,results = dbapi.mysql_query(connectinfo,limit_sql,default_limit)
                QuerySqlLog.objects.create(operator=username,mysqlinst=instinfo,dbname=dbname,sql=limit_sql)
            
            # whitelist_tables = set(dump_white_list.split(","))
            # difftables = execsqltables - whitelist_tables
            # if (len(difftables) > 0):
            #     col,results = dbapi.mysql_query(connectinfo,limit_sql,islimit)
            # else:
            #     col,results = dbapi.mysql_query(connectinfo,limit_sql)
        elif (exectype == 'explain'):
            explain_sql = 'explain %s' % sql
            col,results = dbapi.mysql_query(connectinfo,explain_sql)
        result = { 'col': '', 'results': '',}
        if (len(results) > 0):
            if (results[0] != 'error'):
                for i in results:
                    for k,v in i.items():
                        if(isinstance(v,int)):
                            i[k] = str(v)
        # real_results = []
        # for i in results:
        #     new_item = {}
        #     for k,v in i.items():
        #         if ('.' in k):
        #             new_item[k.replace('.','_')] = v
        #         else:
        #             new_item[k] = v
        #     real_results.append(new_item)
        result['col'] = col
        result['results'] = results
        return Response(result)

class QueryMongodbViewSet(APIView):
    # 权限相关
    permission_classes = [CustomerPremission,IsAuthenticated]
    module_perms = ['query:querymongodb']
    def post(self,request,format=None):
        de = decypt(saltkey=None)
        try:
            limitinfo = QueryLimit.objects.get(Q(query_type='mongodb'))
        except:
            limitinfo = None
        if (limitinfo):
            default_limit = str(limitinfo.query_limit)
        else:
            default_limit = '10'
        dbapi = db_api()
        exectype = request.data['exectype']
        instid = request.data['instid']
        instinfo = MongoDBInst.objects.get(Q(id=instid))
        # instinfo = dbinfo.mongodbinst_id
        # instinfo = MongodbInst.objects.get(Q(id=instid))
        connectinfo = {'conn_host':'','conn_port':'','conn_user':'','conn_passwd':'','conn_db':''}
        connectinfo['conn_host'] = instinfo.inst_host
        connectinfo['conn_port'] = instinfo.inst_port
        connectinfo['conn_user'] = instinfo.read_user
        connectinfo['conn_passwd'] = de.decryptV(instinfo.read_userpwd)
        if (exectype == 'db'):
            query_results = dbapi.mongodb_query(0, connectinfo)
        elif (exectype == 'collection'):
            collectionname = request.data['collectionname']
            connectinfo['conn_db'] = collectionname
            query_results = dbapi.mongodb_query(1, connectinfo)
        elif (exectype == 'sql'):
            # username = request.data['username']
            collectionname = request.data['collectionname']
            connectinfo['conn_db'] = collectionname
            sql = request.data['sql']
            if 'limit' in sql.lower():
                lower_sql = sql.lower()
                p1 = re.compile(r'[(](.*?)[)]', re.S)
                for i in lower_sql.split('.'):
                    if 'limit' in i:
                        sql_limit = int(list(map(int, re.findall(p1, i)))[0])
                if (sql_limit >= 500):
                    limit_sql = sql + '.limit(' + default_limit + ')'
                else:
                    limit_sql = sql
            else:
                limit_sql = sql + '.limit(' + default_limit + ')'
            query_results = dbapi.mongodb_query(2, connectinfo, limit_sql)
        # query_results = dbapi.mongodb_query(1, connectinfo)
        result = {'results':query_results}
        return Response(result)

class QueryRedisViewSet(APIView):
    # 权限相关
    permission_classes = [CustomerPremission,IsAuthenticated]
    module_perms = ['query:queryredis']
    def post(self,request,format=None):
        de = decypt(saltkey=None)
        dbapi = db_api()
        exectype = request.data['exectype']
        redisinst = request.data['selectredis']
        selectdb = request.data['selectdb']
        rediskey = request.data['rediskey']
        instinfo = RedisInst.objects.get(Q(id=redisinst))
        connectinfo = {'conn_host':'','conn_port':'','conn_passwd':'','conn_db':''}
        connectinfo['conn_host'] = instinfo.inst_host
        connectinfo['conn_port'] = instinfo.inst_port
        connectinfo['conn_passwd'] = de.decryptV(instinfo.password)
        connectinfo['conn_db'] = selectdb

        if (exectype == 'getkey'):
            query_results = dbapi.redis_query(1, connectinfo, rediskey)
        re = {'results':query_results}
        return Response(re)