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
from django.urls import path,re_path
from django.conf.urls import url, include
from apps.common.views import *
from Journey.settings import MEDIA_ROOT
from django.conf import settings
from django.views.static import serve
from rest_framework.documentation import include_docs_urls


# swagger pakeage
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from rest_framework_jwt.views import obtain_jwt_token
schema_view = get_schema_view(title='Journey API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

urlpatterns = [
    url(r'^api/docs/', include_docs_urls('Journey API')), 
    url('^api/swagger-docs/', schema_view), # swagger doc
    url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'api/login',obtain_jwt_token),
    url(r'api/ldapauth', LdapAuthViewSet.as_view()),
    url(r'api/logout',LogoutViewSet.as_view(({'get':'logout'}))),
    # conf
    path(r'api/', include('conf.urls')),
    # db
    path(r'api/', include('db.urls')),
    # query
    path(r'api/', include('query.urls')),
    # user
    path(r'api/', include('user.urls')),
    # workflow
    # path(r'api/', include('workflow.urls')),
    # sqlorder
    # path(r'api/', include('sqlorder.urls')),
    # workorder
    path(r'api/', include('workorder.urls')),
    # charts
    path(r'api/', include('charts.urls')),
    # 上传附件
    path('uploads/<path:path>',serve,{'document_root':settings.MEDIA_ROOT}),
    # easyaudit
    path(r'api/', include('easyaudit.urls')),
]
