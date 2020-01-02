from django.db import models
from workflow.models import ApprovalGroup
from db.models import MySQLInst
from sqlorder.storage import FileStorage
import os


IS_AUTO_CHOICE = (
    ('ENABLED','ENABLED'),
    ('DISABLED','DISABLED')
)

IS_ENABLED_CHOICE = (
    ('ENABLED','ENABLED'),
    ('DISABLED','DISABLED')
)

class SqlOrderType(models.Model):
    """
    SQL工单类型表
    """
    ordertype = models.CharField(blank=True,  max_length=128, verbose_name="工单类型")
    first_approver = models.ForeignKey(ApprovalGroup,blank=True,null=True,on_delete=models.SET_NULL,related_name="sqlorder_firstapprover")
    second_approver = models.ForeignKey(ApprovalGroup,blank=True,null=True,on_delete=models.SET_NULL,related_name="sqlorder_secondapprover")
    dba_approver = models.ForeignKey(ApprovalGroup,blank=True,null=True,on_delete=models.SET_NULL,related_name="sqlorder_dbaapprover")
    is_auto = models.CharField(choices=IS_AUTO_CHOICE,max_length=12, default='DISABLED',verbose_name=u"是否启用自动执行")
    is_file = models.CharField(choices=IS_ENABLED_CHOICE,max_length=12, default='DISABLED',verbose_name=u"是否启用附件")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"备注")

    class Meta:
        verbose_name = u"SQL工单类型表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.ordertype


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
)

class SqlOrder(models.Model):
    """
    SQL工单表
    """
    title = models.CharField(blank=True, max_length=255, verbose_name="工单名称")
    ordertype = models.ForeignKey(SqlOrderType,blank=True,null=True,on_delete=models.SET_NULL,related_name="sqlorder_type")
    status = models.IntegerField(choices=STATUS_CHOICE, default=0, verbose_name=u"工单状态")
    approver_group = models.ForeignKey(ApprovalGroup,blank=True,null=True,on_delete=models.SET_NULL,related_name="sqlorder_approvergroup")
    creator = models.CharField(max_length=50, blank=True,verbose_name=u"申请人")
    operator = models.CharField(max_length=50, blank=True,verbose_name=u"操作人")
    create_time = models.DateTimeField(blank=True, auto_now_add=True, verbose_name=u"创建时间")
    update_time = models.DateTimeField(blank=True, auto_now=True, verbose_name=u"更新时间")

    class Meta:
        verbose_name = u"SQL工单表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title

SQLSTATUS_CHOICE = (
    (-1, u'已失败'),
    (0, u'待执行'),
    (1, u'已执行'),
)

class SqlText(models.Model):
    """
    SQL文本表
    """
    sqlorder_id = models.ForeignKey(SqlOrder,blank=False,on_delete=models.CASCADE,related_name="sqlorder_sqltext")
    instid = models.ForeignKey(MySQLInst,blank=True,null=True,on_delete=models.SET_NULL,related_name="sqltext_mysqlinst")
    dbname = models.CharField(max_length=128, blank=True,verbose_name=u"数据库")
    sqltext = models.TextField(blank=True,null=False,verbose_name=u"sql文本")
    sqlstatus = models.IntegerField(choices=SQLSTATUS_CHOICE, default=0, verbose_name=u"SQL状态(inception执行状态)")
    exectime = models.DateTimeField(blank=True, auto_now=True, verbose_name=u"执行时间")
    info = models.TextField(blank=True,null=False,verbose_name=u"inception结果")

    class Meta:
        verbose_name = u"SQL文本表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.sqlorder_id

class SqlFile(models.Model):
    """
    SQL文件表
    """
    sqlorder_id = models.ForeignKey(SqlOrder,blank=False,on_delete=models.CASCADE,related_name="sqlorder_sqlfile")
    creator = models.CharField(max_length=50, blank=True,verbose_name=u"申请人")
    sqlfile = models.FileField(upload_to="sqlfile/%Y%m%d/",storage=FileStorage(),blank=False,verbose_name=u"sql文件")
    sqlfilename = models.CharField(max_length=255, blank=True,verbose_name=u"sql文件名字")
    sqlfileurl = models.CharField(max_length=255, blank=True,verbose_name=u"sql文件url")
    create_time = models.DateTimeField(blank=True, auto_now_add=True, verbose_name=u"创建时间")
    # info = models.TextField(blank=True,null=False,verbose_name=u"inception结果")

    # def save(self, *args, **kwargs):
    #     filename = os.path.splitext(self.sqlfile.name)
    #     self.sqlfilename = '{}{}'.format(filename[0],filename[1])     
    #     super(SqlFile, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = u"SQL文件表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.sqlorder_id


class SqlOrderState(models.Model):
    """
    SQL工单状态流转表
    """
    sqlorder_id = models.ForeignKey(SqlOrder,blank=False,on_delete=models.CASCADE,related_name="sqlorder_state")
    action = models.CharField(max_length=50, blank=True,verbose_name=u"操作动作")
    status = models.CharField(max_length=10, blank=True,verbose_name=u"操作状态success&error")
    operator = models.CharField(max_length=50, blank=True,verbose_name=u"操作人")
    comment = models.CharField(max_length=64, blank=True, null=True, verbose_name=u"备注")
    create_time = models.DateTimeField(blank=True, auto_now_add=True, verbose_name=u"创建时间")
    update_time = models.DateTimeField(blank=True, auto_now=True, verbose_name=u"更新时间")

    class Meta:
        verbose_name = u"SQL工单状态流转表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.order_id