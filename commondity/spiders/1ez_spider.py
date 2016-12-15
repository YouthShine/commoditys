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

class LezSpider(scrapy.Spider):
	name = "1ez"
	names = "spider_"+name + "_redis"
	allowed_domains = ["1ez.com.cn"]
	start_urls = [
		"http://www.1ez.com.cn/"
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
		for link in sel.xpath('//ul[@class="cat-slide-nav clearfix"]/li/div[1]/a/@href').extract():
			#请求=Request(连接，parese_item)
			logging.info("-------linkzu="+link)
			request = scrapy.Request("http://www.1ez.com.cn/"+link, callback=self.parse_item2)
			yield request#返回请求

	#第二个页面
	def parse_item2(self, response):
		#filename = response.url.split("/")[-2]
		#open(filename, 'wb').write(response.body)
		for link in response.xpath('//div[@id="category_tree_index"]/dl/dt/a/@href').extract():
			logging.info("-------link2="+link)
			request = scrapy.Request("http://www.1ez.com.cn/"+link, callback=self.parse_item3)
			yield request
	
	#第三个页面
	def parse_item3(self, response):
		#filename = response.url.split("/")[-2]
		#open(filename, 'wb').write(response.body)
		for link in response.xpath('//ul[@class="y_searchList clearfix"]/li/div/p[2]/a/@href').extract():
			logging.info("-------link3="+link)
			link = "http://www.1ez.com.cn/"+link
			redis=RedisConnect()
			redis.setSadd(self.names,link)

		#获取页码集合
		pages = response.xpath('//div[@class="activity_all"]/a/@href').extract()
		pages_next = ''
		try: 
			pages_next = response.xpath("//div[@class='activity_all']/a[@class='activity_next']/text()").extract()[0]
		except:
			pass
		#print('pages: %s' % pages)#打印页码
		if len(pages) >= 2 and pages_next!='':#如果页码集合>2
			page_link = pages[-1]#图片连接=读取页码集合的倒数第二个页码
			#page_link = page_link.replace('/a/', '')#图片连接=page_link（a替换成空）
			detail_link = 'http://www.1ez.com.cn/%s' % page_link
			#print detail_link+"---"
			logging.info("-------pages_link="+detail_link)
			request = scrapy.Request(detail_link, callback=self.parse_item3)
			yield request