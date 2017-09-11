HuaweiAPP应用爬取
=================================

AHU
--------------------------

##使用框架：Scrapy

##数据库：

###数据库名:huaweiapp
1.huaweiappinfo<br />
```sql
DROP TABLE IF EXISTS `huaweiappinfo`;
CREATE TABLE `huaweiappinfo` (
  `channel` varchar(40) DEFAULT NULL,
  `name` varchar(60) NOT NULL,
  `size` varchar(30) DEFAULT NULL,
  `crawl_url` varchar(80) DEFAULT NULL,
  `version` varchar(20) DEFAULT NULL,
  `update_time` varchar(30) DEFAULT NULL,
  `author` varchar(100) DEFAULT NULL,
  `download` varchar(30) DEFAULT NULL,
  `score` varchar(10) DEFAULT NULL,
  `comment_count` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

```
2.huaweiappcomment<br />
```sql
DROP TABLE IF EXISTS `huaweiappcomment`;
CREATE TABLE `huaweiappcomment` (
  `channel` varchar(40) DEFAULT NULL,
  `name` varchar(60) NOT NULL,
  `commenttime` varchar(40) DEFAULT NULL,
  `commentscore` varchar(15) DEFAULT NULL,
  `phone` varchar(40) DEFAULT NULL,
  `username` varchar(40) DEFAULT NULL,
  `comment` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```