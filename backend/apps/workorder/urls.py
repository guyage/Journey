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
router.register(r'sqlordertype', SqlOrderTypeViewSet, base_name="sqlordertype")
router.register(r'sqlorder', SqlOrderViewSet, base_name="sqlorder")
router.register(r'sqltext', SqlTextViewSet, base_name="sqltext")
router.register(r'sqlfile', SqlFileViewSet, base_name="sqlfile")
# workorder-approvalgroup
router.register(r'approvalgroup', ApprovalGroupViewSet, base_name="approvalgroup")

# workorder-autoorder
router.register(r'autoordertype', AutoOrderTypeViewSet, base_name="autoordertype")
router.register(r'autoorderstep', AutoOrderStepViewSet, base_name="autoorderstep")
router.register(r'autoorder', AutoOrderViewSet, base_name="autoorder")






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