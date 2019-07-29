from django.db import models

STATUS_CHOICE = (
    (-1, u'已失败'),
    (0, u'已终止'),
    (1, u'申请中'),
    (2, u'已同意'),
    (3, u'已完成'),
    (4, u'已驳回'),
)

class WorkOrder(models.Model):
    order_prefix = models.CharField(max_length=128, blank=True, null=True,default='OpsOnline',verbose_name=u"工单号前缀")
    order_type = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"工单类型")
    title = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"主题")
    status = models.IntegerField(choices=STATUS_CHOICE, default=1, verbose_name=u"工单状态")
    content = models.TextField(blank=True,null=False,verbose_name=u"工单参数")
    describe = models.TextField(blank=True,null=False,verbose_name=u"描述")
    creator = models.CharField(max_length=50, blank=True,verbose_name=u"申请人")
    operation_group = models.CharField(max_length=50, blank=True,verbose_name=u"操作组")
    operator = models.CharField(max_length=50, blank=True,verbose_name=u"操作人")
    create_time = models.DateTimeField(blank=True, auto_now_add=True, verbose_name=u"创建时间")
    update_time = models.DateTimeField(blank=True, auto_now=True, verbose_name=u"更新时间")
    comment = models.CharField(max_length=64, blank=True, null=True, verbose_name=u"备注")
    
    class Meta:
        verbose_name = u"工单表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title

class WorkOrderState(models.Model):

    wordorder_id = models.ForeignKey(WorkOrder, blank=True, null=True, on_delete=models.SET_NULL,verbose_name=u'Git工单id', related_name="state_gitwordorder_id")
    step = models.IntegerField(blank=True, null=False,verbose_name=u"步骤")
    action = models.CharField(max_length=50, blank=True,verbose_name=u"操作动作")
    operator = models.CharField(max_length=50, blank=True,verbose_name=u"操作人")
    create_time = models.DateTimeField(blank=True, auto_now_add=True, verbose_name=u"创建时间")
    update_time = models.DateTimeField(blank=True, auto_now=True, verbose_name=u"更新时间")
    comment = models.CharField(max_length=64, blank=True, null=True, verbose_name=u"备注")
    
    
    class Meta:
        verbose_name = u"工单流转表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.operator