#!/usr/bin/env python
#coding:utf-8

import logging

class My_logger():
    
    def __init__(self, logfile = "spider.log", loglevel=3):
        SPIDER_LOG_LEVEL={ 5:logging.DEBUG,
                           4:logging.INFO,
                           3:logging.WARNING,
                           2:logging.ERROR,
                           1:logging.CRITICAL}
        FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
        log_config={'filename': logfile,
                    'level':SPIDER_LOG_LEVEL[loglevel],
                    'format':FORMAT
                    }
        #logging.basicConfig(filename=log_config['filename'], level=log_config['level'],format=log_config['format'] )
        logging.basicConfig(**log_config)
        
    def get_logger(self, name):
        return logging.getLogger(name)
    
    
def __test():
    pass

def _test():
    pass

if __name__ == "__main__":
    _test()
    