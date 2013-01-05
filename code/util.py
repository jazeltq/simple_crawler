#!/usr/bin/env python
#coding:utf-8

import sys

class Util:
    @staticmethod
    def p(s):
        en_type = sys.getfilesystemencoding()
        print s.decode('UTF-8').encode(en_type)
    @staticmethod
    def p_line():
        try:
            raise Exception
        except:
            f = sys.exc_info()[2].tb_frame.f_back
            return (f.f_code.co_name, f.f_lineno)
# 打印行号
p_l = Util.p_line

# 安全打印
p = Util.p

class Singleton(object):
    """
    单件
    """
    objs = {}
    def __new__(cls, *args, **kv):
        if cls in cls.objs:
            return cls.objs[cls]
        cls.objs[cls] = object.__new__(cls)
        
    
def test():
    import logging, traceback
    try:
        logger = logging.getLogger("test")
        #logger.setLevel(3)
        logger.info("hello")
    except:
        traceback.print_exc()
        
        
if __name__ == "__main__":
    test()
    