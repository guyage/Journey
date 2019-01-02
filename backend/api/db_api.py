#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pymysql
import json,datetime,time
import subprocess
from . import config

class db_api():

    def __init__(self):
        pass

    def mysql_query(self,connectinfo,sql):
        conn_host = connectinfo['conn_host']
        conn_port = connectinfo['conn_port']
        conn_user = connectinfo['conn_user']
        conn_passwd = connectinfo['conn_passwd']
        conn_db = connectinfo['conn_db']
        try:
            conn = pymysql.connect(host=conn_host,port=conn_port,user=conn_user,passwd=conn_passwd,db=conn_db,charset='utf8')
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            count = cursor.execute(sql)
            index = cursor.description
            col=[]
            try:
                for i in index:
                    col.append(i[0])
            except Exception as e:
                conn.commit()
                cursor.close()
                conn.close()
                return (['ok'],''), ['set']
            results = cursor.fetchall()
            for i in range(len(results)):
                for k,v in results[i].items():
                    if (isinstance(v,bytes)):
                        if ( 'x01' in (str(v))):
                            results[i][k] = 1
                        elif ('x00' in (str(v))):
                            results[i][k] = 0 
                    elif (isinstance(v,type(None))):
                        results[i][k] = 'NULL'
                    elif (isinstance(v,datetime.datetime)):
                        results[i][k] = v.strftime("%Y-%m-%d %H:%M:%S")
            conn.commit()
            cursor.close()
            conn.close()
            return (col,results)
        except Exception as e:
            return(str(e),''),['error']

    def get_metadata(self,flag,connectinfo,dbname,tablename=None):
        # 获取对应数据库下的所有表名
        if (flag == 1):
            # dbname = meta_info['dbname']
            sql = "SELECT table_name FROM information_schema.TABLES WHERE table_schema='%s';" % (dbname)
            col, results = self.mysql_query(connectinfo,sql)
        # get create table sql
        elif (flag == 2):
            # sql = "SELECT ORDINAL_POSITION AS POS,COLUMN_NAME,COLUMN_TYPE,COLUMN_DEFAULT,IS_NULLABLE,COLUMN_KEY,EXTRA,COLUMN_COMMENT FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = '%s' AND TABLE_NAME = '%s' order by POS;" % (dbname,tablename)
            sql = "show create table %s.%s;" % (dbname,tablename)
            col, results = self.mysql_query(connectinfo,sql)
        # get table columns
        elif (flag == 3):
            sql = "SELECT CONCAT(COLUMN_NAME,', ',COLUMN_TYPE) AS COLUMNS FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = '%s' AND TABLE_NAME = '%s';" % (dbname,tablename)
            col, results = self.mysql_query(connectinfo,sql)
        # get table index
        elif (flag == 4):
            sql = "SELECT CONCAT(INDEX_NAME,' (',GROUP_CONCAT(column_name ORDER BY seq_in_index),')') AS INDEXES FROM information_schema.statistics WHERE TABLE_SCHEMA = '%s' AND TABLE_NAME = '%s' GROUP BY INDEX_NAME ORDER BY INDEX_NAME DESC;" % (dbname,tablename)
            col, results = self.mysql_query(connectinfo,sql)
        return (col,results)

    def exec_cmd(self,cmd):
        res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return res.stdout.read()
    
    def sql_soar(self,flag,sql,dsn):
        soar_path = config.get_conf('soar','soar_path')
        soar_log = config.get_conf('soar','soar_log')
        if (flag ==1):
            # soar_cmd = 'echo ' + '\'' +sql + '\'' + ' | ' + soar_path + ' -test-dsn=' + dsn + ' -allow-online-as-test=true'
            soar_cmd = soar_path + ' -query ' + 'D:\soft\soar\\test.sql' + ' -test-dsn=' + dsn + ' -allow-online-as-test=true'
            print (soar_cmd)
            re = self.exec_cmd(soar_cmd)
        return re