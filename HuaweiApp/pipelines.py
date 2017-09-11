# -*- coding: utf-8 -*-
__author__ = 'liuyang'

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from twisted.enterprise import adbapi
import MySQLdb.cursors
from items import HuaweiAppItem,HuaweiAppCommentItem

class HuaweiAppPipeline(object):
    #TODO 初始化Mysql
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
            host = 'localhost',
            db = 'huaweiapp',
            user = 'root',
            passwd = '1234',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = False
        )

    def process_item(self, item, spider):
        # print type(item)
        if isinstance(item, HuaweiAppItem):
            self.SaveHuaweiAppInfo(item,spider)
        elif isinstance(item,HuaweiAppCommentItem):
            self.SaveHuaweiAppComment(item)

    # TODO 保存app评论信息
    def SaveHuaweiAppComment(self, item):
        item.setdefault('channel', '')
        item.setdefault('name', '')
        item.setdefault('commenttime', '')
        item.setdefault('commentscore', '')
        item.setdefault('phone', '')
        item.setdefault('username', '')
        item.setdefault('comment', '')
        query = self.dbpool.runInteraction(self.insertcomment, item)
        return item

    def insertcomment(self, tx, item):
        print item
        try:
            tx.execute(
                "insert into huaweiappcomment(channel,name,commenttime,commentscore,phone,username,comment) " \
                 "values(%s,%s,%s,%s,%s,%s,%s)", \
                (item['channel'], item['name'], item['commenttime'], item['commentscore'], item['phone'], item['username'], \
                    item['comment']))
        except:
            pass

    # TODO 保存app基本信息
    def SaveHuaweiAppInfo(self, item, spider):
        print "ss"
        item.setdefault('channel','')
        item.setdefault('name','')
        item.setdefault('size','')
        item.setdefault('crawl_url','')
        item.setdefault('version','')
        item.setdefault('update_time','')
        item.setdefault('author','')
        item.setdefault('download','')
        item.setdefault('score','')
        item.setdefault('comment_count','')
        query = self.dbpool.runInteraction(self.insertappinfo, item)
        return item

    def insertappinfo(self, tx, item):
        tx.execute("insert into huaweiappinfo(channel,name,size,crawl_url,version,update_time,author,download,score,comment_count) "\
                   "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",\
                   (item['channel'],item['name'],item['size'],item['crawl_url'],item['version'],item['update_time'],\
                    item['author'],item['download'],item['score'],item['comment_count']))


