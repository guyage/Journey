from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework import filters
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.response import Response
from django.db.models.query import QuerySet
from user.models import *
from workflow.models import *
from workflow.serializers import *
from api.git_api import GitLabAPI
from api.send_mail import send_mail
import json

# Create your views here.
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

    def create(self, request, *args, **kwargs):

        mailtolist = []
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        workorderid = serializer.data['id']
        operator = serializer.data['creator']
        operation_group = serializer.data['operation_group']
        content = serializer.data['content']
        WorkOrderState.objects.create(wordorder_id_id=workorderid,step=1,action='开始',operator=operator)
        userlist = PermissionsGroup.objects.get(Q(permissions_name=operation_group)).user_permissions_join.all()
        for user in userlist:
            mailtolist.append(Users.objects.filter(username=user)[0].email)
        maildata = json.loads(content)
        send_mail(mailtolist,4,maildata)
        return Response(request.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.filter(Q(creator=self.request.user.username)).order_by('-id')
        return queryset

class WorkOrderStateViewSet(viewsets.ModelViewSet):
    """
    工单
    """
    queryset = WorkOrderState.objects.all().order_by('id')
    serializer_class = WorkOrderStateSerializer
    # pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('operator',)
    ordering_fields = ('id',)

class GitLabInfoViewSet(APIView):

    def post(self,request,format=None):
        git_api = GitLabAPI()
        reqtype = request.data['reqtype']
        if (reqtype == 'projects'):
            projects = git_api.get_all_projects()
            results = projects
        re = { 'results': '',}      
        re['results'] = results
        
        return Response(re)

class ToDoWorkOrderViewSet(APIView):

    def post(self,request,format=None):
        username = request.data['username']
        userinfo = Users.objects.get(Q(username=username))
        permissionsgroup = []
        todoworkorderlist = []
        permissions_group = userinfo.permissions_group.all()
        for i in permissions_group:
            permissionsgroup.append(i.permissions_name)
        # Git工单
        workorder = WorkOrder.objects.filter(Q(status=1))
        for workorder in workorder:
            if (workorder.operation_group in permissionsgroup):
                workorder_serializer = WorkOrderSerializer(workorder)
                todoworkorderlist.append(workorder_serializer.data)
        
        results = todoworkorderlist
        results = sorted(results, key=lambda e: e.__getitem__('update_time'),reverse = True)
        re = { 'results': '',}
        re['results'] = results
        
        return Response(re)

class WorkOrderDetailViewSet(APIView):

    def post(self,request,format=None):
        # username = request.data['username']
        workorderid = request.data['workorderid']
        workorderdetail = WorkOrder.objects.get(Q(id=workorderid))
        workorderdetail_serializer = WorkOrderSerializer(workorderdetail)
        results = workorderdetail_serializer.data
        re = { 'results': '',}
        re['results'] = results
        return Response(re)

class WorkOrderStepViewSet(APIView):

    def post(self,request,format=None):
        # username = request.data['username']
        workordersteps = []
        workorderid = request.data['workorderid']
        steps = WorkOrderState.objects.filter(Q(wordorder_id_id=workorderid)).values("step").distinct().count()
        workorderstate = WorkOrderState.objects.filter(Q(wordorder_id_id=workorderid)).order_by('step')
        for step in workorderstate:
            step_serializer = WorkOrderStepSerializer(step)
            workordersteps.append(step_serializer.data)
        results = workordersteps
        re = { 'results': '', 'steps': ''}
        re['results'] = results
        re['steps'] = steps
        return Response(re)

class ChangeWorkOrderStateViewSet(APIView):

    def post(self,request,format=None):
        real_workorderidlist = []
        git_api = GitLabAPI()
        changetype = request.data['changetype']
        workorderidlist = request.data['workorderid']
        operator = request.data['operator']
        if isinstance(workorderidlist,int):
            real_workorderidlist = list(str(workorderidlist))
        elif isinstance(workorderidlist,list):
            real_workorderidlist = workorderidlist
        elif isinstance(workorderidlist,str):
            real_workorderidlist = list(workorderidlist)
        for workorderid in real_workorderidlist:
            if (changetype == 'agree'):
                workorderinfo = WorkOrder.objects.filter(Q(id=workorderid))[0]
                gitlab_set_info = json.loads(workorderinfo.content)
                gitlab_set_results = git_api.set_project_member(gitlab_set_info)
                if (gitlab_set_results == 'ok'):
                    workorderinfo.status = 2
                    workorderinfo.operation_group = 'admin'
                    workorderinfo.save()
                    WorkOrderState.objects.create(wordorder_id_id=workorderid,step=2,action='同意',operator=operator)
                    workorderinfo = WorkOrder.objects.filter(Q(id=workorderid))[0]
                    workorderinfo.status = 3
                    workorderinfo.save()
                    WorkOrderState.objects.create(wordorder_id_id=workorderid,step=3,action='完成',operator='系统')
                else:
                    workorderinfo = WorkOrder.objects.filter(Q(id=workorderid))[0]
                    workorderinfo.status = 2
                    workorderinfo.operation_group = 'admin'
                    workorderinfo.save()
                    workorderinfo.status = -1
                    workorderinfo.save()
                    WorkOrderState.objects.create(wordorder_id_id=workorderid,step=2,action='同意',operator=operator)
                    WorkOrderState.objects.create(wordorder_id_id=workorderid,step=-1,action='失败',operator='系统')  

                # WorkOrderState.objects.create(wordorder_id_id=workorderid,step=3,action='完成',operator='系统')
            elif (changetype == 'reject'):
                workorderinfo = WorkOrder.objects.filter(Q(id=workorderid))[0]
                workorderinfo.status = 4
                workorderinfo.operation_group = ''
                workorderinfo.save()
                WorkOrderState.objects.create(wordorder_id_id=workorderid,step=4,action='驳回',operator=operator)
        results = ''
        re = { 'results': '', }
        re['results'] = results
        return Response(re)
