from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from user.permissions import CustomerPremission
from utils.charts_api import ShowCharts

class ShowChartsViewSet(APIView):
    
    # 权限相关
    permission_classes = [CustomerPremission,]
    module_perms = ['charts:showcharts']
    def post(self,request,format=None):
        
        flag = request.data['flag']
        showcharts = ShowCharts()
        col,results = showcharts.order_charts(flag)
        
        re = { 'col': '', 'results': '',}
        re['col'] = col
        re['results'] = results
        return Response(re)
