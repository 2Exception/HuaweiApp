# -*- coding: utf-8 -*-

__author__ = 'liuyang'

import urllib2
import sys
import threading
import time
reload(sys)
sys.setdefaultencoding('utf-8')

# 读取待检测ip
f = open("ip.txt")
rawProxyList = []
for line in f.readlines():
    line = line.strip('\n')
    rawProxyList.append(line)
print rawProxyList
checkedProxyList = []

#检验代理的类
class ProxyCheck(threading.Thread):
    def __init__(self,proxyList):

        threading.Thread.__init__(self)
        self.proxyList = proxyList
        self.timeout = 5
        self.testUrl = "http://college.gaokao.com/school/tinfo/1/result/1/1/"
        self.testStr = "huawei"

    def checkProxy(self):
        cookies = urllib2.HTTPCookieProcessor()
        # 检测每个代理是否可用
        for proxy in self.proxyList:
            proxyHandler = urllib2.ProxyHandler({"http" : r'http://%s' %proxy})
            # print r'http://%s:%s' %(proxy[0],proxy[1])
            opener = urllib2.build_opener(cookies,proxyHandler)
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1')]
            urllib2.install_opener(opener)
            t1 = time.time()

            try:
                req = urllib2.urlopen("http://appstore.huawei.com/app/C7166", timeout=self.timeout)
                # req = opener.open(self.testUrl, timeout=self.timeout)
                print "urlopen is ok...."
                result = req.read()
                print "read html...."
                timeused = time.time() - t1
                pos = result.find(self.testStr)
                print "pos is %s" %pos

                if (pos > -1):
                    if timeused<3:
                        checkedProxyList.append(proxy)
                        print proxy
                else:
                    continue

            except Exception,e:
                continue

    def sort(self):
        sorted(checkedProxyList,cmp=lambda x,y:cmp(x[1],y[1]))

    def run(self):
        self.checkProxy()
        # self.sort()

if __name__ == "__main__":
    getThreads = []
    checkThreads = []

    #开启20个线程负责校验，将抓取到的代理分成20份，每个线程校验一份
    for i in range(20):
        t = ProxyCheck(rawProxyList[((len(rawProxyList)+19)/20) * i:((len(rawProxyList)+19)/20) * (i+1)])
        checkThreads.append(t)

    for i in range(len(checkThreads)):
        checkThreads[i].start()


    for i in range(len(checkThreads)):
        checkThreads[i].join()


    print ".......................总共有%s个代理通过校验......................." %len(checkedProxyList)

    #持久化
    f= open("G:\\t1.txt",'w+')
    for proxy in checkedProxyList:
        f.write('"http://' + proxy + '",' +  '\r\n')
    f.close()
