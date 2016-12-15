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

class AizSpider(scrapy.Spider):
	name = "gongboshi"
	names = "spider_"+name + "_redis"
	allowed_domains = ["gongboshi.com"]
	start_urls = [
		"http://www.gongboshi.com"
	]
	#构造函数
	def __init__(self):
	   
		log.init_log(settings.get('LOG_DIR'))#
		logging.info("spider start......")
		print "spider start......"
		logging.info("fafafa")
	#主页面 
	def parse(self, response):
		#print "PhantomJS is starting1..."
		#driver = webdriver.PhantomJS()
		#driver = webdriver.PhantomJS()
		#driver.get(response.url)
		#time.sleep(3)
		#body = driver.page_source
		#driver.close()
		#HtmlResponses = HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=response)
		for link in response.xpath("//div[@class='i-mc']/div[@class='subitem']/dl/dd/em/a/@href").extract():
			link = "http://www.gongboshi.com/"+link
			logging.info("-------linkzu="+link)
			request = scrapy.Request(link, callback=self.parse_item2)
			yield request#返回请求

	#第二个页面
	def parse_item2(self, response):
		for link in response.xpath("//tr/td[4]/ul/li[1]/a/@href").extract():
			logging.info("-------link2="+link)
			redis=RedisConnect()
			redis.setSadd(self.names,link)

		#获取页码集合
		pages = response.xpath("//div[@class='pages']/a/@href").extract()
		pages_next = ''
		try: 
			pages_next = response.xpath("//div[@class='pages']/a[4]/text()").extract()[0].encode('utf-8').replace("\t","").replace("\n","").replace("\b","").strip()
		except:
			pass
		page_link = ''
		if len(pages) >= 2 and pages_next!='':
			#page_link = page_link.replace('/a/', '')
			if page_link != pages[-1]:
				page_link = pages[-1]
				#print detail_link+"---"
				logging.info("-------page_links="+page_link)
				request = scrapy.Request(page_link, callback=self.parse_item2)
				yield request