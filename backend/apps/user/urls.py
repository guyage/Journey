# -*- coding:utf-8 -*-
from django.conf.urls import url, include
from rest_framework import routers
from apps.user.views import *

router = routers.DefaultRouter()

router.register(r'user', UsersViewSet, base_name="user")
router.register(r'usergroup', UserGroupViewSet, base_name="usergroup")
router.register(r'role', RoleViewSet, base_name="role")
router.register(r'menu', MenuViewSet, base_name="menu")

urlpatterns = [
    url(r'^', include(router.urls)),
]