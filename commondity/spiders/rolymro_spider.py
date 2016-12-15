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

class YilongSpider(scrapy.Spider):
	name = "rolymro"
	names = "spider_"+name + "_redis"
	allowed_domains = ["rolymro.com"]
	start_urls = [
		"http://www.rolymro.com/"
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
		for link in sel.xpath("//div[@class='center']/div[@class='pro14_2010']/ul/li/a/@href").extract():
			#请求=Request(连接，parese_item)
			logging.info("-------linkzu="+link)
			request = scrapy.Request("http://www.rolymro.com/"+link, callback=self.parse_item2)
			yield request#返回请求

	#第二个页面
	def parse_item2(self, response):
		#filename = response.url.split("/")[-2]
		#open(filename, 'wb').write(response.body)
		for link in response.xpath("//ul[@class='LowerLevels'][1]/li/a/@href").extract():
			logging.info("----link2="+link)
			request = scrapy.Request("http://www.rolymro.com/"+link, callback=self.parse_item3)
			yield request

	#第三个页面
	def parse_item3(self, response):
		print "PhantomJS is starting1..."
		driver = webdriver.PhantomJS()
		driver.get(response.url)
		#time.sleep(3)
		body = driver.page_source
		#driver.close()
		HtmlResponses = HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=response)
		#filename = response.url.split("/")[-2]
		#open(filename, 'wb').write(response.body)
		for link in HtmlResponses.xpath("//table/tbody/tr/td[2]/a/@href").extract():
			logging.info("----link3="+link)
			redis=RedisConnect()
			redis.setSadd(self.names,"http://www.rolymro.com/"+link)

				#获取页码集合
		pages = response.xpath("//div[@class='corpus_left']/p[5]/a/@href").extract()
		pages_next = ''
		try: 
			pages_next = response.xpath("//div[@class='corpus_left']/p[5]/a[@class='p_redirect']/text()").extract()[0]
		except:
			pass
		#print('pages: %s' % pages)#打印页码
		if len(pages) >= 2 and pages_next!= '':#如果页码集合>2
			page_link = pages[-1]#图片连接=读取页码集合的倒数第二个页码
			#page_link = page_link.replace('/a/', '')#图片连接=page_link（a替换成空）
			detail_link = '%s' % page_link
			#print detail_link+"---"
			logging.info("-------detail_link="+detail_link)
			request = scrapy.Request(detail_link, callback=self.parse_item3)
			yield request
	