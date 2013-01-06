#!/usr/bin/env python
#encoding:utf-8

import threading, time, urllib2, urlparse
import socket, traceback, logging

from thread_pool import ThreadPool
from Queue import Empty
from collections import deque
from sgmllib import SGMLParser, SGMLParseError
from web_page import WebPage
from my_logger import MyLogger
from database import Db


class Crawler():
    def __init__(self, myconfig):
        # 线程池, 
        self.thread_pool = ThreadPool(myconfig.thread)
        # 已访问的url集合
        self.visited_urls = set()
        # set 不是线程安全，所以这里加一把锁
        self.visited_urls_lock = threading.Lock()
        # 未访问的url集合
        self.will_visited_urls = deque()
        self.will_visited_urls.append(myconfig.url)
        self.temp_q = deque()
        self.cur_depth = 0
        self.status = ""
        self.myconfig = myconfig
        #MyLogger(myconfig.logfile, myconfig.loglevel)
        MyLogger(myconfig.logfile, loglevel = 5)
        self.db = Db()
        
    
    def start(self):
        self.status = "start"
        while self.cur_depth < self.myconfig.depth:
            if self.status == "stop":
                break
            try:
                while self.will_visited_urls:
                    url = self.will_visited_urls.popleft()
                    # 添加工作，这里基本上没有阻塞，因为是在主线程里，只是负责
                    # 添加工作，真正执行工作是在线程里做的
                 
                    self.thread_pool.add_job(self.handler, url)
                #
                # TODO:
                # 通知线程有活干了，这里可以看出是在将will_visited_urls的url
                # 都添加后才通知线程去干活的，这样设计，粒度似乎有点粗？
                # 如果还想节省时间的话，可以在url的数目 >= 线程初始数目的时候，就通知
                # 线程池里的线程开始干活，如果url的数目 < 线程初始数目的时候，等都
                # 添加完之后，再通知
                
                #print ">>>>>>>>  give event to threads in thread pool"
                # 通知线程池里的线程开始新一轮的抓取
                self.thread_pool.event_do_job()
                # 主动退出调度，让子线程有时间可以执行
                time.sleep(3)
            except Empty:
                # 需要访问的url没有了
                logging.info("no url right now")
            finally:
                
                # 必须等线程池里的线程工作做完之后，才算本次深度的访问结束
                # 这里做的处理是如果线程池里面有线程，则睡3s，再读，
                # 直到线程池里的工作线程为0才停下来
                # 这样才算本次深度的抓取完毕
                while True:
                    #print "thread waiting num is %d, config thread num is %d" % (self.thread_pool.get_thread_waiting_num(), self.myconfig.thread)
                    if self.thread_pool.get_thread_waiting_num() == self.myconfig.thread:
                        # 如果等待的线程数目等于线程初始数目，则说明，所有线程都执行完毕
                        # 所以break
                        break
                    else:
                        # 有线程仍然在执行，则说明， 本次深度的访问还没有结束
                        # 睡眠等待
                        time.sleep(10)
                #此次深度的访问结束，深度加一
                self.cur_depth += 1
                logging.info("crawler depth now is %s" % str(self.cur_depth))
                if self.cur_depth > self.myconfig.depth:
                    break
                # 从url中抓到的网页都放到了temp_q中,
                # 将temp_q中的网页从新给 will_visited_urls，继续
                self.will_visited_urls = self.temp_q
                self.temp_q = deque()
                
                
        # 所有深度的url都抓取完毕 or 爬虫退出
        self.thread_pool.stop_threads()
        logging.info("crawler exit")
        return
        
            
    def handler(self, url):
        content= self.get_html_content(url)
        if content == "" or content == None:
            # 无法获取content，直接返回
            return
        # 添加此url为已访问过
        self.add_url_to_visited(url)
        if content.find(self.myconfig.key) != -1:
            self.db.save_data(url, self.myconfig.key, content)
        try:
            hrefs = self.get_hrefs(content, url)
        except StandardError, se:
            logging.error("error: %s" % (se))
            print se
            # log
            # 无法获取 hrefs
            return
        # 如果获得了hrefs
        if hrefs:
            # 将hrefs添加到 temp_q中，等本级深度访问完毕之后再访问
            for link in hrefs:
                # 最后的考验
                if not self.is_url_visited(link) \
                            and link not in self.will_visited_urls \
                            and link not in self.temp_q:
                    #print "put %s into temp_q" % link 
                    self.temp_q.append(link)
        
    def add_url_to_visited(self, url):
        # 
        self.visited_urls_lock.acquire()
        self.visited_urls.add(url)
        self.visited_urls_lock.release()
        
    def get_url_visited(self):
        # 
        self.visited_urls_lock.acquire()
        n = len(self.visited_urls)
        self.visited_urls_lock.release()
        return n
        
    def is_url_visited(self, url):
        # in: true
        # not in: false
        a = False
        self.visited_urls_lock.acquire()
        a = url in self.visited_urls
        self.visited_urls_lock.release()
        return a
    
    def get_hrefs(self, content, url):
        try:
            if content == None or content == "":
                return;
            url_p = urlparse.urlparse(url)
            if url_p.netloc == "":
                # url 是相对地址，或者无法解析出net location
                #raise StandardError("url urlpase result has nos no netloc")
                return
            hrefs = []
            parser = self.get_parser()
            parser.feed(content)
            full_url = None
            for link in parser.urls:
                if link == "" or link == "#" or link == "javascript:void(0)":
                    continue
                # 这里先过滤掉非url形式的字符串
                # 因为parser解析的仅仅是a标签，所以不一定保证得到的就是
                # url
                if link.find('http') != 0 and link.find('https') != 0 and link.find('/') != 0 and link.find('./')!=0 and link.find('../')!= 0:
                    continue
                link_p = urlparse.urlparse(link)
                if link_p.netloc == "":
                    # 如果是相对地址
                    full_url = url_p.netloc + link
                else:
                    full_url = link
                # 添加到list中
                #print full_url
                hrefs.append(full_url)
        except Exception, e:
            traceback.print_exc()
            logging.error("exception:%s" % e)
        parser.close()
        return hrefs
    
    def get_html_content(self, url):
        # 一种是通过urllib2 返回html content，
        # 另外是通过 requests返回
        return self._get_html_content_by_requests(url)
    
    def _get_html_content_by_urllib2(self, url):
        try:
            content = urllib2.urlopen(url, timeout=5).read()
        except socket.timeout, e:
            # log 
            content = ""
        except urllib2.URLError, e:
            # log
            content = ""
        except Exception, e:
            # lgo
            content = ""
        finally:
            return content
        
    def _get_html_content_by_requests(self, url):
        # refer用的是base url
        w = WebPage(url, self.myconfig.url)
        try:
            w.fetch()
            c = w.getDatas()[1]
            return c
        except Exception, e:
            return ""
        
    def get_parser(self):
        return Parser()
    
    def is_avaliable(self):
        if self.status != "stop":
            return True
        else:
            return False
    def stop_crawling(self):
        if self.is_avaliable():
            self.status = "stop"
        else:
            # 直接pass
            pass
        
    def print_progress(self):
        if self.is_avaliable():
            print '================================='
            print 'Crawling depth is ', self.cur_depth
            print 'urls visited is ', self.get_url_visited()
            print 'thread working is', self.myconfig.thread - self.thread_pool.get_thread_waiting_num()
            print 'url content matched number is', self.db.get_row_num()
            print '================================'

class Parser(SGMLParser):
    """
    通过sgml 来获取url 
    """
    def __init__(self):
        SGMLParser.__init__(self)
        self.urls = []
    def start_a(self, attrs):
        href = [ v for k, v in attrs if k == 'href']
        if href:
            self.urls.extend(href)
    def feed(self, data):
        try:
            SGMLParser.feed(self, data)
        except SGMLParseError, e:
            logging.error("parser meets an error:%s" % e)
            

def __test():
    """
    具体的测试
    """
    def print_result(c):
        while True:
            if c.is_avaliable():
                c.print_progress()
            time.sleep(3)
            
    from config import MyConfig
    MyConfig.do_default()
    c = Crawler(MyConfig)
    threading.Thread(group = None, target=print_result, args=(c,)).start()
    c.start()

def _test():
    """
    对外的测试接口
    """
    __test()
if __name__ == "__main__":
    _test()