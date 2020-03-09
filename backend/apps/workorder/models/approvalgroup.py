from django.db import models
from user.models import Users

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