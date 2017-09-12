# -*- coding: utf-8 -*-
__author__ = 'liuyang'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import scrapy
import time
from ..items import HuaweiAppItem
from ..utils import LogUtil
from ..utils import StrUtil
class HuaweiSpider(scrapy.Spider):

	# 爬虫名字
    name = "huaweiApp"
    # 限制范围
    allowed_domains = ["app.hicloud.com"]
    # URL容器
    start_urls = []

    def __init__(self):
        # 载入start_urls
        self.loadStartURLs()

        # 统计处理url总数
        self.urls_sum = 0L
        return

    # 载入start_urls
    def loadStartURLs(self):
        prefix = "http://appstore.huawei.com/app/C"
        # 固定URL
        for i in range(1,11000000,1):
            self.start_urls.append(prefix + str(i))
        return

    # 解析函数
    def parse(self, response):

        selector = scrapy.Selector(response)

        # APP信息容器
        ite = self.getItem(selector, response)
        if ite != "NULL":
            yield ite

        # 已处理URL数目统计
        self.urls_sum += 1
        if self.urls_sum % 500 == 0:
            LogUtil.HuaweiAPPlog("urls_sum(%d)" % self.urls_sum)

    # 提取Item
    def getItem(self, selector, response):
        # 新建信息容器
        item = HuaweiAppItem()
        # 更新信息
        self.getChannel(selector, item)
        name = self.getName(selector, item)

        # 若名称为空，url不存在，返回空，继续下一个url
        if item["name"] == "NULL":
            return "NULL"
        self.getSize(selector, item)
        self.getCrawlURL(selector, item, response)
        self.getVersion(selector, item)
        self.getUpdateTime(selector, item)
        self.getAuthor(selector, item)
        self.getDownload(selector, item)
        self.getScore(selector, item)
        self.getCommentCount(selector, item)
        return item

    # 获取渠道
    def getChannel(self, selector, item):
        item['channel'] = "华为手机助手"
        # LogUtil.HuaweiAPPlog("channel(%s)" % item['channel'])
        return

    # 获取爬取时间
    def getCrawlTime(self, selector, item):
        item['crawl_time'] = long(time.time())
        LogUtil.HuaweiAPPlog("crawl_time(%d)" % item['crawl_time'])
        return

    # 获取爬取url
    def getCrawlURL(self, selector, item, response):
        item['crawl_url'] = str(response.url).encode('utf-8')
        LogUtil.HuaweiAPPlog("crawl_url(%s)" % item['crawl_url'])
        return

    # 获取软件名
    def getName(self, selector, item):
        xpath = '//div[@class="app-info flt"]/ul/li/p/span[@class="title"]/text()'
        eles = selector.xpath(xpath).extract()
        name = "NULL"
        if (0 != len(eles)):
            name = eles[0]

        item['name'] = StrUtil.delWhiteSpace(name)
        if item['name'] != "NULL":
            LogUtil.HuaweiAPPlog("name(%s)" % item['name'])
        return

    # 获取软件大小
    def getSize(self, selector, item):
        xpath = '//div[@class="app-info flt"]/ul[2]/li[1]/span/text()'

        eles = selector.xpath(xpath).extract()
        item['size'] = "NULL"
        if eles:
            item['size'] = eles[0]
        LogUtil.HuaweiAPPlog("size(%s)" % item['size'])
        return

    # 获取软件版本更新时间
    def getUpdateTime(self, selector, item):
        xpath = '//div[@class="app-info flt"]/ul[2]/li[2]/span/text()'
        eles = selector.xpath(xpath).extract()
        
        item['update_time'] = "NULL"
        if eles:
            item['update_time'] = eles[0]
        LogUtil.HuaweiAPPlog("update_time(%s)" % item['update_time'])
        return


    # 获取版本信息
    def getVersion(self, selector, item):
        xpath = '//div[@class="app-info flt"]/ul[2]/li[4]/span/text()'
        eles = selector.xpath(xpath).extract()
        item['version'] = "NULL"

        if eles:
            item['version'] = eles[0]
        LogUtil.HuaweiAPPlog("version(%s)" % item['version'])
        return

    # 获取作者信息
    def getAuthor(self, selector, item):
        xpath = '//div[@class="app-info flt"]/ul[2]/li[3]/span/@title'
        eles = selector.xpath(xpath).extract()

        item['author'] = "NULL"
        if eles:
            item['author'] = eles[0]
        LogUtil.HuaweiAPPlog("author(%s)" % item['author'])
        return

    # 获取下载人数
    def getDownload(self, selector, item):
        xpath = '//div[@class="app-info flt"]/ul[1]/li[2]/p[1]/span[2]/text()'
        eles = selector.xpath(xpath).extract()

        item['download'] = "NULL"
        if eles:
            item['download'] = re.sub('\D','',eles[0])
        LogUtil.HuaweiAPPlog("download(%s)" % item['download'])
        return

    # 获取评论人数
    def getCommentCount(self, selector, item):
        xpath = '//form[@id="commentForm"]/h4/span/text()'
        eles = selector.xpath(xpath).extract()
        
        item['comment_count'] = "0"
        try:
            item['comment_count'] = re.sub('\D','',eles[0].split('（')[1])
        except:
            item['comment_count'] = "0"
        LogUtil.HuaweiAPPlog("comment_count(%s)" % item['comment_count'])
        return


      # 获取评分
    def getScore(self, selector, item):
        xpath = '//div[@class="app-info flt"]/ul[1]/li[2]/p[2]/span/@class'
        eles = selector.xpath(xpath).extract()
        item['score'] = "NULL"

        if eles:
            score = re.sub('\D','',eles[0])
            if int(score) % 2 == 0:
                item['score'] = str(int(score) / 2)
            else:
                item['score'] = str(int(score) / 2) + '.5'
        LogUtil.HuaweiAPPlog("score(%s)" % item['score'])
        return
