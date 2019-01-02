#!/usr/bin/env python
# -*- coding:utf-8 -*-

import db_api

db_api = db_api.db_api()

sql = 'select * from student;'

connectinfo = {'conn_host':'','conn_port':'','conn_user':'','conn_passwd':'','conn_db':''}
connectinfo['conn_host'] = '1.1.1.1'
connectinfo['conn_port'] = 3306
connectinfo['conn_user'] = 'root'
connectinfo['conn_passwd'] = 'aaa111'
connectinfo['conn_db'] = 'test'

print (connectinfo)

col,results = db_api.mysql_query(connectinfo,sql)

print(col)
print(results)