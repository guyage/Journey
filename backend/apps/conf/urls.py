# -*- coding:utf-8 -*-
from django.conf.urls import url, include
from rest_framework import routers
from apps.conf.views import *

router = routers.DefaultRouter()

router.register(r'mailconfig', MailConfigViewSet, basename="mailconfig")
router.register(r'querylimit', QueryLimitViewSet, basename="querylimit")
router.register(r'dumpwhitelist', DumpWhiteListViewSet, basename="dumpwhitelist")

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'mailtest', MailTestViewSet.as_view()),
]