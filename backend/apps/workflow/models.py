from django.db import models

class CommonInfo(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=64, blank=True, null=True, verbose_name=u"备注")
    create_time = models.DateTimeField(blank=True, auto_now_add=True, verbose_name=u"创建时间")
    update_time = models.DateTimeField(blank=True, auto_now=True, verbose_name=u"更新时间")

    class Meta:
        abstract = True
        app_label = 'db'


