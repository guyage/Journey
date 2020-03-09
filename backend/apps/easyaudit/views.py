from django.shortcuts import render
from rest_framework.views import APIView
from utils.baseviews import BaseApiViewSet
from rest_framework.response import Response
from django.db.models import Q
from user.permissions import CustomerPremission
import time,datetime
from easyaudit.models import *
from easyaudit.serializers import *

class CRUDEventViewSet(BaseApiViewSet):
    """
    获取系统操作日志
    """
    # 权限相关
    module_perms = ['easyaudit:crudevent']

    def post(self,request,format=None):
        results = []
        timerange = request.data['timerange'] if 'timerange' in request.data else None
        username = request.data['username'] if 'username' in request.data else None
        # 默认显示最近7天内的日志
        if (timerange is None) and (username is None):
            laste_time = (datetime.date.today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d %X')
            laste_logs = CRUDEvent.objects.filter(Q(datetime__gt=laste_time),Q(user__isnull=False),~Q(changed_fields__icontains='jwt_secret')).order_by('-id')
            for log in laste_logs:
                log_serializer = CRUDEventSerializer(log)
                results.append(log_serializer.data)

        elif (timerange):
            date_from = timerange[0]
            date_to = timerange[1]
            search_logs = CRUDEvent.objects.filter(Q(datetime__range=(date_from,date_to)),Q(user__isnull=False),~Q(changed_fields__icontains='jwt_secret')).order_by('-id')
            for log in search_logs:
                log_serializer = CRUDEventSerializer(log)
                results.append(log_serializer.data)

        re = { 'results': '',}
        re['results'] = results
        return Response(re)
