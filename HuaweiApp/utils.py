# -*- coding: utf-8 -*-
__author__ = 'liuyang'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import MySQLdb

#TODO 从数据库读取要爬取的连接
class ReadLing(object):
	def __init__(self):
		self.host = 'localhost'
		self.db = 'huaweiapp'
		self.user = 'root'
		self.password = '1234'


	#读取数据
	def get_records(self, table_name):
		db = MySQLdb.connect(self.host, self.user, self.password, self.db, charset='utf8')
		cursor = db.cursor()
		records = []
		try:
			cursor.execute("select * from %s" % table_name)
			records = cursor.fetchall()
		except Exception, e:
			print e
		db.commit()
		cursor.close()
		db.close()
		return records


#TODO 字符串工具
class StrUtil(object):
	def __init__(self):
		pass

	# 删除字符串中的空白符，连续空白符用空格代替
	@staticmethod
	def delWhiteSpace(msg):
		pattern = re.compile('\s+')
		return (re.sub(pattern, ' ', msg)).strip()

	# 判断字符串是否为空
	@staticmethod
	def isEmpty(msg):
		return msg and msg.strip()

	# 判断URL是否包含prefix并补全
	@staticmethod
	def completeURL(prefix, url):
		index = prefix.rfind('/')
		url = prefix[0:index + 1] + url
		return url

# 日志工具
class LogUtil(object):
	def __init__(self):
		pass

	@staticmethod
	def HuaweiAPPlog(msg):
		print "HuaweiAPP >> " + str(msg)
		return