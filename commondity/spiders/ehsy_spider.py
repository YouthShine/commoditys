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
	name = "ehsy"
	names = "spider_"+name + "_redis"
	allowed_domains = ["ehsy.com"]
	start_urls = [
		"http://www.ehsy.com"
	]
	#构造函数
	def __init__(self):
	   
		log.init_log(settings.get('LOG_DIR'))#
		logging.info("spider start......")
		print "spider start......"
		logging.info("fafafa")
	#主页面 
	def parse(self, response):
		print "PhantomJS is starting1..."
		#driver = webdriver.PhantomJS()
		driver = webdriver.PhantomJS()
		driver.get(response.url)
		time.sleep(3)
		body = driver.page_source
		#driver.close()
		HtmlResponses = HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=response)
		for link in HtmlResponses.xpath("//a[@class='aHref-level3 ng-binding']/@href").extract():
			link = "http://www.ehsy.com"+link
			logging.info("-------linkzu="+link)
			request = scrapy.Request(link, callback=self.parse_item2)
			yield request#返回请求

	#第二个页面
	def parse_item2(self, response):
		for link in response.xpath("//div[@class='product']/div[@class='productName']/a/@href").extract():
			link = "http://www.ehsy.com"+link
			logging.info("-------link2="+link)
			redis=RedisConnect()
			redis.setSadd(self.names,link)

		#获取页码集合
		pages = response.xpath("//div[@id='product-list']/div[@class='showPagintion']/div[@class='pagintion']/li/a/@href").extract()
		pages_next = ''
		try: 
			pages_next = response.xpath("//div[@id='product-list']/div[@class='showPagintion']/div[@class='pagintion']/li[@class='pg-next']/a/text()").extract()[0]
		except:
			pass
		if len(pages) >= 2 and pages_next!='':
			page_link = pages[-1]
			#page_link = page_link.replace('/a/', '')
			detail_link = 'http://www.ehsy.com%s' % page_link
			#print detail_link+"---"
			logging.info("-------page_links="+detail_link)
			request = scrapy.Request(detail_link, callback=self.parse_item2)
			yield request