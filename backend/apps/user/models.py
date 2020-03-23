from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class UserGroup(models.Model):
    """
    用户组表
    """
    group = models.CharField(max_length=64, unique=True)
    comment = models.CharField(max_length=128, blank=True,)

    class Meta:
        verbose_name = u"用户组"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.group

class Menu(models.Model):
    """
    菜单表
    """
    name = models.CharField(blank=False, max_length=128, verbose_name="菜单名称")
    parent_id = models.IntegerField(blank=True, verbose_name=u"父菜单ID，一级菜单为0")
    url = models.CharField(blank=True,  max_length=255, verbose_name="菜单对应url")
    # api = models.CharField(blank=True,  max_length=255, verbose_name="后端api接口地址")
    # perms = models.CharField(blank=True,  max_length=255, verbose_name="授权(多个用逗号分隔，如sys:user:post,sys:user:patch)")
    mtype = models.IntegerField(blank=True, verbose_name=u"菜单类型 0:目录 1:菜单 2:内部跳转url ")
    icon = models.CharField(blank=True,  max_length=255, verbose_name="菜单对应图标")
    creator = models.CharField(max_length=64, blank=True, verbose_name=u"创建人")
    modifier = models.CharField(max_length=64, blank=True, verbose_name=u"最后修改人")
    del_flag = models.IntegerField(blank=True, verbose_name=u"是否删除 -1:删除 0:正常")
    create_time = models.DateTimeField( auto_now_add=True, verbose_name=u"创建时间")
    update_time = models.DateTimeField(blank=True, auto_now=True, verbose_name=u"更新时间")
    comment = models.CharField(max_length=64, blank=True, verbose_name=u"备注")

    class Meta:
        verbose_name = u"菜单表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

class Perms(models.Model):
    """
    权限表
    """
    name = models.CharField(blank=True,  max_length=255, verbose_name="后端api名称")
    api = models.CharField(blank=True,  max_length=255, verbose_name="后端api接口地址")
    module_perms = models.CharField(blank=True,  max_length=255, verbose_name="后端接口标识")
    perms = models.CharField(blank=True, max_length=255, verbose_name="授权(多个用逗号分隔，如sys:user:post,sys:user:patch)")
    creator = models.CharField(max_length=64, blank=True, verbose_name=u"创建人")
    modifier = models.CharField(max_length=64, blank=True, verbose_name=u"最后修改人")
    del_flag = models.IntegerField(blank=True, verbose_name=u"是否删除 -1:删除 0:正常")
    create_time = models.DateTimeField( auto_now_add=True, verbose_name=u"创建时间")
    update_time = models.DateTimeField(blank=True, auto_now=True, verbose_name=u"更新时间")
    comment = models.CharField(max_length=64, blank=True, verbose_name=u"备注")

class Role(models.Model):
    """
    角色表
    """
    name = models.CharField(blank=True, max_length=64, verbose_name="角色名称")
    menu = models.ManyToManyField(Menu,blank=True,related_name="role_menu")
    perms = models.ManyToManyField(Perms,blank=True,related_name="role_perms")

    class Meta:
        verbose_name = u"角色表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

class Users(AbstractUser):
    """
    用户表(继承django默认用户表)
    """
    group = models.ForeignKey(UserGroup,blank=True,null=True,on_delete=models.SET_NULL,related_name="user_group")
    roles = models.ManyToManyField(Role, blank=True,verbose_name='拥有的所有角色',related_name="user_role")
    mobile = models.CharField(blank=True, max_length=11, verbose_name="电话")
    webcat = models.CharField(blank=True, max_length=128, verbose_name="微信")
    comment = models.CharField(max_length=64, blank=True,  verbose_name=u"备注")
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
