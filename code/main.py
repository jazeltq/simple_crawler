#!/usr/bin/env python
#encoding:utf-8

import threading, time

from crawler import Crawler
from config import get_config, MyConfig

class progress_info(threading.Thread):
    
    def __init__(self, crawler):
        threading.Thread.__init__(self)
        self.crawler = crawler
        self.start()
        
    def run(self):
        while True:
            if self.crawler.is_avaliable():
                self.crawler.print_progress()
                time.sleep(5)
                
def main():
    myconfig = get_config()
    
    if myconfig == False:
        return
    
    if myconfig == None:
        print "do not have any configuration, then siwtch testself truns on!"
        myconfig = MyConfig()
        myconfig.testself = True
    
    if myconfig.testself:
        # 如果 testself开关 trun on
        # 则 其它设置默认无效
        myconfig.do_default()
    myconfig.show_config()
    crawler = Crawler(myconfig)
    progress_info(crawler)
    crawler.start()
    
if __name__ == "__main__":
    main()