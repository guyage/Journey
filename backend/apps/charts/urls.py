# -*- coding:utf-8 -*-
from django.conf.urls import url, include
from apps.charts.views import *

urlpatterns = [
    url(r'showcharts', ShowChartsViewSet.as_view()),
]