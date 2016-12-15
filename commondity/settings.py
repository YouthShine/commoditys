# -*- coding: utf-8 -*-

# Scrapy settings for commondity project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
from selenium import webdriver
#which spider should use WEBKIT
#中间件
#WEBKIT_DOWNLOADER=['spider.name']
#DOWNLOADER_MIDDLEWARES = {
<<<<<<< HEAD
<<<<<<< HEAD
  #  'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
  # 'commondity.items.middleware.ProxyMiddleware': 100,
 #  }
=======
   #'commondity.items.middleware.JavaScriptMiddleware': 543,
  # 'commondity.items.downloadwebkit.WebkitDownloaderTest': None,
   #}
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
   #'commondity.items.middleware.JavaScriptMiddleware': 543,
  # 'commondity.items.downloadwebkit.WebkitDownloaderTest': None,
   #}
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394



import os
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
LOG_DIR = os.path.join(PROJECT_DIR, 'logs')

BOT_NAME = 'commondity'

SPIDER_MODULES = ['commondity.spiders']
NEWSPIDER_MODULE = 'commondity.spiders'
#载入ImageDownLoadPipeline类
ITEM_PIPELINES = {'commondity.pipelines.image.base_pipe.BasePipeline': 1}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'commondity (+http://www.yourdomain.com)'
<<<<<<< HEAD
<<<<<<< HEAD
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5' 
# Obey robots.txt rules
ROBOTSTXT_OBEY = False
=======

# Obey robots.txt rules
ROBOTSTXT_OBEY = True
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======

# Obey robots.txt rules
ROBOTSTXT_OBEY = True
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394

CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_ITEMS = 100
CONCURRENT_REQUESTS = 16
#os.environ["DISPLAY"] = ":0"
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
<<<<<<< HEAD
<<<<<<< HEAD
DOWNLOAD_DELAY = 3
=======
#DOWNLOAD_DELAY = 3
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
#DOWNLOAD_DELAY = 3
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
<<<<<<< HEAD
<<<<<<< HEAD
COOKIES_ENABLED = False
=======
#COOKIES_ENABLED = False
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
#COOKIES_ENABLED = False
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#DOWNLOADER_MIDDLEWARES = {
    #'commondity.items.middleware.JavaScriptMiddleware': 543,
    
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
<<<<<<< HEAD
<<<<<<< HEAD
   # 'commondity.middlewares.MyCustomDownloaderMiddleware': 543,
#}
#DOWNLOADER_MIDDLEWARES = {
#	'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,  
#	'commondity.rotate_useragent.RotateUserAgentMiddleware' :400  
=======
=======
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
#    'commondity.middlewares.MyCustomDownloaderMiddleware': 543,
#}
#DOWNLOADER_MIDDLEWARES = {
 	#'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,  
	#'commondity.rotate_useragent.RotateUserAgentMiddleware' :400  
<<<<<<< HEAD
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
#}



# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'commondity.pipelines.SomePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
