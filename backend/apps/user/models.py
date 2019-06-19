from django.db import models
from django.contrib.auth.models import AbstractUser
import django.utils.timezone as timezone
import uuid
# Create your models here.
class UserGroup(models.Model):
    group_name = models.CharField(max_length=80, unique=True)
    comment = models.CharField(max_length=160, blank=True, null=False)

    class Meta:
        verbose_name = u"用户组"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.group_name

class PermissionsGroup(models.Model):
    permissions_name = models.CharField(max_length=80, unique=True)
    comment = models.CharField(max_length=160, blank=True, null=False)

    class Meta:
        verbose_name = u"权限组"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.permissions_name

class Users(AbstractUser):
    group = models.ManyToManyField(UserGroup,blank=True,related_name="user_group_join")
    permissions_group = models.ManyToManyField(PermissionsGroup,blank=True,related_name="user_permissions_join")
    mobile = models.CharField(blank=True, null=False, max_length=11, verbose_name="电话")
    webcat = models.CharField(blank=True, null=False, max_length=120, verbose_name="微信")
    comment = models.CharField(max_length=64, blank=True, null=False, verbose_name=u"备注")
    create_time = models.DateTimeField( auto_now_add=True, verbose_name=u"创建时间")
    update_time = models.DateTimeField(blank=True, auto_now=True, verbose_name=u"更新时间")
    jwt_secret = models.UUIDField(default=uuid.uuid4(), verbose_name=u"用户jwt加密秘钥")
    
    class Meta:
        verbose_name = u"用户(Users)"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username

def jwt_get_secret_key(Users):
    return Users.jwt_secret