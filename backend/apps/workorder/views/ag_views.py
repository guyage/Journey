# coding=utf-8
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import viewsets
from workorder.serializers.ag_serializers import *
from workorder.models.approvalgroup import *
from user.permissions import CustomerPremission
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny

class ApprovalGroupViewSet(viewsets.ModelViewSet):
    """
    list:
        工单审批组列表.
    create:
        创建工单审批组.
    delete:
        删除工单审批组.
    update:
        修改工单审批组.
    """
    
    queryset = ApprovalGroup.objects.all().order_by('id')
    serializer_class = ApprovalGroupSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('approver_group_name',)
    ordering_fields = ('id',)
    # 权限相关
    permission_classes = [CustomerPremission,IsAuthenticated]
    module_perms = ['workorder:approvergroup']

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        userselected = request.data['userselected']
        instance.users.set(userselected)
        return Response(serializer.data)