# -*- coding: utf-8 -*-

from django.db import models

class BaseModel(models.Model):
    '''
       基础表(抽象类),所有model需要增加以下三个字段
    '''
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间', auto_now_add=True, null=True, blank=True)
    update_time = models.DateTimeField(verbose_name='更新时间', help_text='更新时间', auto_now=True, null=True, blank=True)
    comment = models.TextField(verbose_name='备注', help_text='备注', null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['-id']
