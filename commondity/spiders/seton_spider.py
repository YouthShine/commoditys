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

class SetonSpider(scrapy.Spider):
	name = "seton"
	names = "spider_"+name + "_redis"
	allowed_domains = ["seton.com.cn"]
	start_urls = [
		"http://www.seton.com.cn"
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
		for link in sel.xpath('//li/span/h3/a/@href').extract():
			#请求=Request(连接，parese_item)
			logging.info("linkzu="+link)
			request = scrapy.Request("http://www.seton.com.cn/"+link, callback=self.parse_item2)
			yield request#返回请求

	#第二个页面
	def parse_item2(self, response):
		for link in response.xpath("//a[@class='entry-title']/@href").extract():
			logging.info("link2="+link)
			redis=RedisConnect()
			redis.setSadd(self.names,"http://www.seton.com.cn/"+link)

					#获取页码集合
		pages = response.xpath("//table[@class='pager floatRight']/tr/td/a/@href").extract()
		pages_next = ''
		try: 
			pages_next = response.xpath("//table[@class='pager floatRight']/tr/td/a[@class='next']/text()").extract()[0]
		except:
			pass
		#print('pages: %s' % pages)#打印页码
		if len(pages) >= 2 and pages_next!='':#如果页码集合>2
			page_link = pages[-1]#图片连接=读取页码集合的倒数第二个页码
			#page_link = page_link.replace('/a/', '')#图片连接=page_link（a替换成空）
			detail_link = '%s' % page_link
			#print detail_link+"---"
			logging.info("detail_link==next_url="+detail_link)
			request = scrapy.Request(detail_link, callback=self.parse_item2)
			yield request#返回请求  yield Request('http://www.haocaimao.com%s' %page_link, callback=self.parse_image)

