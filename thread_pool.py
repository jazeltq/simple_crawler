#!/usr/bin/env python
#coding:utf-8

"""
 线程池类封装
 线程在工作队列没有工作的时候，阻塞在 没有工作 这个事件上
 当工作队列添加了工作之后，可以激活线程继续工作
"""

import threading, traceback
from Queue import Queue, Empty
from util import p_l, p


class A_thread(threading.Thread):
    """
    具体的工作线程，采用的线程模型是
    1 工作队列为空的时候，等待线程数加一
    2 等待线程阻塞在 没有工作 这个事件上
    3 当从阻塞事件上返回的时候，等待线程数减去一
    """
    def __init__(self, tp, timeout=3, **kwargs):
        threading.Thread.__init__(self, kwargs=kwargs)
        #线程在结束前等待任务队列多长时间
        self._timeout = timeout
        self._thread_pool = tp
        self._status = "start"
        self.try_times = 0
        self.queue_empty = False
        self.fatal_error = False
        self.setDaemon(True)
        self.start()

    def run(self):
        
        while True:
            if self._status == "stop":
                #print ("%s exit !" % threading.current_thread().getName())
                return
            try:
                # 从工作队列中获取一个任务
                call_able,args, kargs = self._thread_pool.get_one_job()
                # 做相关的工作
                call_able(*args, **kargs)
            except Empty:
                self.queue_empty = True
            except Exception, e:
                self.fatal_error = True
                # 走到这里说明，线程遇到不可知的错误
                print ("%s: fatal error " % threading.current_thread().getName())
                print ("*****%s" % e)
                traceback.print_exc()
            finally:
                if self.queue_empty:
                    # 工作队列中没有工作了，线程等待的数目加一
                    self._thread_pool.inc_thread_waiting_num()
                    # log
                    #print "%s has no job to do now" % threading.current_thread().getName()
                    #print( "没活干了" )
                    # 阻塞在没有工作的事件上
                    self._thread_pool.event_no_job()
                    # 从这里返回说明，有事件，这样等待工作的线程数目就可以减一
                    self._thread_pool.dec_thread_waiting_num()
                    self.queue_empty = False
                    #print( "我靠， 终于有活干了" )
                elif self.fatal_error:
                    if self.try_times > self._thread_pool.try_times:
                        self._status = "stop"
                    else:
                        self.try_times += 1
    def stop(self):
        self._status = "stop"

class ThreadPool:
    def __init__(self, num_of_threads = 10):
        self._workQueue = Queue()
        self._threads = []
        # 没有工作的线程数，初始为0
        self.thread_waiting_num = 0
        self.thread_waiting_num_lock = threading.Lock()
        self.no_job_event = threading.Event()
        self.thread_timeout = 3
        self.try_times = 3
        self.__createThreadPool(num_of_threads)
        
    def __createThreadPool(self, num_of_threads):
        
        for i in range(num_of_threads):
            self._threads.append(A_thread(self))
            
    def add_job(self, call_able, *args, **kargs):
        self._workQueue.put((call_able, args, kargs))
        
    def inc_thread_waiting_num(self):
        # 
        self.thread_waiting_num_lock.acquire()
        self.thread_waiting_num += 1
        self.thread_waiting_num_lock.release()
        
    def dec_thread_waiting_num(self):
        # 
        self.thread_waiting_num_lock.acquire()
        self.thread_waiting_num -= 1
        self.thread_waiting_num_lock.release()
    
    def get_thread_waiting_num(self):
        # 获取正在干活的线程的个数
        self.thread_waiting_num_lock.acquire()
        res = self.thread_waiting_num
        self.thread_waiting_num_lock.release()
        return res
        
    def stop_threads(self):
        for t in self._threads:
            t.stop()
        # 假激活，哈哈
        self.event_do_job()
        for t in self._threads:
            if t.isAlive():
                t.join()
                
    def event_no_job(self):
        if self.no_job_event.is_set():
            self.no_job_event.clear()
        # 没有工作的时候阻塞
        #print "thread waiting num %d" % self.get_thread_waiting_num()
        self.no_job_event.wait()
        
    def event_do_job(self):
        
        # 如果有线程等待，则唤醒线程
        if self.get_thread_waiting_num():
            self.no_job_event.set()
        else:
            # 没有线程等待，直接返回
            return
    
    def get_one_job(self):
        try:
            j = self._workQueue.get(timeout=self.thread_timeout)
            return j
        except Empty:
            raise Empty
        
class __test(object):
    """
     测试线程池
    """
    def __init__(self):
        self.num = 0;
        self.num_lock = threading.Lock()
        pass
    def handler(self):
        # 阻塞 
        for i in xrange(10000):
            if self.num_lock.acquire():
                self.num += 1
                self.num_lock.release()
    def do_test(self):
        import time
        # 三个线程
        tp = ThreadPool(3)
        # 添加了13个工作
        for i in range(13):
            tp.add_job(self.handler)
        # 开始干活
        tp.event_do_job()
        # 让出cpu
        time.sleep(5)
        while tp.get_thread_waiting_num() != 3:
            time.sleep(5)
        # 结束线程
        tp.stop_threads()
        if self.num == 13*10000:
            print "%d ?= %d" % (self.num, 13*10000)
            print "Test ok: ThreadPool seems not let u down"
        else:
            print "Test Error: ThreadPool is not reliable"

def _test():
    """
    测试
    """
    __test().do_test()
            
if __name__ == "__main__":
    _test()
