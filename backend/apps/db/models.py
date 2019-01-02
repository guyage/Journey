# coding=utf-8
from django.db import models

class CommonInfo(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=64, blank=True, null=True, verbose_name=u"备注")
    create_time = models.DateTimeField(blank=True, auto_now_add=True, verbose_name=u"创建时间")
    update_time = models.DateTimeField(blank=True, auto_now=True, verbose_name=u"更新时间")

    class Meta:
        abstract = True
        app_label = 'db'


IS_ENABLED_CHOICE = (
    (0, u'禁用'),
    (1, u'启用')
)

# MySQL Database
class MySQLDatabase(CommonInfo):
    dbname = models.CharField(max_length=128, blank=False, null=False, verbose_name=u"MYSQL数据库名")
    host = models.GenericIPAddressField(blank=True, null=True, verbose_name=u"MYSQL IP地址")
    port = models.PositiveIntegerField(blank=True, null=True, default=3306, verbose_name=u"MYSQL端口")
    adminuser = models.CharField(max_length=32, blank=False, null=False, verbose_name=u"MYSQL用户名")
    password = models.CharField(max_length=64, blank=False, null=False, verbose_name=u"MYSQL密码")
    version = models.CharField(max_length=32,default=5.7,verbose_name=u"MYSQL版本")
    is_enabled = models.PositiveSmallIntegerField(choices=IS_ENABLED_CHOICE, verbose_name=u"是否启用")
    

    class Meta:
        verbose_name = u"MYSQL数据库"
        verbose_name_plural = verbose_name
        db_table = 'mysql_databases'

    def __unicode__(self):
        return self.dbname

