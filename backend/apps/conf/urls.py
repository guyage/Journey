# -*- coding:utf-8 -*-
from django.conf.urls import url, include
from rest_framework import routers
from apps.conf.views import *

router = routers.DefaultRouter()

router.register(r'mailconfig', MailConfigViewSet, base_name="mailconfig")
router.register(r'querylimit', QueryLimitViewSet, base_name="querylimit")
router.register(r'dumpwhitelist', DumpWhiteListViewSet, base_name="dumpwhitelist")

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'mailtest', MailTestViewSet.as_view()),
]