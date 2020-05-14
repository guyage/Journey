# -*- coding:utf-8 -*-
from django.conf.urls import url, include
from rest_framework import routers
from apps.db.views import *

router = routers.DefaultRouter()

router.register(r'mysqlinst', MySQLInstViewSet, basename="mysqlinst")
router.register(r'mongodbinst', MongoDBInstViewSet, basename="mongodbinst")
router.register(r'redisinst', RedisInstViewSet, basename="redisinst")
router.register(r'useraccessmysql', UserAccessMySQLViewSet, basename="useraccessmysql")
router.register(r'useraccessmongodb', UserAccessMongoDBViewSet, basename="useraccessmongodb")
router.register(r'useraccessredis', UserAccessRedisViewSet, basename="useraccessredis")

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'mysqlmeta', MySQLMetaViewSet.as_view()),
    url(r'mysqluser', MySQLUserViewSet.as_view()),
    url(r'mysqlstatus', MySQLStatusViewSet.as_view()),
    url(r'useraccessdb', UserAccessDbViewSet.as_view()),
]