# -*- coding: utf-8 -*-


BOT_NAME = 'HuaweiApp'

SPIDER_MODULES = ['HuaweiApp.spiders']
NEWSPIDER_MODULE = 'HuaweiApp.spiders'

# 禁止重定向
REDIRECT_MAX_TIMES = 0

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
    # 'HuaweiApp.middlewares.RotateUserAgentMiddleware' :400,
    # 'HuaweiApp.middlewares.ProxyMiddleware': 410
}

DOWNLOAD_DELAY = 0.05
DOWNLOAD_TIMEOUT = 300

LOG_LEVEL = 'INFO'

ITEM_PIPELINES = {
   'HuaweiApp.pipelines.HuaweiAppPipeline': 300,
}


