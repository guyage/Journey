from django.shortcuts import render
from db.models import *
from db.serializers import *
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.views import APIView
from utils.db_api import db_api
from django.db.models import Q
from rest_framework.response import Response
from django.db.models.query import QuerySet
from rest_framework import status
from user.permissions import CustomerPremission
from utils.cryption import decypt
import os


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
    # 权限相关
    permission_classes = [CustomerPremission,]
    module_perms = ['db:mysqlinst']
    
    def create(self, request, *args, **kwargs):
        # de = decypt(os.environ.get("saltkey"))
        de = decypt(saltkey=None)
        manage_userpwd = request.data['manage_userpwd']
        read_userpwd = request.data['read_userpwd']
        request.data['manage_userpwd'] = de.get_encrypted_key(manage_userpwd)
        request.data['read_userpwd'] = de.get_encrypted_key(read_userpwd)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        de = decypt(saltkey=None)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if ('manage_userpwd' in request.data):
            manage_userpwd = request.data['manage_userpwd']
            request.data['manage_userpwd'] = de.get_encrypted_key(manage_userpwd)
        if ('read_userpwd' in request.data):
            read_userpwd = request.data['read_userpwd']
            request.data['read_userpwd'] = de.get_encrypted_key(read_userpwd)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    

class MongoDBInstViewSet(viewsets.ModelViewSet):
    """
    list:
        MongoDBInst.
    create:
        创建MongoDBInst.
    delete:
        删除MongoDBInst.
    update:
        修改MongoDBInst.
    """
    queryset = MongoDBInst.objects.all().order_by('id')
    serializer_class = MongoDBInstSerializer
    # pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('inst_name','inst_host','inst_port','role','services','comment')
    ordering_fields = ('id',)
    # 权限相关
    permission_classes = [CustomerPremission,]
    module_perms = ['db:mongodbinst']

    def create(self, request, *args, **kwargs):
        # de = decypt(os.environ.get("saltkey"))
        de = decypt(saltkey=None)
        manage_userpwd = request.data['manage_userpwd']
        read_userpwd = request.data['read_userpwd']
        request.data['manage_userpwd'] = de.get_encrypted_key(manage_userpwd)
        request.data['read_userpwd'] = de.get_encrypted_key(read_userpwd)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        de = decypt(saltkey=None)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if ('manage_userpwd' in request.data):
            manage_userpwd = request.data['manage_userpwd']
            request.data['manage_userpwd'] = de.get_encrypted_key(manage_userpwd)
        if ('read_userpwd' in request.data):
            read_userpwd = request.data['read_userpwd']
            request.data['read_userpwd'] = de.get_encrypted_key(read_userpwd)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

class RedisInstViewSet(viewsets.ModelViewSet):
    """
    list:
        RedisInst.
    create:
        创建RedisInst.
    delete:
        删除RedisInst.
    update:
        修改RedisInst.
    """
    queryset = RedisInst.objects.all().order_by('id')
    serializer_class = RedisInstSerializer
    # pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('inst_name','inst_host','inst_port','role','services','comment')
    ordering_fields = ('id',)
    # 权限相关
    permission_classes = [CustomerPremission,]
    module_perms = ['db:redisinst']

    def create(self, request, *args, **kwargs):
        # de = decypt(os.environ.get("saltkey"))
        de = decypt(saltkey=None)
        password = request.data['password']
        request.data['password'] = de.get_encrypted_key(password)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        de = decypt(saltkey=None)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if ('password' in request.data):
            password = request.data['password']
            request.data['password'] = de.get_encrypted_key(password)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

class UserAccessMySQLViewSet(viewsets.ModelViewSet):
    """
    数据库列表，分页，查找
    """
    
    queryset = UserAccessMySQL.objects.all().order_by('-id')
    serializer_class = UserAccessMySQLSerializer
    # pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('username','user_access_db','comment','status')
    ordering_fields = ('id',)
    # 权限相关
    permission_classes = [CustomerPremission,]
    module_perms = ['db:useraccessmysql']

    def create(self, request, *args, **kwargs):
        real_data = request.data
        for db in request.data['user_access_db']:
            userhavedb = UserAccessMySQL.objects.filter(Q(username=request.data['username']),Q(user_access_db=db),Q(mysqlinst=request.data['mysqlinst']),Q(status=1)|Q(status=2)).count()
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
                queryset = queryset.all().order_by('-id')
        else:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                # Ensure queryset is re-evaluated on each request.
                queryset = queryset.filter(Q(username=self.request.user.username)).order_by('-id')
        return queryset


class MySQLMetaViewSet(APIView):

    # 权限相关
    permission_classes = [CustomerPremission,]
    module_perms = ['db:mysqlmeta']

    def post(self,request,format=None):
        de = decypt(saltkey=None)
        dbapi = db_api()
        request_type = request.data['type']
        instid = request.data['instid']
        instinfo = MySQLInst.objects.get(Q(id=instid))
        # 获取连接信息
        connectinfo = {'conn_host':'','conn_port':'','conn_user':'','conn_passwd':'','conn_db':''}
        connectinfo['conn_host'] = instinfo.inst_host
        connectinfo['conn_port'] = instinfo.inst_port
        connectinfo['conn_user'] = instinfo.read_user
        connectinfo['conn_passwd'] = de.decryptV(instinfo.read_userpwd)
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

    # 权限相关
    permission_classes = [CustomerPremission,]
    module_perms = ['db:useraccessdb']

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
        elif (str(dbtype) == 'mongodbinst'):
            username = request.data['username']
            user_access_inst_count = UserAccessMongoDB.objects.filter(Q(username=username),Q(status=2)).values("mongodbinst_id").distinct().count()
            if (user_access_inst_count > 0):
                user_access_mongodbinst = []
                insts = UserAccessMongoDB.objects.filter(Q(username=username),Q(status=2)).values("mongodbinst_id").distinct()
                for inst in insts:
                    inst_id = inst['mongodbinst_id']
                    instinfo = MongoDBInst.objects.get(Q(id=inst_id))
                    user_access_mongodbinst.append({'instid':inst_id,'instname':instinfo.inst_name})
                    results = user_access_mongodbinst
            else:
                results = []
        elif (str(dbtype) == 'redisinst'):
            username = request.data['username']
            user_access_inst_count = UserAccessRedis.objects.filter(Q(username=username),Q(status=2)).values("redisinst_id").distinct().count()
            if (user_access_inst_count > 0):
                user_access_redisinst = []
                insts = UserAccessRedis.objects.filter(Q(username=username),Q(status=2)).values("redisinst_id").distinct()
                for inst in insts:
                    inst_id = inst['redisinst_id']
                    instinfo = RedisInst.objects.get(Q(id=inst_id))
                    user_access_redisinst.append({'instid':inst_id,'instname':instinfo.inst_name})
                    results = user_access_redisinst
            else:
                results = []
        re = { 'results': '',}
        re['results'] = results
        return Response(re)

class MySQLUserViewSet(APIView):
    # 权限相关
    permission_classes = [CustomerPremission,]
    module_perms = ['db:mysqluser']

    def post(self,request,format=None):
        de = decypt(saltkey=None)
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
        connectinfo['conn_passwd'] = de.decryptV(instinfo.manage_userpwd)
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
        return Response(re)

class MySQLStatusViewSet(APIView):
    # 权限相关
    permission_classes = [CustomerPremission,]
    module_perms = ['db:mysqlstatus']

    def post(self,request,format=None):
        de = decypt(saltkey=None)
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
        connectinfo['conn_passwd'] = de.decryptV(instinfo.manage_userpwd)
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

class UserAccessMongoDBViewSet(viewsets.ModelViewSet):
    """
    数据库列表，分页，查找
    """
    
    queryset = UserAccessMongoDB.objects.all().order_by('-id')
    serializer_class = UserAccessMongoDBSerializer
    # pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('username','comment','status')
    ordering_fields = ('id',)

    # 权限相关
    permission_classes = [CustomerPremission,]
    module_perms = ['db:useraccessmongodb']

    def create(self, request, *args, **kwargs):
        real_data = request.data
        userhavedb = UserAccessMongoDB.objects.filter(Q(username=request.data['username']),Q(mongodbinst=request.data['mongodbinst']),Q(status=1)|Q(status=2)).count()
        if (userhavedb == 0):
            serializer = self.get_serializer(data=real_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            useraccessdata = UserAccessMongoDB.objects.get(id=serializer.data['id'])
            useraccessdata.mongodbinst_id = request.data['mongodbinst']
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
                queryset = queryset.all().order_by('-id')
        else:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                # Ensure queryset is re-evaluated on each request.
                queryset = queryset.filter(Q(username=self.request.user.username)).order_by('-id')
        return queryset

class UserAccessRedisViewSet(viewsets.ModelViewSet):
    """
    数据库列表，分页，查找
    """
    
    queryset = UserAccessRedis.objects.all().order_by('-id')
    serializer_class = UserAccessRedisSerializer
    # pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('username','comment','status')
    ordering_fields = ('id',)
    # 权限相关
    permission_classes = [CustomerPremission,]
    module_perms = ['db:useraccessredis']


    def create(self, request, *args, **kwargs):
        real_data = request.data
        userhavedb = UserAccessRedis.objects.filter(Q(username=request.data['username']),Q(redisinst=request.data['redisinst']),Q(status=1)|Q(status=2)).count()
        if (userhavedb == 0):
            serializer = self.get_serializer(data=real_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            useraccessdata = UserAccessRedis.objects.get(id=serializer.data['id'])
            useraccessdata.redisinst_id = request.data['redisinst']
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
                queryset = queryset.all().order_by('-id')
        else:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                # Ensure queryset is re-evaluated on each request.
                queryset = queryset.filter(Q(username=self.request.user.username)).order_by('-id')
        return queryset