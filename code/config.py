#!/usr/bin/env python
#coding:utf-8

import sys, getopt
from util import Util

def usage():
    the_usage = """spider.py -u url -d deep -f logfile -l loglevel(1-5)  --testself --thread number --dbfile  filepath  --key=”HTML5” 
    
        参数说明：
        
        -u 指定爬虫开始地址
        
        -d 指定爬虫深度
        
        --thread 指定线程池大小，多线程爬取页面，可选参数，默认10
        
        --dbfile 存放结果数据到指定的数据库（sqlite）文件中
        
        --key 页面内的关键词，获取满足该关键词的网页，可选参数，默认为所有页面
        
        -l 日志记录文件记录详细程度，数字越大记录越详细，可选参数，默认spider.log
        
        --testself 程序自测，可选参数 """
    Util.p(the_usage)
    
class MyConfig(object):
    """
    TODO: MyConfig 改为单件
    """
    url=""
    depth=0
    logfile=""
    dbfile=""
    loglevel=0
    testself=False
    thread=0
    key=""
    
    @classmethod
    def do_default(cls):
        cls.url = "http://www.iqiyi.com"
        cls.depth = 2
        cls.logfile = "spider.log"
        cls.dbfile = "sqlite.db"
        cls.loglevel = 3 # warning
        cls.testself = False
        cls.thread = 10
        cls.key = "HTML5"
        
    @classmethod
    def clear_config(cls):
        cls.url=""
        cls.depth=0
        cls.logfile=""
        cls.dbfile=""
        cls.loglevel=0
        cls.testself=False
        cls.thread=0
        cls.key=""
        
    @classmethod
    def show_config(cls):
        c = "url:%s depth:%d logfile:%s loglevel:%d dbfile:%s testself:%s thread:%d key:%s" % \
            (cls.url, cls.depth, cls.logfile, cls.loglevel, cls.dbfile, cls.testself, cls.thread, cls.key)
        print "your configuration:\n", c


def get_config():
    """
    参数正确解析：返回Myconfig对象
    参数解析错误：返回False
    没有参数返回: None
    """
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'f:l:u:d:', ["key=", "testself", "dbfile=", "thread=", "help"])
    except getopt.error:
        usage()
        return False
    
    if len(opts) == 0:
        return None
    for o, v in opts:
        if o == "-u":
            MyConfig.url = v
        elif o == "-d":
            if str.isdigit(v):
                MyConfig.depth = int(v)
            else:
                MyConfig.depth = 2
        elif o == '-f':
            MyConfig.logfile = v
        elif o == '-l':
            if str.isdigit(v):
                MyConfig.loglevel = int(v)
            else:
                MyConfig.loglevel = 0
        elif o == '--key':
            MyConfig.key = v
        elif o == '--testself':
            MyConfig.testself = True
        elif o == '--dbfile':
            MyConfig.dbfile = v
        elif o == '--thread':
            if str.isdigit(v):
                MyConfig.threadnum = int(v)
            else:
                MyConfig.threadnum = 10
        elif o == "--help":
            usage()
            return False
        else:
            print "Error, %s can not be used!" % o
            usage()
            # 直接返回
            return None
    return MyConfig

def test():
    a = MyConfig()
    print a
    print ">>>>>>>>>>>>>>>>"
    MyConfig.do_default()
    MyConfig.show_config()
    print a
    print ">>>>>>>>>>>>>>>>"
    MyConfig.clear_config()
    myconfig = get_config()
    myconfig.show_config()
    
def _test():
    test()
    
if __name__ == "__main__":
    _test()
    