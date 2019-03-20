"""Journey URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from apps.db.views import *
from apps.user.views import *
from apps.sql.views import *
from rest_framework_jwt.views import obtain_jwt_token

router = routers.DefaultRouter()
router.register(r'mysqlinst', MySQLInstViewSet, base_name="mysqlinst")
router.register(r'mysqldb', MySQLDatabaseViewSet, base_name="mysqldb")
router.register(r'db', MySQLDatabaseViewSet, base_name="db")
router.register(r'user', UsersViewSet, base_name="user")
router.register(r'mongodbinst', MongodbInstViewSet, base_name="mongodbinst")
router.register(r'mongodbdb', MongodbDBViewSet, base_name="mongodbdb")
router.register(r'redisdb', RedisDBViewSet, base_name="redisdb")
# router.register(r'useraccessdb', UserAccessDbViewSet, base_name="useraccessdb")
# router.register(r'user', UsersViewSet, base_name="user")

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'api/', include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    url(r'api/login',obtain_jwt_token),
    url(r'^api/userinfo/(?P<username>\w+)/$', UserInfoViewSet.as_view()),
    url(r'^api/query', SQLQueryViewSet.as_view()),
    url(r'^api/sqlsoar', SQLSoarViewSet.as_view()),
    url(r'^api/mongodbquery', MongodbQueryViewSet.as_view()),
    url(r'^api/redisdbquery', RedisdbQueryViewSet.as_view()),
    url(r'^api/dbmeta', MysqlMetaViewSet.as_view()),
    url(r'^api/mysqluser', MysqlUserViewSet.as_view()),
    url(r'^api/ldapauth', LdapAuthViewSet.as_view()),
    url(r'^api/logout', LogoutViewSet.as_view(({'get':'logout'}))),
]
