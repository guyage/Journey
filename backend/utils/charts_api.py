#!/usr/bin/env python
# -*- coding:utf-8 -*-
from utils.db_api import db_api
from utils.get_config import get_conf

class ShowCharts():

    def __init__(self):
        self.connectinfo = {'conn_host':'','conn_port':'','conn_user':'','conn_passwd':'','conn_db':''}
        self.connectinfo['conn_host'] = get_conf('db','host')
        self.connectinfo['conn_port'] = int(get_conf('db','port'))
        self.connectinfo['conn_user'] = get_conf('db','user')
        self.connectinfo['conn_passwd'] = get_conf('db','password')
        self.connectinfo['conn_db'] = get_conf('db','database')

    def order_charts(self,flag):
        dbapi = db_api()
        # 获取系统内工单总数
        if (flag == 0):
            sql = "select count(id) as sqlorder_total from sqlorder_sqlorder;"
            col, results = dbapi.mysql_query(self.connectinfo,sql)
        # 获取sql工单7天内数量
        elif (flag == 1):
            sql = "SELECT `date` as hisdate,IFNULL(total,0) as total \
                   FROM (SELECT @s:=@s + 1 AS `index`, DATE(DATE_SUB(CURRENT_DATE, INTERVAL @s DAY)) AS `date` \
                   FROM mysql.help_topic,(SELECT @s:= -1) temp \
                   WHERE @s < 6 \
                   ORDER BY `date`) hisdate \
                   LEFT JOIN \
                   (SELECT COUNT(*) AS total,LEFT(create_time,10) AS total_date \
                   FROM `workorder_workorderbase` \
                   WHERE LEFT(create_time,10) \
                   GROUP BY LEFT(create_time,10)) hissqlordersum \
                   ON hissqlordersum.total_date = hisdate.date order by `date`;"
            col, result = dbapi.mysql_query(self.connectinfo,sql)
            hisdate = []
            histotal = []
            for i in result:
                hisdate.append(i['hisdate'])
                histotal.append(i['total'])
            results = {'hisdate':hisdate,'histotal':histotal}
        return col, results