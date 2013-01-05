#!/usr/bin/env python
#coding:utf-8

import logging


SPIDER_LOG_LEVEL={ 5:logging.DEBUG,
                   4:logging.INFO,
                   3:logging.WARNING,
                   2:logging.ERROR,
                   1:logging.CRITICAL}
class My_logger():
    def __init__(self, logfile = "spider.log", loglevel=3):
        FORMAT = "%(asctime)s %(name)s [%(levelname)s] [%(message)s]"
        log_config={'filename': logfile,
                    'level':SPIDER_LOG_LEVEL[loglevel],
                    'format':FORMAT
                    }
        logging.basicConfig(**log_config)
    def getLogger(self, name):
        return logging.getLogger(name)
    
    
def __test():
    l = My_logger().getLogger("test")
    l.debug("just a test")
    l.info("just a test")
    l.warning("just a test")
    l.error("just a test")
    l.critical("just a test")
    l.info("just a test")
    
    l = My_logger().getLogger("world")
    l.debug("just a world")
    l.info("just a world")
    l.warning("just a world")
    l.error("just a world")
    l.critical("just a world")
    l.info("just a world")

def _test():
    __test()

if __name__ == "__main__":
    _test()
    