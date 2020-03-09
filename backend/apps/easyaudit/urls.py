# -*- coding:utf-8 -*-
from django.conf.urls import url, include
from apps.easyaudit.views import *


urlpatterns = [
    url(r'crudevent', CRUDEventViewSet.as_view()),
]
