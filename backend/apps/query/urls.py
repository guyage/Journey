# -*- coding:utf-8 -*-
from django.conf.urls import url, include
from apps.query.views import *


urlpatterns = [
    # query
    url(r'querysql', QuerySqlViewSet.as_view()),
    url(r'querymongodb', QueryMongodbViewSet.as_view()),
    url(r'queryredis', QueryRedisViewSet.as_view()),
]