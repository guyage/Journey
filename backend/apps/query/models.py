from django.db import models
from db.models import MySQLInst

class QuerySqlLog(models.Model):
    """
    sql查询日志表
    """
    operator = models.CharField(max_length=64, blank=True,null=True, verbose_name=u"查询人")
    mysqlinst = models.ForeignKey(MySQLInst,blank=True,null=True,on_delete=models.SET_NULL,verbose_name=u"查询实例",related_name="querysqllog_mysqlinst")
    dbname = models.CharField(max_length=64, blank=True,null=True, verbose_name=u"查询数据库")
    sql = models.TextField(blank=True,verbose_name=u"查询sql")
    create_time = models.DateTimeField( auto_now_add=True, verbose_name=u"创建时间")
    update_time = models.DateTimeField(blank=True, auto_now=True, verbose_name=u"更新时间")
    comment = models.CharField(max_length=64, blank=True, verbose_name=u"备注")

    class Meta:
        verbose_name = u"sql查询日志表"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.operator