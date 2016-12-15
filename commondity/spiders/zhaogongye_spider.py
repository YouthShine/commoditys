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

class EhsySpider(scrapy.Spider):
	name = "zhaogongye"
	names = "spider_"+name + "_redis"
	allowed_domains = ["zhaogongye.cn"]
	start_urls = [
		"http://www.zhaogongye.cn"
	]
	#构造函数
	def __init__(self):
	   
		log.init_log(settings.get('LOG_DIR'))#
		logging.info("spider start......")
		print "spider start......"
		logging.info("fafafa")
	#主页面 
	def parse(self, response):
		for link in response.xpath("//div[@class='pop']/dl/dd/a/@href").extract():
			link = "http://www.zhaogongye.cn"+link
			logging.info("-------linkzu="+link)
			request = scrapy.Request(link, callback=self.parse_item2)
			yield request#返回请求

	#第二个页面
	def parse_item2(self, response):
		for link in response.xpath("//p[@class='f14 pt10 pheight']/a[@class='col59']/@href").extract():
			link = "http://www.zhaogongye.cn"+link
			logging.info("-------link2="+link)
			redis=RedisConnect()
			redis.setSadd(self.names,link)

		#获取页码集合
		pages = response.xpath("//a[@class='page2']/@href").extract()
		pages_next = ''
		try:
			pages_next = pages[-2].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		if len(pages) >= 2 and pages_next=='下一页':
			page_link = pages[-2]
			#page_link = page_link.replace('/a/', '')
			detail_link = 'http://www.zhaogongye.cn%s' % page_link
			#print detail_link+"---"
			logging.info("-------page_links="+detail_link)
			request = scrapy.Request(detail_link, callback=self.parse_item2)
			yield request