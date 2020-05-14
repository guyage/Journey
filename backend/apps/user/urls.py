# -*- coding:utf-8 -*-
from django.conf.urls import url, include
from rest_framework import routers
from apps.user.views import *

router = routers.DefaultRouter()

router.register(r'user', UsersViewSet, basename="user")
router.register(r'usergroup', UserGroupViewSet, basename="usergroup")
router.register(r'role', RoleViewSet, basename="role")
router.register(r'menu', MenuViewSet, basename="menu")
router.register(r'perms', PermsViewSet, basename="perms")

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'userinfo', UserInfoViewSet.as_view()),
]