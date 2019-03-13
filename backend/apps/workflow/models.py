from django.db import models

class WorkOrderType(models.Model):
    id = models.AutoField(primary_key=True)
    ordertype_id = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"类型ID")
    ordertype_name = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"类型名")
    ordersteps_id = models.IntegerField(blank=True, null=True,verbose_name=u"步骤ID")
    ordersteps_name = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"步骤名")
    ordersteps_button = models.CharField(max_length=256, blank=True, null=True, verbose_name=u"步骤按钮")
    ordersteps_permissions = models.CharField(max_length=256, blank=True, null=True, verbose_name=u"步骤权限组")
    create_time = models.DateTimeField(blank=True, auto_now_add=True, verbose_name=u"创建时间")
    update_time = models.DateTimeField(blank=True, auto_now=True, verbose_name=u"更新时间")
    comment = models.CharField(max_length=64, blank=True, null=True, verbose_name=u"备注")

    class Meta:
        verbose_name = u"工单类型表"
        verbose_name_plural = verbose_name
        db_table = 'workordertype'

    def __unicode__(self):
        return self.ordertypename

class WorkFlow(models.Model):
    id = models.AutoField(primary_key=True)
    ordertype_id = models.ForeignKey(WorkOrderType,null=True,on_delete=models.SET_NULL,verbose_name='工单类型ID',related_name='ordertype_id')
    ordertype_name = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"类型名")
    workflow_id = models.IntegerField(blank=True, null=True,verbose_name=u"工作流ID")
    creator = models.CharField(max_length=64, blank=True, null=True, verbose_name=u"工单创建人")
    operator = models.CharField(max_length=64, blank=True, null=True, verbose_name=u"工单操作人")
    theme = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"工单主题")
    content = models.TextField(verbose_name=u"工单内容")
    notices = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"通知方式")
    create_time = models.DateTimeField(blank=True, auto_now_add=True, verbose_name=u"创建时间")
    update_time = models.DateTimeField(blank=True, auto_now=True, verbose_name=u"更新时间")
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"描述")

    class Meta:
        verbose_name = u"工作流表"
        verbose_name_plural = verbose_name
        db_table = 'workflow'

    def __unicode__(self):
        return self.workflow_id