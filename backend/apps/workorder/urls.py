# -*- coding:utf-8 -*-
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path
from Journey.settings import MEDIA_ROOT
from django.conf import settings
from django.views.static import serve
from apps.workorder.views.sqlorder import *
from apps.workorder.views.autoorder import *
from apps.workorder.views.workorder import *
from apps.workorder.views.ag_views import *

router = routers.DefaultRouter()

# workorder-sqlorder
router.register(r'sqlordertype', SqlOrderTypeViewSet, basename="sqlordertype")
router.register(r'sqlorder', SqlOrderViewSet, basename="sqlorder")
router.register(r'sqltext', SqlTextViewSet, basename="sqltext")
router.register(r'sqlfile', SqlFileViewSet, basename="sqlfile")
# workorder-approvalgroup
router.register(r'approvalgroup', ApprovalGroupViewSet, basename="approvalgroup")

# workorder-autoorder
router.register(r'autoordertype', AutoOrderTypeViewSet, basename="autoordertype")
router.register(r'autoorderstep', AutoOrderStepViewSet, basename="autoorderstep")
router.register(r'autoorder', AutoOrderViewSet, basename="autoorder")






urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'mysqlorder', MySqlOrderViewSet.as_view()),
    url(r'inception', InceptionViewSet.as_view()),
    url(r'gitlabinfo', GitLabInfoViewSet.as_view()),
    url(r'sqlorderdetail', SqlOrderDetailViewSet.as_view()),
    # url(r'todosqlorder', ToDoSqlOrderViewSet.as_view()),
    # url(r'allsqlorder', AllSqlOrderViewSet.as_view()),
    # workorder
    url(r'allworkorder', AllWorkOrderViewSet.as_view()),

]