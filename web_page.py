#!/usr/bin/env python
#encoding:utf-8
"""
 get web page content
 
"""

import requests, re, logging

class WebPage(object):

    def __init__(self, url, refer_url = None):
        self.url = url
        if refer_url == None:
            self.refer_url = url
        else:
            self.refer_url = refer_url;
        self.pageSource = None
        self.customeHeaders()

    def fetch(self, retry=2, proxies=None):
        '''获取html源代码'''
        try:
            #设置了prefetch=False，当访问response.text时才下载网页内容,避免下载非html文件
            response = requests.get(self.url, headers=self.headers, timeout=10, proxies=proxies)
            if self._isResponseAvaliable(response):
                self._handleEncoding(response)
                self.pageSource = response.text
                return True
            else:
                pass
        except Exception,e:
            print e
            if retry>0: #超时重试
                return self.fetch(retry-1)
            else:
                pass
        return None

    def customeHeaders(self, **kargs):
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:9.0.1) Gecko/20100101 Firefox/9.0.1',
            'Accept-Language':'en-us,zh-cn;q=0.7,zh;q=0.3',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive',
            #Cookie: vjuids=-b048eba5.129eb2a18f6.0.e1554353908618; vjlast=1356838032; SINAGLOBAL=119.40.36.130.166291279550700586; ULV=1356838024525:182:1:1:4989610303816.123.1356838024522:1352295562132; US1=ca6c2bf0.4276781.4cd9412b.9f1d422a; U_TRS1=d39d8b82.a6ce129b.4d5b5035.c799b287; __utma=269849203.613469539.1293707085.1306713707.1313411819.4; ALLYESID4=00110116203530330564441; UOR=,,; FSINAGLOBAL=119.40.36.130.166291279550700586; SSCSum=1; Apache=4989610303816.123.1356838024522; U_TRS2=000000a7.8f917af6.50dfb488.5c29722f; SinaRot/www///=50; mv2012_sina_lb=0; rpb_1_2=1356838031040; sinaVideoAd=played; CoupletMediahttp://www.sina.com.cn/=0; lxlrtst=1356830087_o; lxlrttp=1356830087
            #If-Modified-Since: Sun, 30 Dec 2012 03:19:11 GMT
            #Cache-Control: max-age=0
            'Referer':self.refer_url
        }
        self.headers.update(kargs)

    def getDatas(self):
        return self.url, self.pageSource

    def _isResponseAvaliable(self, response):
        #网页为200时再获取源码, 只选取html页面。 
        if response.status_code == requests.codes.ok:
            if 'html' in response.headers['Content-Type']:
                return True
        return False

    def _handleEncoding(self, response):
        #requests会自动处理编码问题.
        #但是当header没有指定charset并且content-type包含text时,
        #会使用RFC2616标准，指定编码为ISO-8859-1
        #因此需要用网页源码meta标签中的charset去判断编码
        if response.encoding == 'ISO-8859-1':
            charset_re = re.compile("((^|;)\s*charset=)([^\"]*)", re.M)
            charset=charset_re.search(response.text) 
            charset=charset and charset.group(3) or None 
            response.encoding = charset

def __test():
    w = WebPage('http://www.baidu.com', 'http://wwww.baidu_vs_google.com')
    w.fetch()
    print w.getDatas()[1]
    
def _test():
    __test()

if __name__ == "__main__":
    _test()
   