#!/usr/bin/env python
# -*- coding=utf-8 -*-

__doc__ = """\
定义一些数据库操作的类

从数据库里面取数据
"""

import threading
import config
try:
    import MySQLdb
    MYSQL_FLAG = True
except Exception, e:
    MYSQL_FLAG = False

class GetDataFromDatabase(threading.Thread):
    def __init__(self, autndbs_name):
        threading.Thread.__init__(self)
        self.autndbs_name = autndbs_name
        if MYSQL_FLAG:
            self.dbconn = MySQLdb.connect(host=config.DATABASE['host'],
                                          port=config.DATABASE['port'], 
                                          user=config.DATABASE['user'],
                                          passwd=config.DATABASE['pass'],
                                          db=config.DATABASE['dbname'])
            self.dbcursor = self.dbconn.cursor()

    def get_data(self):
        """从数据里面取数据"""
        results = {}
        for dbname in self.autndbs_name:
            sql = self.get_sql_statement(dbname)
            n = self.dbcursor.execute(sql)
            res = self.dbcursor.fetchall()
            results[dbname] = []
            for rows in res:
                for field in rows:
                    results[dbname].append(field)

        return results

    def get_sql_statement(self, autndb):
        """获取指定仓库用来fetch的sql语句

        这个sql语句用来取主键

        Args:
            autndb: idol里面仓库的名字

        Returns:
            list include autndb specify
            """
        if None == autndb:
            return None

        sql = None
        if config.SQL_LIST.has_key(autndb):
            sql = config.SQL_LIST[autndb]

        return sql

    def get_all_sql(self):
        sqls = {}
        for dbname in self.autndbs_name:
            sqls[dbname] = self.get_sql_statement(dbname)
        return sqls

    def write_data_to_file(self):
        results = self.get_data()
        for db in results.keys():
            fp = open(db+'.csv', 'w')
            for l in results[db]:
                s = ",".join(["%s"]*len(l)) + "\n"
                fp.write(s % l)
            fp.close()
        

    def __del__(self):
        if MYSQL_FLAG:
            self.dbcursor.close()
            self.dbconn.close()

