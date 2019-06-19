from django.db import models
import django.utils.timezone as timezone
# Create your models here.
IS_ENABLED_CHOICE = (
    ('ENABLED','ENABLED'),
    ('DISABLED','DISABLED')
)

ROLE_CHOICE = (
    ('Master','Master'),
    ('Slave','Slave')
)

class MySQLInst(models.Model):
    inst_name = models.CharField(max_length=128, blank=False, null=False, verbose_name=u"MySQLInst名称")
    inst_host = models.GenericIPAddressField(blank=False, null=False, verbose_name=u"MySQLInstIP地址")
    inst_port = models.PositiveIntegerField(blank=False, null=False, verbose_name=u"MySQLInst端口")
    manage_user = models.CharField(max_length=32, blank=True, null=False, verbose_name=u"MySQLInst管理用户")
    manage_userpwd = models.CharField(max_length=64, blank=True, null=False, verbose_name=u"MySQLInst管理用户密码")
    read_user = models.CharField(max_length=32, blank=True, null=False, verbose_name=u"MySQLInst只读用户")
    read_userpwd = models.CharField(max_length=32, blank=True, null=False, verbose_name=u"MySQLInst只读用户密码")
    role = models.CharField(choices=ROLE_CHOICE,blank=True,max_length=12, default='Master',verbose_name=u"是否启用")
    services = models.CharField(max_length=255, blank=True, null=False, verbose_name=u"涉及服务")
    version = models.CharField(max_length=32,blank=True,default='5.7.21',verbose_name=u"MYSQL版本")
    is_enabled = models.CharField(choices=IS_ENABLED_CHOICE,max_length=12, default='ENABLED',verbose_name=u"是否启用")
    create_time = models.DateTimeField( auto_now_add=True, verbose_name=u"创建时间")
    update_time = models.DateTimeField(blank=True, auto_now=True, verbose_name=u"更新时间")
    comment = models.CharField(max_length=64, blank=True, null=False, verbose_name=u"备注")
    
    class Meta:
        verbose_name = u"MYSQL实例"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return (self.inst_host + ':' + self.inst_port)

class UserAccessMySQL(models.Model):
    username = models.CharField(max_length=50, blank=False,verbose_name=u"用户名")
    mysqlinst = models.ForeignKey(MySQLInst, blank=True, null=True, on_delete=models.SET_NULL,verbose_name=u'MYSQL实例id', related_name="user_access_mysqlinst")
    user_access_db = models.CharField(max_length=64, blank=False,verbose_name=u"用户访问数据库")
    # life_time = models.IntegerField(blank=False,verbose_name=u"MYSQL用户访问权限时间")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u"创建时间")
    update_time = models.DateTimeField(blank=True, auto_now=True, verbose_name=u"更新时间")
    # expired_time = models.DateTimeField(blank=True, verbose_name=u"MYSQL用户访问权限到期时间")
    STATUS_CHOICE = (
        (0, u'已禁止'),
        (1, u'申请中'),
        (2, u'使用中'),
        (3, u'已驳回')
    )

    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICE, default=1, verbose_name=u"用户申请查询权限状态")
    comment = models.CharField(max_length=64, blank=True, null=True, verbose_name=u"备注")

    class Meta:
        verbose_name = u"MYSQL用户权限时间表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username