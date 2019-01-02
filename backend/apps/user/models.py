# coding=utf-8
from django.db import models
from django.contrib.auth.models import AbstractUser
import django.utils.timezone as timezone
import uuid

USER_GROUPS_CHOICE = (
    ('admin', u'管理组'),
    ('dev', u'开发组')
)

# class CommonInfo(models.Model):
#     id = models.AutoField(primary_key=True)
#     comment = models.CharField(max_length=64, blank=True, null=True, verbose_name=u"备注")
#     create_time = models.DateTimeField(auto_now_add=True, verbose_name=u"创建时间")
#     update_time = models.DateTimeField(auto_now=True, verbose_name=u"更新时间")

#     class Meta:
#         abstract = True
#         app_label = 'user'
class Users(AbstractUser):
    mobile = models.CharField(blank=True, null=False, max_length=11, verbose_name="电话")
    webcat = models.CharField(blank=True, null=False, max_length=120, verbose_name="微信")
    group = models.CharField(max_length=20, choices=USER_GROUPS_CHOICE, default='dev', verbose_name=u"用户组")
    accessdb = models.CharField(max_length=500,blank=True, null=False,verbose_name="可访问数据库")
    comment = models.CharField(max_length=64, blank=True, null=False, verbose_name=u"备注")
    create_time = models.DateTimeField( auto_now_add=True, verbose_name=u"创建时间")
    update_time = models.DateTimeField(blank=True, auto_now=True, verbose_name=u"更新时间")
    jwt_secret = models.UUIDField(default=uuid.uuid4(), verbose_name=u"用户jwt加密秘钥")
    
    class Meta:
        verbose_name = u"用户(Users)"
        verbose_name_plural = verbose_name
        db_table = 'users'

    def __unicode__(self):
        return self.real_name

def jwt_get_secret_key(Users):
    return Users.jwt_secret

# class UserRoles(CommonInfo):
#     rolename = models.CharField(max_length=100,blank=False, null=False,verbose_name="角色名")
# class UserAccessDb(CommonInfo):
#     username = models.CharField(max_length=100,blank=False, null=False,verbose_name="用户名")
#     accessdblist = models.CharField(max_length=500,blank=False, null=False,verbose_name="用户名")

# class TodoList(models.Model):
#     username = models.CharField(max_length=100,blank=False, null=False,verbose_name="用户名")
#     todo = models.CharField(max_length=100,blank=False, null=False,verbose_name="待办事项")
#     #待办事项状态(1:active,2:completed,3:suspended)
#     status = models.IntegerField(blank=False, null=False,verbose_name="状态")
#     create_time = models.DateTimeField(blank=True, auto_now_add=True, verbose_name=u"创建时间")
#     update_time = models.DateTimeField(blank=True, auto_now=True, verbose_name=u"更新时间")


#     class Meta:
#         verbose_name = u"待办事项(TodoList)"
#         verbose_name_plural = verbose_name
#         db_table = 'user_todolist'

#     def __unicode__(self):
#         return self.username

