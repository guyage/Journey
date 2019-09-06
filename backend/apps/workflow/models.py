from django.db import models
from user.models import Users

class WorkOrderType(models.Model):
    """
    工单类型表
    """
    ordertype = models.CharField(blank=True,  max_length=128, verbose_name="工单类型")
    formconfig = models.TextField(blank=True,verbose_name='form配置')
    remotefuncs = models.TextField(blank=True,verbose_name='工单相关远程方法')
    script = models.CharField(blank=True,  max_length=255, verbose_name="执行脚本")

    class Meta:
        verbose_name = u"工单类型表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.ordertype



class ApprovalGroup(models.Model):
    """
    工单审批组
    """
    approver_group_name = models.CharField(blank=True,  max_length=128, verbose_name="工单审批组")
    users = models.ManyToManyField(Users, blank=True,verbose_name='审批组内用户',related_name="approver_user")

    class Meta:
        verbose_name = u"工单审批组表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.approver_group_name

class WorkOrderStep(models.Model):
    """
    工单步骤表
    """
    ordertype = models.ForeignKey(WorkOrderType,blank=True,null=True,on_delete=models.CASCADE,related_name="ordertype_step")
    approver_group = models.ForeignKey(ApprovalGroup,blank=True,null=True,on_delete=models.SET_NULL,related_name="order_step_approvergroup")
    step_id = models.IntegerField(blank=True, verbose_name=u"步骤id")
    step_name = models.CharField(blank=True,  max_length=128, verbose_name="步骤名称")

    class Meta:
        verbose_name = u"工单步骤表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.ordertype

STATUS_CHOICE = (
    (-1, u'已失败'),
    (0, u'已终止'),
    (1, u'审批中'),
    (2, u'已同意'),
    (3, u'已完成'),
    (4, u'已驳回'),
)

class WorkOrder(models.Model):
    """
    工单表
    """
    title = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"工单主题")
    ordertype = models.ForeignKey(WorkOrderType,blank=True,null=True,on_delete=models.SET_NULL,related_name="workorder_type")
    status = models.IntegerField(choices=STATUS_CHOICE, default=1, verbose_name=u"工单状态")
    approver_group = models.ForeignKey(ApprovalGroup,blank=True,null=True,on_delete=models.SET_NULL,related_name="workorder_approvergroup")
    content = models.TextField(blank=True,null=False,verbose_name=u"工单参数")
    creator = models.CharField(max_length=50, blank=True,verbose_name=u"申请人")
    operator = models.CharField(max_length=50, blank=True,verbose_name=u"操作人")
    create_time = models.DateTimeField(blank=True, auto_now_add=True, verbose_name=u"创建时间")
    update_time = models.DateTimeField(blank=True, auto_now=True, verbose_name=u"更新时间")

    class Meta:
        verbose_name = u"工单表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title

class WorkOrderState(models.Model):

    wordorder_id = models.ForeignKey(WorkOrder, blank=True, null=True, on_delete=models.CASCADE,verbose_name=u'工单id', related_name="state_wordorder_id")
    step = models.IntegerField(blank=True, null=False,verbose_name=u"对应工单步骤ID")
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