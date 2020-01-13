# -*- coding:utf-8 -*-
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path
from Journey.settings import MEDIA_ROOT
from django.conf import settings
from django.views.static import serve
from apps.sqlorder.views import *

router = routers.DefaultRouter()

# sqlorder
router.register(r'sqlordertype', SqlOrderTypeViewSet, base_name="sqlordertype")
router.register(r'sqlorder', SqlOrderViewSet, base_name="sqlorder")
router.register(r'sqltext', SqlTextViewSet, base_name="sqltext")
router.register(r'sqlfile', SqlFileViewSet, base_name="sqlfile")

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'mysqlorder', MySqlOrderViewSet.as_view()),
    url(r'inception', InceptionViewSet.as_view()),
    url(r'sqlorderdetail', SqlOrderDetailViewSet.as_view()),
    url(r'todosqlorder', ToDoSqlOrderViewSet.as_view()),
    url(r'allsqlorder', AllSqlOrderViewSet.as_view()),
    # 上传附件
    # path('uploads/<path:path>',serve,{'document_root':settings.MEDIA_ROOT}),
]