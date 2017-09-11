# -*- coding: utf-8 -*-
__author__ = 'liuyang'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import scrapy
from scrapy.http import Request
from ..items import HuaweiAppCommentItem
from ..utils import LogUtil
from ..utils import ReadLing
class HuaWeiCommentSpider(scrapy.Spider):
    # 爬虫名字
    name = "huaweiAppComment"
    # 限制范围
    allowed_domains = ["app.hicloud.com"]
    def __init__(self):

        # 统计处理url总数
        self.urls_sum = 0L

        return

    def start_requests(self):
        Appinfo = ReadLing().get_records('huaweiappinfo')
        # 遍历每个app爬取评论
        for appinfo in Appinfo:
            # 每爬取100个app，输出一次标记
            self.urls_sum += 1
            if self.urls_sum % 100 == 0:
                LogUtil.HuaweiAPPlog("urls_sum(%d)" % self.urls_sum)


            if appinfo[9] not in ['0','','NULL']:
                    # 从url中匹配app编号
                    appbianhao = re.sub('\D', '', appinfo[3])
                    IndexUrl = "http://appstore.huawei.com/comment/commentAction.action?appId=C"
                    try:
                        if int(appinfo[9]) > 15:
                            url = IndexUrl + appbianhao + "&appName=" + \
                                  appinfo[1] + "&_page=1"
                            yield Request(url=url, meta={"name": appinfo[1]},
                                          callback=self.HuaweiAppCommenfparse)
                            '''
            ###########################华为应用市场##############################
                              评论页在1000页之后均为重复数据，
                              若评论页超过1000页，只爬取前1000
                              页数据
                        '''
                            if int(appinfo[9])/5 < 1000:
                                for i in range(4,int(appinfo[9])/5+1,1):
                                    url = IndexUrl + appbianhao + "&appName=" + appinfo[1] + "&_page=" + str(i)
                                    yield Request(url=url, meta={"name": appinfo[1]},
                                              callback=self.HuaweiAppCommenfparse)
                            else:
                                for i in range(4,1000,1):
                                    url = IndexUrl + appbianhao + "&appName=" + appinfo[1] + "&_page=" + str(i)
                                    yield Request(url=url, meta={"name": appinfo[1]},
                                              callback=self.HuaweiAppCommenfparse)
                            '''
                            华为应用市场评论数据第一页评论15条，
                            之后每页5条，
                            若评论数少于15条，
                            只爬取第一页
                        '''
                        else:
                            url = IndexUrl + appbianhao + "&appName=" + \
                                  appinfo[1] + "&_page=1"
                            yield Request(url=url, meta={"name": appinfo[1]},
                                          callback=self.HuaweiAppCommenfparse)
                    except:
                        print "出现错误连接"


    def HuaweiAppCommenfparse(self,response):
        selector = scrapy.Selector(response)
        Commentinfo = selector.xpath('//div[@class="comment"]')
        for commentinfo in Commentinfo:
            # 新建信息容器
            item = HuaweiAppCommentItem()
            self.getChannel(item)
            item["name"] = response.meta["name"]
            self.getcommenttime(commentinfo, item)
            self.getcommentscore(commentinfo, item)
            self.getphone(commentinfo, item)
            self.getusername(commentinfo, item)
            self.getcomment(commentinfo, item)
            yield item

    # 获取渠道
    def getChannel(self, item):
        item['channel'] = "华为手机助手"
        return

    # 获取评论时间
    def getcommenttime(self, commentinfo, item):
        xpath = 'p[@class="sub"]/span[@class="frt"]/text()'
        eles = commentinfo.xpath(xpath).extract()

        if eles:
            item['commenttime'] = eles[0]
        else:
            item['commenttime'] = "NULL"
        return

    def getcommentscore(self, commentinfo, item):
        xpath = 'p[@class="sub"]/span[1]/@class'

        eles = commentinfo.xpath(xpath).extract()
        if eles:
            commentscore = re.sub('\D','',eles[0])
            if int(commentscore) % 2 == 0:
                item['commentscore'] = str(int(commentscore) / 2)
            else:
                item['commentscore'] = str(int(commentscore) / 2) + '.5'
        else:
            item['commentscore'] = "NULL"
        return

    def getphone(self, commentinfo, item):
        xpath = 'p[@class="sub"]/span[4]/text()'

        eles = commentinfo.xpath(xpath).extract()
        if eles:
            b = re.sub('来自','',eles[0])
            item['phone'] = re.sub('手机','',b)
        else:
            item['phone'] = "华为应用市场"
        return

    def getusername(self, commentinfo, item):
        xpath = 'p[@class="sub"]/span[2]/text()'
        eles = commentinfo.xpath(xpath).extract()

        if eles:
            item['username'] = eles[0]
        else:
            item['username'] = "NULL"
        return

    def getcomment(self,commentinfo, item):
        xpath = 'p[@class="content"]/text()'
        eles = commentinfo.xpath(xpath).extract()

        if eles:
            item['comment'] = eles[0].strip()
        else:
            item['comment'] = "NULL"
        return
