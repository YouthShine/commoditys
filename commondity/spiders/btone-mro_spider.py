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
	name = "btone-mro"
	names = "spider_"+name + "_redis"
	allowed_domains = ["btone-mro.com"]
	start_urls = [
		"http://www.btone-mro.com/"
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
		for link in sel.xpath("//dl[@class='iProDiv']/dd/a/@href").extract():
			#请求=Request(连接，parese_item)
			logging.info("-------linkzu="+link)
			request = scrapy.Request("http://www.btone-mro.com"+link, callback=self.parse_item2)
			yield request#返回请求

	#第二个页面
	def parse_item2(self, response):
		#filename = response.url.split("/")[-2]
		#open(filename, 'wb').write(response.body)
		for link in response.xpath("//div[@class='subPage']/div[@class='subType']/div/a/@href").extract():
			logging.info("-------link2="+link)
			request = scrapy.Request("http://www.btone-mro.com"+link, callback=self.parse_item3)
			yield request

	#第三个页面
	def parse_item3(self, response):
		#filename = response.url.split("/")[-2]
		#open(filename, 'wb').write(response.body)
		for link in response.xpath("//table[@id='pro-list']/tbody/tr/td[3]/a/@href").extract():
			link = "http://www.btone-mro.com"+link
			logging.info("-------link3="+link)
			redis=RedisConnect()
			redis.setSadd(self.names,link)

		#获取页码集合
		pages = response.xpath("//div[@id='ctl00_ContentPlaceHolder1_pager1']/div[2]/a/@href").extract()
		pages_next = ''
		try: 
			pages_next = response.xpath("//div[@id='main']/div[@id='content']/div[@id='second']/div/div[1]/div[@id='AspNetPager1']/a[@class='down']/text()").extract()[0]
		except:
			pass
		#print('pages: %s' % pages)#打印页码
		if len(pages) >= 2:#如果页码集合>2
			page_link = pages[-2]#图片连接=读取页码集合的倒数第二个页码
			#page_link = page_link.replace('/a/', '')#图片连接=page_link（a替换成空）
			detail_link = 'http://www.btone-mro.com%s' % page_link
			#print detail_link+"---"
			logging.info("-------page_links="+detail_link)
			request = scrapy.Request(detail_link, callback=self.parse_item3)
			yield request
