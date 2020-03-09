from rest_framework import viewsets
from rest_framework.views import APIView
from user.permissions import CustomerPremission

class BaseModelViewSet(viewsets.ModelViewSet):
    # 权限相关
    permission_classes = [CustomerPremission,]

class BaseApiViewSet(APIView):
    # 权限相关
    permission_classes = [CustomerPremission,]