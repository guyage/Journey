# -*- coding: UTF-8 -*-
from django.db.models import Q
from utils.baseviews import BaseApiViewSet
from rest_framework.response import Response
from workorder.models.sqlorder import *
from workorder.models.autoorder import *
from workorder.serializers.workorder import *
import time,datetime
import pytz

import logging
# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger('default')

class AllWorkOrderViewSet(BaseApiViewSet):

    # 权限相关标识
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
        # //获取sql工单列表
        for sqlorder in searchsqlorders:
            sqlorder_serializer = AllWorkOrderSerializer(sqlorder)
            results.append(sqlorder_serializer.data)
        # 获取自助工单列表
        for autoorder in searchautoorders:
            autoorder_serializer = AllWorkOrderSerializer(autoorder)
            results.append(autoorder_serializer.data)
        re = { 'results': '',}
        re['results'] = results
        return Response(re)