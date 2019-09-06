from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models.query import QuerySet
from django.db.models import Q
from rest_framework import status
from rest_framework import filters
from workflow.models import *
from user.permissions import CustomerPremission
from workflow.serializers import *
from api.git_api import GitLabAPI
from api.workflow_api import exec_cmd
import json
from api.send_mail import send_mail

class WorkOrderTypeViewSet(viewsets.ModelViewSet):
    """
    list:
        工单类型列表.
    create:
        创建工单类型.
    delete:
        删除工单类型.
    update:
        修改工单类型.
    """
    
    queryset = WorkOrderType.objects.all().order_by('id')
    serializer_class = WorkOrderTypeSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('ordertype',)
    ordering_fields = ('id',)
    # 权限相关
    permission_classes = [CustomerPremission,]
    module_perms = ['workflow:workordertype']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        ordertype_id = serializer.data['id']
        WorkOrderStep.objects.create(step_id=1,ordertype_id=ordertype_id,step_name='start')
        WorkOrderStep.objects.create(step_id=2,ordertype_id=ordertype_id,step_name='finsh')
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ApprovalGroupViewSet(viewsets.ModelViewSet):
    """
    list:
        工单审批组列表.
    create:
        创建工单审批组.
    delete:
        删除工单审批组.
    update:
        修改工单审批组.
    """
    
    queryset = ApprovalGroup.objects.all().order_by('id')
    serializer_class = ApprovalGroupSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('approver_group_name',)
    ordering_fields = ('id',)
    # 权限相关
    permission_classes = [CustomerPremission,]
    module_perms = ['workflow:approvergroup']

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        userselected = request.data['userselected']
        instance.users.set(userselected)
        return Response(serializer.data)

class WorkOrderStepViewSet(viewsets.ModelViewSet):
    """
    list:
        工单步骤列表.
    create:
        创建工单步骤.
    delete:
        删除工单步骤.
    update:
        修改工单步骤.
    """
    
    queryset = WorkOrderStep.objects.all().order_by('id')
    serializer_class = WorkOrderStepSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('step_id',)
    ordering_fields = ('id',)
    # 权限相关
    permission_classes = [CustomerPremission,]
    module_perms = ['workflow:workorderstep']

    def create(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        # # serializer.is_valid(raise_exception=True)
        # # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        WorkOrderStep.objects.create(**request.data)
        finsh_new_step_id = request.data['step_id'] + 1
        finsh_step = WorkOrderStep.objects.filter(Q(step_name='finsh'),Q(ordertype_id=request.data['ordertype_id'])).update(step_id=finsh_new_step_id)
        return Response(status=status.HTTP_201_CREATED)

class WorkOrderViewSet(viewsets.ModelViewSet):
    """
    工单
    """
    queryset = WorkOrder.objects.all().order_by('-id')
    serializer_class = WorkOrderSerializer
    # pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('title')
    ordering_fields = ('id',)
    # 权限相关
    permission_classes = [CustomerPremission,]
    module_perms = ['workflow:workorder']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        ordertype_id = serializer.data['ordertype']
        # 获取下一步骤的审批组
        approver_group_id = WorkOrderStep.objects.get(Q(ordertype_id=ordertype_id),Q(step_id=2)).approver_group_id
        workorder_id = serializer.data['id']
        workorder_operator = serializer.data['operator']
        WorkOrder.objects.filter(id=workorder_id).update(approver_group_id=approver_group_id)
        # 获取下一步骤审批组相关用户发送邮件通知
        try:
            mailtolist = []
            userlist = ApprovalGroup.objects.get(Q(id=approver_group_id)).users.all()
            for user in userlist:
                mailtolist.append(user.email)
            print (mailtolist)
            maildata = json.loads(serializer.data['content'])
            send_mail(mailtolist,4,maildata)
        except:
            pass
        # 插入创建工单步骤记录
        WorkOrderState.objects.create(wordorder_id_id=workorder_id,step=1,action='start',operator=workorder_operator)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        # 修改工单状态
        self.perform_update(serializer)
        # 获取工单类型信息
        workorder_type_id = serializer.data['ordertype']
        ordertypesteps_count = WorkOrderType.objects.get(id=workorder_type_id).ordertype_step.all().count()
        # 获取工单信息
        have_steps = instance.state_wordorder_id.all().count()
        workorder_id = serializer.data['id']
        status = request.data['status']
        step = have_steps + 1
        operator = serializer.data['operator']
        if (status == 2):
            #插入工单步骤
            WorkOrderState.objects.create(wordorder_id_id=workorder_id,step=step,action='同意',operator=operator)
            # 判断同意之后是否该系统自动执行(即判断是否为结束前一步)
            is_end = ordertypesteps_count - step
            if (is_end == 1):
                # 执行脚本
                script_cmd = []
                script = WorkOrderType.objects.get(id=workorder_type_id).script
                content = serializer.data['content']
                script_cmd.append('python')
                script_cmd.append(script)
                script_cmd.append(content)
                exec_status = exec_cmd(script_cmd)
                # 判断执行脚本是否成功
                end_step = step + 1
                if ('success' in str(exec_status,encoding="utf8")):
                    # 成功后改变工单状态
                    WorkOrder.objects.filter(id=workorder_id).update(approver_group_id='',status=3)
                    WorkOrderState.objects.create(wordorder_id_id=workorder_id,step=end_step,action='finsh',operator='系统')
                elif ('fail' in str(exec_status,encoding="utf8")):
                    WorkOrder.objects.filter(id=workorder_id).update(approver_group_id='',status=-1)
                    WorkOrderState.objects.create(wordorder_id_id=workorder_id,step=end_step,action='finsh',operator='系统')
            else:
                # 不是结束前一步，获取下一步骤的审批组
                approver_group_id = WorkOrderStep.objects.get(Q(ordertype_id=workorder_type_id),Q(step_id=step)).approver_group_id
                WorkOrder.objects.filter(id=workorder_id).update(approver_group_id=approver_group_id)
        elif (status == 4):
            #插入工单步骤
            WorkOrderState.objects.create(wordorder_id_id=workorder_id,step=step,action='驳回',operator=operator)
        
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    

class WorkOrderDetailViewSet(APIView):
    # 权限相关
    permission_classes = [CustomerPremission,]
    module_perms = ['workflow:workorderdetail']
    def post(self,request,format=None):
        # username = request.data['username']
        workorderid = request.data['workorderid']
        workorderdetail = WorkOrder.objects.get(Q(id=workorderid))
        workorderdetail_serializer = WorkOrderSerializer(workorderdetail)

        return Response(workorderdetail_serializer.data)


class GitLabInfoViewSet(APIView):

    def post(self,request,format=None):
        git_api = GitLabAPI()
        reqtype = request.data['reqtype']
        if (reqtype == 'projects'):
            projects = git_api.get_all_projects()
            results = projects
        elif (reqtype == 'groups'):
            groups = git_api.get_all_groups()
            results = groups
        elif (reqtype == 'users'):
            users = git_api.get_all_users()
            results = users
        re = { 'results': '',}      
        re['results'] = results
        
        return Response(re)

class ToDoWorkOrderViewSet(APIView):

    def get(self,request,format=None):
        userinfo = self.request.user
        results = []
        approver_group = userinfo.approver_user.all().values('id').distinct()
        user_approver_groups = []
        for approver_group_id in approver_group:
            user_approver_groups.append(approver_group_id['id'])
        todoworkorders = WorkOrder.objects.filter(Q(approver_group_id__in=user_approver_groups)).order_by('-id')
        for todoworkorder in todoworkorders:
            todoworkorder_serializer = WorkOrderSerializer(todoworkorder)
            results.append(todoworkorder_serializer.data)
        re = { 'results': '',}
        re['results'] = results
        return Response(re)

class MyWorkOrderViewSet(APIView):

    def get(self,request,format=None):
        username = self.request.user.username
        results = []
        myworkorders = WorkOrder.objects.filter(Q(creator=self.request.user.username)).order_by('-id')
        for myworkorder in myworkorders:
            myworkorder_serializer = WorkOrderSerializer(myworkorder)
            results.append(myworkorder_serializer.data)
        re = { 'results': '',}
        re['results'] = results
        return Response(re)


