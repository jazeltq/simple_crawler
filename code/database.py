#!/usr/bin/env python
#coding:utf-8

"""
 数据库相关的操作
"""

import sqlite3, logging


class Db:
    def __init__(self, dbfile = "test.db", logger = None):
        """
         数据库初始化
        """
        if logger:
            self.logger = logger.get_logger("sqlite3")
        else:
            self.logger = logging.getLogger('sqlite3')
        self.conn = sqlite3.connect(dbfile, isolation_level = None, check_same_thread = False)
        self.conn.execute("create table if not exists url_result(\
                    id integer primary key autoincrement, \
                    url text, \
                    key_word text,\
                    page_source text)")
        self.logger.info("db connect")
        
    def save_data(self, url, key, content):
        """
         保存数据
        """
        if self.conn:
            sql = "insert into url_result (url, key_word, page_source) values (?,?,?);"
            self.conn.execute(sql, (url, key, content))
            self.logger.info("execute %s" % sql)
        else:
            # log
            self.logger.error("database connection is not available!")
            raise sqlite3.Error(" Database connection is not available!")
            
    def close_conn(self):
        """
         关闭连接
        """
        if self.conn:
            self.conn.close()
            self.logger.info("close db connection!")
        else:
            self.logger.error("database connection is not available!")
            raise sqlite3.Error("Database connection is not available!")
        
