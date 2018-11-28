# -*- coding: utf-8 -*-

import os

# Scrapy settings for Artical project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Artical'

SPIDER_MODULES = ['Artical.spiders']
NEWSPIDER_MODULE = 'Artical.spiders'

# LOG_ENABLE = True
# #保存爬虫日志的文件名
# LOG_FILE = 'position.log'
# #scrapy有五个等级，等于和高于此等级（INFO）的信息会被保存
# LOG_LEVEL = 'ERROR'

#等级如下：（高到底）
#CRITICAL：严重错误
#ERROR：一般错误
#WARNING：警告信息
#INFO：一般信息
#DEBUG：调试信息

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Artical (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#默认随机值为 0.5-1.5s
DOWNLOAD_DELAY = 3

#下载延迟，默认180s
# DOWNLOAD_TIMEOUT = 60

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   # 'Accept-Language': 'en',
#    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
# }

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
RANDOM_UA_TYPE = 'random'


# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'Artical.middlewares.ArticalSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'Artical.middlewares.ArticalDownloaderMiddleware': 543,
   'Artical.middlewares.RandomUserAgentMiddleWare': 655,
   # 'Artical.middlewares.RandomProxyMiddleWare': 5,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'scrapy.pipelines.images.ImagesPipeline':1,
   'Artical.pipelines.ImgPipeline': 1,

   # 'Artical.pipelines.ArticalPipeline': 2,
   'Artical.pipelines.ArticalJsonPipeline': 2,

   # 'Artical.pipelines.MysqlPipeline': 3,
   # 'Artical.pipelines.MysqlTwistedPipline': 3,

}

IMAGES_URLS_FIELD = 'front_img_url'
project_dir = os.path.dirname(os.path.abspath(__file__))
IMAGES_STORE = os.path.join(project_dir,'images')


# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


#Mysql配置
MYSQL_HOST = "127.0.0.1"
MYSQL_DBNAME = "artical_spider"
MYSQL_USER = "root"
MYSQL_PASSWORD = "0"


SQL_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
SQL_DATE_FORMAT = "%Y-%m-%d"


# CLOSESPIDER_PAGECOUNT = 50
