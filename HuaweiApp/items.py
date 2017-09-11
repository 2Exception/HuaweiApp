# -*- coding: utf-8 -*-
__author__ = 'liuyang'

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
'''
######## 华为app基本信息容器 ########
'''

class HuaweiAppItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    channel         = scrapy.Field()
    name 		    = scrapy.Field()
    size		    = scrapy.Field()
    crawl_url		= scrapy.Field()
    version			= scrapy.Field()
    update_time		= scrapy.Field()
    author          = scrapy.Field()
    download		= scrapy.Field()
    score           = scrapy.Field()
    comment_count 	= scrapy.Field()


'''
######## 华为app评论数据 ########
'''
class HuaweiAppCommentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    # 数据获取渠道
    channel         = scrapy.Field()
    # app名称
    name 		    = scrapy.Field()
    # 评论时间
    commenttime		= scrapy.Field()
    # 评论分数
    commentscore    = scrapy.Field()
    # 使用的手机userID
    phone           = scrapy.Field()
    # 评论者ID
    username        = scrapy.Field()
    # 评论内容
    comment 	= scrapy.Field()

'''
######## 国家组织招聘岗位数据########
'''

class JobDataItem(scrapy.Item):

    englishname = scrapy.Field() #组织英文缩写

    chinesename = scrapy.Field() #组织中文名称

    incontinent = scrapy.Field() #组织所属洲

    incountry = scrapy.Field()   #组织所在国家

    type = scrapy.Field()        #组织类别

    url = scrapy.Field()         #组织主页

    joburl = scrapy.Field()      #组织招聘岗位主页

    describe = scrapy.Field()    #岗位描述

    suoshu = scrapy.Field()      #所属机构

    work = scrapy.Field()        #岗位名称

    applytime = scrapy.Field()   #申请截止时间

    linkman = scrapy.Field()     #岗位联系人


