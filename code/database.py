#!/usr/bin/env python
#coding:utf-8

"""
 数据库相关的操作
"""

import sqlite3


class Db:
    def __init__(self, dbfile = "test.db", logger = None):
        """
         数据库初始化
         dbfile:数据库文件名
         logger:就是logger
        """
        self.conn = sqlite3.connect(dbfile, isolation_level = None, check_same_thread = False)
        self.conn.execute("create table if not exists url_result(\
                    id integer primary key autoincrement, \
                    url text, \
                    key_word text,\
                    page_source text)")
        # not yet
        self.logger = None
        #the_logger.info("db connect")
        
    def save_data(self, url, key, content):
        """
         保存数据
        """
        if self.conn:
            sql = "insert into url_result (url, key_word, page_source) values (?,?,?);"
            self.conn.execute(sql, (url, key, content))
        else:
            # log
            raise sqlite3.Error(" Database connection is not available!")
            
    def close_conn(self):
        """
         关闭连接
        """
        if self.conn:
            self.conn.close()
        else:
            raise sqlite3.Error("Database connection is not available!")
        
    def log_or_p(self, message, level):
        """
         记录日志
        """
        if self.logger:
            self.loger.info(message)
        else:
            # 没有logger的话，这里就不打印了哈。。。
            pass