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

class ShopSpider(scrapy.Spider):
	name = "8shop"
	names = "spider_"+name + "_redis"
	allowed_domains = ["8shop.cc"]
	start_urls = [
		"http://www.8shop.cc"
	]
	def __init__(self):
	   
		log.init_log(settings.get('LOG_DIR'))#
		logging.info("spider start......")
		print "spider start......"
		logging.info("fafafa")
	#Main pages
	def parse(self, response):
		sel = Selector(response)
		for link in sel.xpath('//li[@class="normal"]/a/@href').extract():
			logging.info("-----linkzu="+link)
			request = scrapy.Request(link, callback=self.parse_item2)
			yield request

	#Second pages
	def parse_item2(self, response):
		for link in response.xpath('//div[@class="squares"]/ul/li/h3/span[1]/span[1]/a/@href').extract():
			logging.info("----link2="+link)
			redis=RedisConnect()
			redis.setSadd(self.names,link)

		pages = response.xpath('//div[@class="shop_list_page"]/div[1]/a/@href').extract()
		pages_next = ''
		try: 
			pages_next = response.xpath("//div[@class='shop_list_page']/div[1]/a[@class='down']/text()").extract()[0]
		except:
			pass
		if len(pages) >= 2 and pages_next!='':
			page_link = pages[-1]
			detail_link = '%s' % page_link
			#print detail_link+"---"
			logging.info("-----page_links="+detail_link)
			request = scrapy.Request(detail_link, callback=self.parse_item2)
			yield request

