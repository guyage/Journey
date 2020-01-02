# -*- coding:utf-8 -*-
from django.conf.urls import url, include
from rest_framework import routers
from apps.db.views import *

router = routers.DefaultRouter()

router.register(r'mysqlinst', MySQLInstViewSet, base_name="mysqlinst")
router.register(r'mongodbinst', MongoDBInstViewSet, base_name="mongodbinst")
router.register(r'redisinst', RedisInstViewSet, base_name="redisinst")
router.register(r'useraccessmysql', UserAccessMySQLViewSet, base_name="useraccessmysql")
router.register(r'useraccessmongodb', UserAccessMongoDBViewSet, base_name="useraccessmongodb")
router.register(r'useraccessredis', UserAccessRedisViewSet, base_name="useraccessredis")

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'mysqlmeta', MySQLMetaViewSet.as_view()),
    url(r'mysqluser', MySQLUserViewSet.as_view()),
    url(r'mysqlstatus', MySQLStatusViewSet.as_view()),
    url(r'useraccessdb', UserAccessDbViewSet.as_view()),
]