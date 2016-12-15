# -*- coding: utf-8 -*-
import scrapy
import math
from commondity.items.base_item import BaseItem  
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from commondity.lib.service import log
import logging
from scrapy.conf import settings
from scrapy.http import Request
from selenium import webdriver
import time
from scrapy.http import HtmlResponse
from commondity.lib.service.redisconnect import *
from commondity.lib.service.geturls import * 

class WwmroSpider(scrapy.Spider):
    name = "wwmro"
    names = "spider_"+name + "_redis"
    allowed_domains = ["wwmro.com"]
    start_urls = [
        "http://www.wwmro.com"
    ]
    #构造函数
    def __init__(self):
       
        log.init_log(settings.get('LOG_DIR'))#
        logging.info("spider start......")
        print "spider start......"
        logging.info("fafafa")
    #主页面
    def parse(self, response):
        #sel是页面源代码，载入scrapy.selector
        sel = Selector(response)
        #每个连接，用@href属性
        for link in sel.xpath('//div[@class="category pngFix"]/ul[@class="menu"]/li/h3/a/@href').extract():
            #请求=Request(连接，parese_item)
            logging.info("-------linkzu="+link)
            request = scrapy.Request("http://www.wwmro.com/"+link, callback=self.parse_item)
            yield request#返回请求

    #第二个页面
    def parse_item(self, response):
		for link in response.xpath('//ul[@class="list_pic"]/li[@class="item"]/dl/dt/a/@href').extract():
			logging.info("-------link2="+link)
			redis=RedisConnect()
			redis.setSadd(self.names,"http://www.wwmro.com/"+link)

		#获取页码集合
		pages = response.xpath('//div[@class="pagination"]/ul/li/a/@href').extract()
		#print('pages: %s' % pages)#打印页码
		if len(pages) >= 2:#如果页码集合>2
			page_link = pages[-2]#图片连接=读取页码集合的倒数第二个页码
			#page_link = page_link.replace('/a/', '')#图片连接=page_link（a替换成空）
			detail_link = 'http://www.wwmro.com%s' % page_link
			#print detail_link+"---"
			logging.info("-------pagee_link="+detail_link)
			request = scrapy.Request(detail_link, callback=self.parse_item)
			yield request#返回请求  yield Request('http://www.wwmro.com%s' %page_link, callback=self.parse_item
