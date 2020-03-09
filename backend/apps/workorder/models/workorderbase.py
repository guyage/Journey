# -*- coding: UTF-8 -*-
from django.db import models

STATUS_CHOICE = (
    (-1, u'已失败'),
    (0, u'待审批'),
    (1, u'已驳回'),
    (2, u'已完成'),
    (3, u'DBA-CHECK'),
    (4, u'待执行'),
    (5, u'已执行，待验证'),
    (6, u'已验证'),
    (7, u'已取消'),
    (8,u'未接受'),
    (9,u'正在处理'),
)

class WorkOrderBase(models.Model):
    """
    工单基础信息表
    """
    title = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"工单主题")
    classify = models.CharField(max_length=50, blank=True,verbose_name=u"分类")
    status = models.IntegerField(choices=STATUS_CHOICE, default=0, verbose_name=u"工单状态")
    creator = models.CharField(max_length=50, blank=True,verbose_name=u"申请人")
    operator = models.CharField(max_length=50, blank=True,verbose_name=u"操作人")
    create_time = models.DateTimeField(blank=True, auto_now_add=True, verbose_name=u"创建时间")
    update_time = models.DateTimeField(blank=True, auto_now=True, verbose_name=u"更新时间")

    class Meta:
        verbose_name = u"工单基础信息表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title