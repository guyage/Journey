from django.db import models
from utils.basemodel import BaseModel
from db.models import MySQLInst

class QuerySqlLog(BaseModel):
    """
    sql查询日志表
    """
    operator = models.CharField(max_length=64, blank=True,null=True, verbose_name=u"查询人")
    mysqlinst = models.ForeignKey(MySQLInst,blank=True,null=True,on_delete=models.SET_NULL,verbose_name=u"查询实例",related_name="querysqllog_mysqlinst")
    dbname = models.CharField(max_length=64, blank=True,null=True, verbose_name=u"查询数据库")
    sql = models.TextField(blank=True,verbose_name=u"查询sql")

    class Meta:
        verbose_name = u"sql查询日志表"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.operator