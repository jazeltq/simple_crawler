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
    threadnum=0
    key=""
    
    @classmethod
    def do_default(cls):
        cls.url = "http://www.iqiyi.com"
        cls.depth = 2
        cls.logfile = "spider.log"
        cls.dbfile = "sqlite.db"
        cls.loglevel = 3 # warning
        cls.testself = False
        cls.threadnum = 10
        cls.key = "HTML5"
        
    @classmethod
    def clear_config(cls):
        cls.url=""
        cls.depth=0
        cls.logfile=""
        cls.dbfile=""
        cls.loglevel=0
        cls.testself=False
        cls.threadnum=0
        cls.key=""
        
    @classmethod
    def show_config(cls):
        c = "url:%s depth:%d logfile:%s loglevel:%d dbfile:%s testself:%s threadnum:%d key:%s" % \
            (cls.url, cls.depth, cls.logfile, cls.loglevel, cls.dbfile, cls.testself, cls.threadnum, cls.key)
        print "\nyour configuration:\n", c
        
    @classmethod
    def check_config(cls):
        """
        主要目的是当从命令行没有获取相关的
        参数的时候，可以配置成默认的
        """
        if cls.testself == True:
            return
        if cls.url == "":
            cls.url = "http://www.iqiyi.com"
        if cls.depth == 0:
            cls.depth = 2
        if cls.logfile == "":
            cls.logfile = "spider.log"
        if cls.loglevel == 0:
            cls.loglevel = 3 # warning
        if cls.threadnum == 0:
            cls.threadnum = 10
        if cls.key == "":
            cls.key = "HTML5"
            
def get_config():
    """
    参数正确解析：返回Myconfig对象
    参数解析错误：返回False
    没有参数返回: None
    """
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'f:l:u:d:', ["key=", "testself", "dbfile=", "thread=", "help"])
    except getopt.error, e:
        print e
        import traceback
        traceback.print_exc()
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
    print "do default>>>>>>>>>>>>>>>>"
    MyConfig.do_default()
    MyConfig.show_config()
    print a
    print "clear config>>>>>>>>>>>>>>>>"
    MyConfig.clear_config()
    MyConfig.show_config()
    print "check config---------------"
    MyConfig.clear_config()
    MyConfig.check_config()
    MyConfig.show_config()
    print "test get_config-------"
    # 不想每次都写参数，就这样赋值测试了
    l = sys.argv
    # test depth
    l.append("-d")
    l.append("5")
    print "test -d 5", get_config().show_config()
    # test logfile
    del l[1:]
    l.append("-f")
    l.append("log_file")
    MyConfig.clear_config()
    print "test -f log_file", get_config().show_config()
    
    del l[1:]
    l.append("-u")
    l.append("http://www.iqiyi.com")
    MyConfig.clear_config()
    print "test -u http://www.iqiyi.com", get_config().show_config()
    
    del l[1:]
    l.append("-l")
    l.append("3")
    MyConfig.clear_config()
    print "test -l 3", get_config().show_config()
    
    del l[1:]
    l.append("--key")
    l.append("jfkldsajlkfd")
    MyConfig.clear_config()
    print "test --key jfkldsajlkfd", get_config().show_config()
    
    del l[1:]
    l.append("--dbfile")
    l.append("db.file")
    MyConfig.clear_config()
    print "test --dbfile db.file", get_config().show_config()
    
    del l[1:]
    l.append("--thread")
    l.append("13")
    MyConfig.clear_config()
    print "test --thread 13", get_config().show_config()
    
    del l[1:]
    l.append("--testself")
    MyConfig.clear_config()
    print "test --testself", get_config().show_config()
    
    del l[1:]
    opt_l = ["-u", "http://www.baidu.com", "-f", "log_file", "-d", "3", "-l", "3",
             "--key", "HTML5", "--testself", "--dbfile", "test.db", "--thread", "12"]
    l.extend(opt_l)
    MyConfig.clear_config()
    print "test all:", " ".join(opt_l), get_config().show_config()
    
def _test():
    test()
    
if __name__ == "__main__":
    _test()
    