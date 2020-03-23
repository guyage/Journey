from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import status
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from user.permissions import CustomerPremission
from sqlorder.models import *
from sqlorder.serializers import *
from db.models import MySQLInst
# from workflow.models import ApprovalGroup
from utils.db_api import db_api
import time,datetime
from utils.get_config import get_conf

class SqlOrderTypeViewSet(viewsets.ModelViewSet):
    """
    list:
        SQL工单类型列表.
    create:
        创建SQL工单类型.
    delete:
        删除SQL工单类型.
    update:
        修改SQL工单类型.
    """
    
    queryset = SqlOrderType.objects.all().order_by('id')
    serializer_class = SqlOrderTypeSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('ordertype',)
    ordering_fields = ('id',)
    # 权限相关
    permission_classes = [CustomerPremission,]
    module_perms = ['sqlorder:sqlordertype']

class SqlTextViewSet(viewsets.ModelViewSet):
    """
    list:
        SqlText列表.
    create:
        创建SqlText.
    delete:
        删除SqlText.
    update:
        修改SqlText.
    """
    
    queryset = SqlText.objects.all().order_by('id')
    serializer_class = SqlTextSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    # search_fields = ('ordertype',)
    # ordering_fields = ('id',)
    # 权限相关
    permission_classes = [CustomerPremission,]
    module_perms = ['sqlorder:sqltext']

class SqlFileViewSet(viewsets.ModelViewSet):
    """
    list:
        SqlFile列表.
    create:
        创建SqlFile.
    delete:
        删除SqlFile.
    update:
        修改SqlFile.
    """
    
    queryset = SqlFile.objects.all().order_by('id')
    serializer_class = SqlFileSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    # search_fields = ('ordertype',)
    # ordering_fields = ('id',)
    # 权限相关
    permission_classes = [CustomerPremission,]
    module_perms = ['sqlorder:sqlfile']

class SqlOrderViewSet(viewsets.ModelViewSet):
    """
    list:
        SQL工单列表.
    create:
        创建SQL工单.
    delete:
        删除SQL工单.
    update:
        修改SQL工单.
    """
    
    queryset = SqlOrder.objects.all().order_by('id')
    serializer_class = SqlOrderSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('ordertype',)
    ordering_fields = ('id',)
    # 权限相关
    permission_classes = [CustomerPremission,]
    module_perms = ['sqlorder:sqlorder']

    def create(self, request, *args, **kwargs):
        # 获取请求数据
        sqlorder_data = request.data
        # 添加初始状态及下一级审核组
        sqlorder_data['status'] = 0
        ordertype_id = sqlorder_data['ordertype']
        ordertype_info = SqlOrderType.objects.get(Q(id=ordertype_id))
        # 获取sqlorder类型是否为可以上传附件
        is_file = ordertype_info.is_file
        sqlorder_data['approver_group'] = ordertype_info.first_approver.id
        serializer = self.get_serializer(data=sqlorder_data)
        serializer.is_valid(raise_exception=True)
        try:
            # 存储sqlorder
            self.perform_create(serializer)
            sqlorder_id = serializer.data['id']
            # 存储sqlorderstate
            SqlOrderState.objects.create(sqlorder_id_id=sqlorder_id,action='create',status='success',operator=serializer.data['operator'])
            if (is_file == 'DISABLED'):
                # 获取sql内容及存储sqltext
                sql_data = request.data['sql_data']['sqlcontent']
                for sql in sql_data:
                    SqlText.objects.create(sqlorder_id_id=sqlorder_id,instid_id=sql['dbname'][0],dbname=sql['dbname'][1],sqltext=sql['sqltext'],sqlstatus=0)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        # 获取工单类型
        ordertypeinfo = [(1,'create')]
        sqlordertype = instance.ordertype
        ordertype_approver = SqlOrderType.objects.values('first_approver','second_approver','dba_approver').get(Q(id=sqlordertype.id))
        # 获取工单类型是否有附件
        is_file = SqlOrderType.objects.values('is_file').get(Q(id=sqlordertype.id))
        is_file['is_file']
        # 生成工单流程步骤
        for k,v in ordertype_approver.items():
                if (v):
                    ordertypeinfo.append((ordertypeinfo[-1][0]+1,k))
        ordertypeinfo.append((ordertypeinfo[-1][0]+1,'exec'))
        ordertypeinfo.append((ordertypeinfo[-1][0]+1,'check'))
        ordertypeinfo.append((ordertypeinfo[-1][0]+1,'done'))
        # 获取当前工单步骤
        sqlorder_states = instance.sqlorder_state.all().values('action').order_by('-id')[:1]
        laste_state = sqlorder_states[0]['action']
        # 判断当前步骤所处位置及下一步步骤
        for step in ordertypeinfo:
            if (step[1] == laste_state):
                current_step_index = ordertypeinfo.index(step) + 1
        current_step = ordertypeinfo[current_step_index][1]
        next_step = ordertypeinfo[current_step_index+1][1]
        # 获取请求数据 && 定义修改数据
        change_data = {}
        action = request.data['action']
        change_data['operator'] = request.data['operator']
        sqlorder_id = request.data['id']
        approver_group_id = 'NULL'
        if (action == 'agree'):
            if (current_step == 'first_approver'):
                if (next_step == 'dba_approver'):
                    change_data['status'] = 3
                    step_status = 'success'
                    approver_group_id = ordertype_approver[next_step]
                elif (next_step == 'second_approver'):
                    change_data['status'] = 0
                    step_status = 'success'
                    approver_group_id = ordertype_approver[next_step]
            elif (current_step == 'second_approver'):
                if (next_step == 'dba_approver'):
                    change_data['status'] = 3
                    step_status = 'success'
                    approver_group_id = ordertype_approver[next_step]
            elif (current_step == 'dba_approver'):
                change_data['status'] = 4
                step_status = 'success'
                approver_group_id = ordertype_approver[current_step]
            elif (current_step == 'exec'):
                exectype = request.data['exectype']
                if (is_file['is_file'] == 'ENABLED'):
                    if (exectype == 'manual'):
                        change_data['status'] = 5
                        step_status = 'success'
                        approver_group_id = ''
                        request.data['operator'] = 'inception'
                else:
                    if (exectype == 'manual'):
                        change_data['status'] = 5
                        step_status = 'success'
                        approver_group_id = ''
                        request.data['operator'] = 'inception'
                    elif (exectype == 'auto'):
                        change_data['status'] = 5
                        approver_group_id = ''
                        request.data['operator'] = 'inception'
                        # 调用inception执行
                        iserror = self.inception_exec(sqlorder_id)
                        # 判断inception执行结果是否成功
                        if (iserror == 0):
                            step_status = 'success'
                            change_data['status'] = 5
                        elif (iserror > 0):
                            step_status = 'error'
                            change_data['status'] = -1
            elif (current_step == 'check'):
                checktype = request.data['checktype']
                if (checktype == 'success'):
                    change_data['status'] = 6
                    step_status = 'success'
                    approver_group_id = ''
                elif (checktype == 'error'):
                    change_data['status'] = -1
                    step_status = 'error'
                    approver_group_id = ''
        elif (action == 'reject'):
            change_data['status'] = 1
            approver_group_id = ''
            step_status = 'error'
        # change_data['ordertype'] = ordertype_approver[next_step]
        try:
            serializer = self.get_serializer(instance, data=change_data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            # print (serializer.data)
            SqlOrder.objects.filter(id=serializer.data['id']).update(approver_group_id=approver_group_id)
            # 添加sqlorder步骤记录
            SqlOrderState.objects.create(sqlorder_id_id=sqlorder_id,action=current_step,status=step_status,operator=request.data['operator'])
            # 如果开发验证通过，关闭sql工单，并添加记录
            if (current_step == 'check'):
                if (step_status == 'success'):
                    # 添加sqlorder步骤记录
                    SqlOrderState.objects.create(sqlorder_id_id=sqlorder_id,action=next_step,status=step_status,operator='系统')
                    SqlOrder.objects.filter(id=serializer.data['id']).update(approver_group_id='',status=2)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def inception_exec(self,sqlorderid):
        # inception连接信息
        inception_info = {'conn_host':'','conn_port':'','conn_user':'','conn_passwd':''}
        inception_info['conn_host'] = get_conf('inception','inc_host')
        inception_info['conn_port'] = get_conf('inception','inc_port')
        inception_info['conn_user'] = get_conf('inception','inc_user')
        inception_info['conn_passwd'] = get_conf('inception','inc_password')
        dbapi = db_api()
        sqlorder = SqlOrder.objects.get(Q(id=sqlorderid))
        sqlordererror = 0
        for sqlinfo in sqlorder.sqlorder_sqltext.all():
            # 执行sql信息
            # 执行数据库
            dbname = sqlinfo.dbname
            instinfo = sqlinfo.instid
            # sql
            sql = sqlinfo.sqltext
            exec_sql = '/*--user=%s;--password=%s;--host=%s;--enable-execute;--enable-remote-backup;--port=%d;*/inception_magic_start;use %s;%sinception_magic_commit;' % (instinfo.manage_user,instinfo.manage_userpwd,instinfo.inst_host, instinfo.inst_port, dbname,sql)
            col,results = dbapi.inception(inception_info,exec_sql)
            sqlexecstatus = 1
            
            for info in results:
                if (info['errlevel'] != 0):
                    sqlordererror = sqlordererror + 1
                    sqlexecstatus = -1
            SqlText.objects.filter(Q(id=sqlinfo.id)).update(info=results,sqlstatus=sqlexecstatus)
        return sqlordererror
        
class MySqlOrderViewSet(APIView):
    # 权限相关
    permission_classes = [CustomerPremission,]
    module_perms = ['sqlorder:mysqlorder']
    def get(self,request,format=None):
        username = self.request.user.username
        results = []
        mysqlorders = SqlOrder.objects.filter(Q(creator=self.request.user.username)).order_by('-id')
        for mysqlorder in mysqlorders:
            mysqlorder_serializer = SqlOrderSerializer(mysqlorder)
            results.append(mysqlorder_serializer.data)
        re = { 'results': '',}
        re['results'] = results
        return Response(re)

class ToDoSqlOrderViewSet(APIView):
    # 权限相关
    permission_classes = [CustomerPremission,]
    module_perms = ['sqlorder:todosqlorder']
    def get(self,request,format=None):
        userinfo = self.request.user
        username = userinfo.username
        results = []
        # 获取用户所在的审批组
        approver_group = userinfo.approver_user.all().values('id').distinct()
        user_approver_groups = []
        for approver_group_id in approver_group:
            user_approver_groups.append(approver_group_id['id'])
        # 获取用户的待办工单
        todosqlorders = SqlOrder.objects.filter(Q(approver_group_id__in=user_approver_groups)|Q(status=5,creator=username)).order_by('-id')
        for todosqlorder in todosqlorders:
            todosqlorder_serializer = SqlOrderSerializer(todosqlorder)
            results.append(todosqlorder_serializer.data)
        re = { 'results': '',}
        re['results'] = results
        return Response(re)

class SqlOrderDetailViewSet(APIView):
    # 权限相关
    permission_classes = [CustomerPremission,]
    module_perms = ['sqlorder:sqlorderdetail']
    def post(self,request,format=None):
        # username = request.data['username']
        sqlorderid = request.data['sqlorderid']
        sqlorderdetail = SqlOrder.objects.get(Q(id=sqlorderid))
        sqlorderdetail_serializer = SqlOrderDetailSerializer(sqlorderdetail)

        return Response(sqlorderdetail_serializer.data)


class InceptionViewSet(APIView):
    # 权限相关
    permission_classes = [CustomerPremission,]
    module_perms = ['sqlorder:inception']
    def post(self,request,format=None):
        result = { 'col': '', 'results': ''}
        # inception连接信息
        inception_info = {'conn_host':'','conn_port':'','conn_user':'','conn_passwd':''}
        inception_info['conn_host'] = get_conf('inception','inc_host')
        inception_info['conn_port'] = get_conf('inception','inc_port')
        inception_info['conn_user'] = get_conf('inception','inc_user')
        inception_info['conn_passwd'] = get_conf('inception','inc_password')
        dbapi = db_api()
        inception_type = request.data['type']
        if (inception_type == 'check'):
            inception_sql_data = request.data['sql_data']
            inst_id = inception_sql_data['dbname'][0]
            dbname = inception_sql_data['dbname'][1]
            instinfo = MySQLInst.objects.get(Q(id=inst_id))
            sql = inception_sql_data['sqltext']
            check_sql= '/*--user=%s;--password=%s;--host=%s;--enable-check;--enable-remote-backup;--port=%d;*/inception_magic_start;use %s;%sinception_magic_commit;' % (instinfo.manage_user,instinfo.manage_userpwd,instinfo.inst_host, instinfo.inst_port, dbname,sql)
            print (check_sql)
            col,results = dbapi.inception(inception_info,check_sql)
            print (col,results)
            check_info = []
            for info in results:
                if (info['errlevel'] != 0):
                    check_info.append(info)
            result['col'] = col
            result['results'] = check_info
        return Response(result)

class AllSqlOrderViewSet(APIView):
    # 权限相关
    permission_classes = [CustomerPremission,]
    module_perms = ['sqlorder:allsqlorder']
    def get(self,request,format=None):
        userinfo = self.request.user
        username = userinfo.username
        results = []
        # 获取最近7天内的所有完成工单
        laste_time = (datetime.date.today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d %X')
        print (laste_time)
        allsqlorders = SqlOrder.objects.filter(create_time__gt=laste_time).order_by('-id')
        for sqlorder in allsqlorders:
            sqlorder_serializer = SqlOrderSerializer(sqlorder)
            results.append(sqlorder_serializer.data)
        re = { 'results': '',}
        re['results'] = results
        return Response(re)

    def post(self,request,format=None):
        userinfo = self.request.user
        username = userinfo.username
        results = []
        # 获取7天内的初始时间
        laste_time = (datetime.date.today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d %X')
        searchtype = request.data['searchtype']
        timerange = request.data['timerange']
        if (searchtype == 'my'):
            if (timerange):
                date_from = timerange[0]
                date_to = timerange[1]
                searchsqlorders = SqlOrder.objects.filter(Q(creator=self.request.user.username),Q(create_time__range=(date_from,date_to))).order_by('-id')
            else:
                searchsqlorders = SqlOrder.objects.filter(Q(creator=self.request.user.username),Q(create_time__gt=laste_time)).order_by('-id')
        elif (searchtype == 'time'):
            if (timerange):
                date_from = timerange[0]
                date_to = timerange[1]
                searchsqlorders = SqlOrder.objects.filter(Q(create_time__range=(date_from,date_to))).order_by('-id')
        for sqlorder in searchsqlorders:
            sqlorder_serializer = SqlOrderSerializer(sqlorder)
            results.append(sqlorder_serializer.data)
        re = { 'results': '',}
        re['results'] = results
        return Response(re)