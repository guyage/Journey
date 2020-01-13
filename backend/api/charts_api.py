#!/usr/bin/env python
# -*- coding:utf-8 -*-
from api.db_api import db_api
from api.get_config import get_conf

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
        return col, results