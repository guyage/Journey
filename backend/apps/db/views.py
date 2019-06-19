from django.shortcuts import render
from db.models import *
from db.serializers import *
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.views import APIView
from api.db_api import db_api
from django.db.models import Q
from rest_framework.response import Response
from django.db.models.query import QuerySet
from rest_framework import status


class MySQLInstViewSet(viewsets.ModelViewSet):
    """
    list:
        MySQLInst列表.
    create:
        创建MySQLInst.
    delete:
        删除MySQLInst.
    update:
        修改MySQLInst.
    """
    queryset = MySQLInst.objects.all().order_by('id')
    serializer_class = MySQLInstSerializer
    # pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('inst_name','inst_host','inst_port','role','services','comment')
    ordering_fields = ('id',)

class UserAccessMySQLViewSet(viewsets.ModelViewSet):
    """
    数据库列表，分页，查找
    """
    
    queryset = UserAccessMySQL.objects.all().order_by('id')
    serializer_class = UserAccessMySQLSerializer
    # pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('username','user_access_db','comment',)
    ordering_fields = ('id',)

    def create(self, request, *args, **kwargs):
        real_data = request.data
        for db in request.data['user_access_db']:
            userhavedb = UserAccessMySQL.objects.filter(Q(username=request.data['username']),Q(user_access_db=db),Q(status=1)|Q(status=2)).count()
            if (userhavedb == 0):
                real_data['user_access_db'] = db
                serializer = self.get_serializer(data=real_data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                useraccessdata = UserAccessMySQL.objects.get(id=serializer.data['id'])
                useraccessdata.mysqlinst_id = request.data['mysqlinst']
                useraccessdata.save()
                headers = self.get_success_headers(serializer.data)
            else:
                return Response({'message':'请勿重复申请'},status=500)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        if (self.request.user.is_superuser):
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                # Ensure queryset is re-evaluated on each request.
                queryset = queryset.all()
        else:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                # Ensure queryset is re-evaluated on each request.
                queryset = queryset.filter(Q(username=self.request.user.username))
        return queryset


class MySQLMetaViewSet(APIView):

    def post(self,request,format=None):
        dbapi = db_api()
        request_type = request.data['type']
        instid = request.data['instid']
        instinfo = MySQLInst.objects.get(Q(id=instid))
        # 获取连接信息
        connectinfo = {'conn_host':'','conn_port':'','conn_user':'','conn_passwd':'','conn_db':''}
        connectinfo['conn_host'] = instinfo.inst_host
        connectinfo['conn_port'] = instinfo.inst_port
        connectinfo['conn_user'] = instinfo.read_user
        connectinfo['conn_passwd'] = instinfo.read_userpwd
        if (str(request_type) == 'database'):
            instid = request.data['instid']
            col,results = dbapi.get_metadata(0,connectinfo)
        elif (str(request_type) == 'table'):
            dbname = request.data['dbname']
            col,results = dbapi.get_metadata(1,connectinfo,dbname)
        elif (str(request_type) == 'tablemeta'):
            dbname = request.data['dbname']
            tablename = request.data['tablename']
            col,results = dbapi.get_metadata(2,connectinfo,dbname,tablename)
        re = { 'col': '', 'results': '',}
        re['col'] = col
        re['results'] = results
        return Response(re)

class UserAccessDbViewSet(APIView):

    def post(self,request,format=None):

        dbtype = (request.data['dbtype'])

        if (str(dbtype) == 'mysqlinst'):
            user_access_mysqlinst = []
            username = request.data['username']
            user_access_inst_count = UserAccessMySQL.objects.filter(Q(username=username),Q(status=2)).values("mysqlinst_id").distinct().count()
            if (user_access_inst_count > 0):
                insts = UserAccessMySQL.objects.filter(Q(username=username),Q(status=2)).values("mysqlinst_id").distinct()
                for inst in insts:
                    inst_id = inst['mysqlinst_id']
                    dbs = UserAccessMySQL.objects.filter(Q(username=username),Q(status=2),Q(mysqlinst_id=inst_id)).values("user_access_db").distinct()
                    instinfo = MySQLInst.objects.get(Q(id=inst_id))
                    # user_access_mysqlinst.append({'id':inst_id,'label':instinfo.inst_name,'type':'inst'})
                    user_access_mysqlinst.append({'instid':inst_id,'instname':instinfo.inst_name})
                    results = user_access_mysqlinst
            else:
                results = []
        elif (str(dbtype) == 'mysqldb'):
            user_access_mysqldb = []
            mysqlinst = request.data['mysqlinst']
            username = request.data['username']
            dbs = UserAccessMySQL.objects.filter(Q(username=username),Q(status=2),Q(mysqlinst_id=mysqlinst['id'])).values("user_access_db").distinct()
            for db in dbs:
                # user_access_mysqldb.append({'label':db['user_access_db'],'type':'db'})
                user_access_mysqldb.append({'dbname':db['user_access_db']})
            results = user_access_mysqldb
        re = { 'results': '',}
        re['results'] = results
        return Response(re)

class MySQLUserViewSet(APIView):

    def post(self,request,format=None):
        dbapi = db_api()
        instid = request.data['instid']
        request_type = request.data['type']
        # dbinfo = MySQLDatabase.objects.get(Q(dbname=dbname))
        instinfo = MySQLInst.objects.get(Q(id=instid))
        # 获取连接信息
        connectinfo = {'conn_host':'','conn_port':'','conn_user':'','conn_passwd':'','conn_db':''}
        connectinfo['conn_host'] = instinfo.inst_host
        connectinfo['conn_port'] = instinfo.inst_port
        connectinfo['conn_user'] = instinfo.manage_user
        connectinfo['conn_passwd'] = instinfo.manage_userpwd
        connectinfo['conn_db'] = 'mysql'
        col,dblists = dbapi.get_metadata(0,connectinfo)
        dblist = []
        for i in dblists:
            dblist.append(i['table_schema'])
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

class MySQLStatusViewSet(APIView):

    def post(self,request,format=None):
        dbapi = db_api()
        instid = request.data['instid']
        request_type = request.data['type']
        # dbinfo = MySQLDatabase.objects.get(Q(dbname=dbname))
        instinfo = MySQLInst.objects.get(Q(id=instid))
        # 获取连接信息
        connectinfo = {'conn_host':'','conn_port':'','conn_user':'','conn_passwd':'','conn_db':''}
        connectinfo['conn_host'] = instinfo.inst_host
        connectinfo['conn_port'] = instinfo.inst_port
        connectinfo['conn_user'] = instinfo.manage_user
        connectinfo['conn_passwd'] = instinfo.manage_userpwd
        connectinfo['conn_db'] = 'information_schema'
        # 查询关键字
        col = []
        results = []
        if ( str(request_type) == 'full'):
            col,results = dbapi.get_metadata(6,connectinfo)
        elif ( str(request_type) == 'active'):
            col,results = dbapi.get_metadata(7,connectinfo)
        elif ( str(request_type) == 'innodb'):
            col,results = dbapi.get_metadata(8,connectinfo)
        elif ( str(request_type) == 'master'):
            col,results = dbapi.get_metadata(9,connectinfo)
        elif ( str(request_type) == 'slave'):
            col,results = dbapi.get_metadata(10,connectinfo)
        elif ( str(request_type) == 'kill'):
            sessionid = request.data['sessionid']
            killsql = "kill %s;" % (sessionid)
            col,results = dbapi.mysql_query(connectinfo,killsql)
        re = { 'col': '', 'results': ''}
        re['col'] = col
        re['results'] = results
        return Response(re)