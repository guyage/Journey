# # -*- coding:utf-8 -*-
# from django.conf.urls import url, include
# from rest_framework import routers
# from apps.workflow.views import *

# router = routers.DefaultRouter()

# # workflow
# router.register(r'workordertype', WorkOrderTypeViewSet, base_name="workordertype")
# router.register(r'approvalgroup', ApprovalGroupViewSet, base_name="approvalgroup")
# router.register(r'workorderstep', WorkOrderStepViewSet, base_name="workorderstep")
# router.register(r'workorder', WorkOrderViewSet, base_name="workorder")

# urlpatterns = [
#     url(r'^', include(router.urls)),
#     url(r'gitlabinfo', GitLabInfoViewSet.as_view()),
#     url(r'workorderdetail', WorkOrderDetailViewSet.as_view()),
#     # url(r'myworkorder', MyWorkOrderViewSet.as_view()),
#     url(r'todoworkorder', ToDoWorkOrderViewSet.as_view()),
# ]