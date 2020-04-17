# -*- coding:utf-8 -*-
from django.conf.urls import url, include
from apps.query.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'querysqllog', QuerySqlLogViewSet, base_name="querysqllog")

urlpatterns = [
    # 
    url(r'^', include(router.urls)),
    url(r'querysql', QuerySqlViewSet.as_view()),
    url(r'querymongodb', QueryMongodbViewSet.as_view()),
    url(r'queryredis', QueryRedisViewSet.as_view()),
]