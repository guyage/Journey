# -*- coding: UTF-8 -*-
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from workorder.models.sqlorder import *
from workorder.models.autoorder import *
from workorder.serializers.workorder import *
from user.permissions import CustomerPremission
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
import time,datetime
import pytz

import logging
# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger('default')

class AllWorkOrderViewSet(APIView):

    # 权限相关标识
    permission_classes = [CustomerPremission,IsAuthenticated]
    module_perms = ['workorder:allworkorder']

    def get(self,request,format=None):
        userinfo = self.request.user
        username = userinfo.username
        results = []
        # 获取最近7天内的工单
        laste_time = (datetime.date.today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d %X')
        laste_sqlorders = SqlOrder.objects.filter(Q(create_time__gt=laste_time))
        laste_autoorders = AutoOrder.objects.filter(Q(create_time__gt=laste_time))
        # //获取sql工单列表
        for sqlorder in laste_sqlorders:
            sqlorder_serializer = AllWorkOrderSerializer(sqlorder)
            results.append(sqlorder_serializer.data)

        # 获取自助工单列表
        for autoorder in laste_autoorders:
            autoorder_serializer = AllWorkOrderSerializer(autoorder)
            results.append(autoorder_serializer.data)
        sort_results = sorted(results, key=lambda k: k['create_time'],reverse=True)
        re = { 'results': '',}
        re['results'] = sort_results
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
                searchautoorders = AutoOrder.objects.filter(Q(creator=self.request.user.username),Q(create_time__range=(date_from,date_to))).order_by('-id')
            else:
                searchsqlorders = SqlOrder.objects.filter(Q(creator=self.request.user.username),Q(create_time__gt=laste_time)).order_by('-id')
                searchautoorders = AutoOrder.objects.filter(Q(creator=self.request.user.username),Q(create_time__gt=laste_time)).order_by('-id')
        elif (searchtype == 'time'):
            if (timerange):
                date_from = timerange[0]
                date_to = timerange[1]
                searchsqlorders = SqlOrder.objects.filter(Q(create_time__range=(date_from,date_to))).order_by('-id')
                searchautoorders = AutoOrder.objects.filter(Q(create_time__range=(date_from,date_to))).order_by('-id')
        # 获取待办的工单
        elif (searchtype == 'todo'):
            todo_order_status = [-1,1,2]
            user_approvalgroup_list = []
            for i in userinfo.approver_user.all():
                user_approvalgroup_list.append(i.id)
            if (timerange):
                date_from = timerange[0]
                date_to = timerange[1]
                searchsqlorders = SqlOrder.objects.filter(~Q(status__in=todo_order_status),Q(approver_group_id__in=user_approvalgroup_list),Q(create_time__range=(date_from,date_to))).order_by('-id')
                searchautoorders = AutoOrder.objects.filter(~Q(status__in=todo_order_status),Q(approver_group_id__in=user_approvalgroup_list),Q(create_time__range=(date_from,date_to))).order_by('-id')
            else:
                searchsqlorders = SqlOrder.objects.filter(~Q(status__in=todo_order_status),Q(approver_group_id__in=user_approvalgroup_list),Q(create_time__gt=laste_time)).order_by('-id')
                searchautoorders = AutoOrder.objects.filter(~Q(status__in=todo_order_status),Q(approver_group_id__in=user_approvalgroup_list),Q(create_time__gt=laste_time)).order_by('-id')
        elif (searchtype == 'search'):
            searchcontent = request.data['searchcontent']
            if (timerange):
                date_from = timerange[0]
                date_to = timerange[1]
                searchsqlorders = SqlOrder.objects.filter(Q(title__contains=searchcontent)|Q(creator__contains=searchcontent),Q(create_time__range=(date_from,date_to))).order_by('-id')
                searchautoorders = AutoOrder.objects.filter(Q(title__contains=searchcontent)|Q(creator__contains=searchcontent),Q(create_time__range=(date_from,date_to))).order_by('-id')
            else:
                searchsqlorders = SqlOrder.objects.filter(Q(title__contains=searchcontent)|Q(creator__contains=searchcontent),Q(create_time__gt=laste_time)).order_by('-id')
                searchautoorders = AutoOrder.objects.filter(Q(title__contains=searchcontent)|Q(creator__contains=searchcontent),Q(create_time__gt=laste_time)).order_by('-id')
        
        # //获取sql工单列表
        for sqlorder in searchsqlorders:
            sqlorder_serializer = AllWorkOrderSerializer(sqlorder)
            results.append(sqlorder_serializer.data)
        # 获取自助工单列表
        for autoorder in searchautoorders:
            autoorder_serializer = AllWorkOrderSerializer(autoorder)
            results.append(autoorder_serializer.data)
        
        sort_results = sorted(results, key=lambda k: k['create_time'],reverse=True)
        re = { 'results': '',}
        re['results'] = sort_results
        return Response(re)