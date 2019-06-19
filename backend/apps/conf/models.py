from django.db import models

# Create your models here.
class MailConfig(models.Model):
    mail_host = models.CharField(blank=True, null=False, max_length=64, verbose_name="邮箱服务器")
    mail_port = models.IntegerField(blank=True, null=False,default=25, verbose_name="邮箱服务器端口")
    mail_user = models.CharField(blank=True, null=False, max_length=32, verbose_name="邮箱用户")
    mail_pass = models.CharField(blank=True, null=False, max_length=32, verbose_name="邮箱用户密码")
    create_time = models.DateTimeField( auto_now_add=True, verbose_name=u"创建时间")
    update_time = models.DateTimeField(blank=True, auto_now=True, verbose_name=u"更新时间")
    comment = models.CharField(max_length=64, blank=True, null=False, verbose_name=u"备注")

    class Meta:
        verbose_name = u"邮件配置"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.mail_user