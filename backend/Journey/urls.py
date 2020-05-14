"""Journey URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,re_path
from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token
from Journey.settings import MEDIA_ROOT
from django.conf import settings
from django.views.static import serve

from apps.common.views import *


urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'api/login',obtain_jwt_token),
    url(r'api/ldapauth', LdapAuthViewSet.as_view()),
    url(r'api/logout',LogoutViewSet.as_view(({'get':'logout'}))),
    # user
    path(r'api/', include('user.urls')),
    # db
    path(r'api/', include('db.urls')),
    # query
    path(r'api/', include('query.urls')),
    # charts
    path(r'api/', include('charts.urls')),
    # easyaudit
    path(r'api/', include('easyaudit.urls')),
    # workorder
    path(r'api/', include('workorder.urls')),
    # 上传附件
    path('uploads/<path:path>',serve,{'document_root':settings.MEDIA_ROOT}),
]
