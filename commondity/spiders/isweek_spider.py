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
from commondity.lib.service.redisconnect import *
from commondity.lib.service.geturls import *


class IsweekSpider(scrapy.Spider):
	name = "isweek"
	names = "spider_"+name + "_redis"
	allowed_domains = ["isweek.cn"]
	start_urls = [
		"http://www.isweek.cn"
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
		for link in sel.xpath('//nav[@id="nav"]/div/ul/li[1]/a/@href').extract():
			#请求=Request(连接，parese_item)
			logging.info("-------linkzu="+link)
			request = scrapy.Request("http://www.isweek.cn"+link, callback=self.parse_item2)
			yield request#返回请求

	#第二个页面
	def parse_item2(self, response):
		#filename = response.url.split("/")[-2]
		#open(filename, 'wb').write(response.body)
		for link in response.xpath('//div[@class="w-fly-mr"]/div/section/h2/a/@href').extract():
			logging.info("----link2="+link)
			request = scrapy.Request("http://www.isweek.cn"+link, callback=self.parse_item3)
			yield request

	#第三个页面
	def parse_item3(self, response):
		#global name 
		#filename = response.url.split("/")[-2]
		#open(filename, 'wb').write(response.body)
		
		for link in response.xpath('//ul[@class="proshow-bd prolist clearfix"]/li/div/a/@href').extract():
			logging.info("----link3="+link)
			redis=RedisConnect()
			redis.setSadd(self.names,"http://www.isweek.cn"+link)

				#获取页码集合
		pages = response.xpath('//div[@class="proshow-ft clearfix"]/div/div/a/@href').extract()
		pages_next = ''
		try: 
			pages_next = response.xpath("//div[@class='proshow-ft clearfix']/div/div/a[@class='next']/text()").extract()[0]
		except:
			pass
		#print('pages: %s' % pages)#打印页码
		if len(pages) > 2 and pages_next!='':#如果页码集合>2
			page_link = pages[-1]#图片连接=读取页码集合的倒数第二个页码
			#page_link = page_link.replace('/a/', '')#图片连接=page_link（a替换成空）
			detail_link = 'http://www.isweek.cn%s' % page_link
			#print detail_link+"---"
			logging.info("-------page_link="+detail_link)
			request = scrapy.Request(detail_link, callback=self.parse_item3)
			yield request