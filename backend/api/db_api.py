#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pymysql
import json,datetime,time
import subprocess
from pymongo import MongoClient
import ply.lex as lex, re
from bson import json_util
import redis

class db_api():

    def __init__(self):
        pass

    def mysql_query(self,connectinfo,sql,sqllimit=None):
        conn_host = connectinfo['conn_host']
        conn_port = connectinfo['conn_port']
        conn_user = connectinfo['conn_user']
        conn_passwd = connectinfo['conn_passwd']
        conn_db = connectinfo['conn_db']
        # default_limit = int(config.get_conf('sqllimit','limit'))
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
            # results = cursor.fetchall()
            if sqllimit:
                results = cursor.fetchmany(size=int(sqllimit))
            else:
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

    def get_metadata(self,flag,connectinfo,dbname=None,tablename=None):
        # 获取对应实例下的数据库
        if (flag == 0):
            # dbname = meta_info['dbname']
            sql = "SELECT DISTINCT table_schema FROM information_schema.TABLES WHERE table_schema NOT IN ('sys','information_schema','mysql','performance_schema','percona','infra','pt','youcai');"
            col, results = self.mysql_query(connectinfo,sql)
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
        elif (flag == 5):
            sql = '''select concat(user,'@',"'",host,"'") as "user@host" from mysql.user;'''
            col, results = self.mysql_query(connectinfo,sql)
        # show full processlist
        elif (flag == 6):
            sql = "select * from information_schema.processlist;"
            col, results = self.mysql_query(connectinfo,sql)
        # show active
        elif (flag == 7):
            sql = "select * from information_schema.processlist where COMMAND!='Sleep' and USER!='system user';"
            col, results = self.mysql_query(connectinfo,sql)
        # show engine
        elif (flag == 8):
            sql = "show engine innodb status;"
            col, results = self.mysql_query(connectinfo,sql)
        # show master status
        elif (flag == 9):
            sql = "show master status;"
            col, results = self.mysql_query(connectinfo,sql)
        # show salve status
        elif (flag == 10):
            sql = "show slave status;"
            col, results = self.mysql_query(connectinfo,sql)
        return (col,results)

    def exec_cmd(self,cmd):
        res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return res.stdout.read()

    def soar_sql_file(self, sql,username):
        file_time = time.strftime('%Y%m%d%H%M%S',time.localtime())
        soar_file_tmp = config.get_conf('soar','soar_file_tmp')
        soar_sql__tmpfile = soar_file_tmp + username + '.txt'
        try:
            f = open(soar_sql__tmpfile,'w')
            f.write(sql)
        except OSError as e:
            return e
        finally:
            if f in locals():
                f.close()
            return soar_sql__tmpfile

    def sql_soar(self,flag,sql,dsn,username):
        soar_path = config.get_conf('soar','soar_path')
        soar_log = config.get_conf('soar','soar_log')
        soar_sql_file = self.soar_sql_file(sql,username)
        if (flag ==1):
            # soar_cmd = 'echo ' + '\'' +sql + '\'' + ' | ' + soar_path + ' -test-dsn=' + dsn + ' -allow-online-as-test=true'
            #soar_cmd = soar_path + ' -query ' + 'D:\soft\soar\\test.sql' + ' -test-dsn=' + dsn + ' -allow-online-as-test=true'
            soar_cmd = soar_path + ' -query ' + soar_sql_file + ' -test-dsn=' + dsn + ' -allow-online-as-test=true'
            re = self.exec_cmd(soar_cmd)
        return re

    def mongodb_query(self,flag,connectinfo,sql=None):
        conn_host = connectinfo['conn_host']
        conn_port = connectinfo['conn_port']
        conn_user = connectinfo['conn_user']
        conn_passwd = connectinfo['conn_passwd']
        client = MongoClient(conn_host,conn_port)
        db_auth = client.admin
        db_auth.authenticate(conn_user, conn_passwd)
        if (flag == 0):
            re = client.database_names()
        elif (flag == 1):
            conn_db = connectinfo['conn_db']
            db = getattr(client,conn_db)
            re = db.collection_names()
        elif (flag == 2):
            conn_db = connectinfo['conn_db']
            db = getattr(client,conn_db)
            execresults = eval(sql)
            # re = {'results' : ''}
            re = []
            for i in execresults:
                # re["results"].append(i)
                re.append(json_util.dumps(i))
            # re = db.userDetail.find_one()
            # print ('222', re)
        return re

    def redis_query(self,flag,connectinfo,rediskey=None):
        conn_host = connectinfo['conn_host']
        conn_port = connectinfo['conn_port']
        conn_passwd = connectinfo['conn_passwd']
        conn_db = connectinfo['conn_db']
        
        if (flag == 1):
            r = redis.Redis(host=conn_host, port=conn_port, password=conn_passwd, db=conn_db,decode_responses=True)
            re = r.get(rediskey)
        return re

    def extract_table_name_from_sql(self,sql_str):
        # remove the /* */ comments
        q = re.sub(r"/\*[^*]*\*+(?:[^*/][^*]*\*+)*/", "", sql_str)
        # remove whole line -- and # comments
        lines = [line for line in q.splitlines() if not re.match("^\s*(--|#)", line)]
        # remove trailing -- and # comments
        q = " ".join([re.split("--|#", line)[0] for line in lines])
        # split on blanks, parens and semicolons
        tokens = re.split(r"[\s)(;]+", q)
        # scan the tokens. if we see a FROM or JOIN, we set the get_next
        # flag, and grab the next one (unless it's SELECT).
        result = set()
        get_next = False
        for token in tokens:
            if get_next:
                if token.lower() not in ["", "select"]:
                    result.add(token)
                get_next = False
            get_next = token.lower() in ["from", "join"]

        return result