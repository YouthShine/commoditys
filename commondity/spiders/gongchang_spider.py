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


class GongchangSpider(scrapy.Spider):
	name = "gongchang"
	names = "spider_"+name + "_redis"
	allowed_domains = ["gongchang.com"]
	start_urls = [
		"http://www.gongchang.com/"
	]
	def __init__(self):
	   
		log.init_log(settings.get('LOG_DIR'))#
		logging.info("spider start......")
		print "spider start......"
		logging.info("fafafa")
	def parse(self, response):
		sel = Selector(response)
		for link in sel.xpath("//div[@class='cm-row']/ul[@class='cm-list clf']/li/a/@href").extract():
			logging.info("-------linkzu="+link)
			request = scrapy.Request(link, callback=self.parse_item2)
			yield request

	def parse_item2(self, response):
		#filename = response.url.split("/")[-2]
		#open(filename, 'wb').write(response.body)
		for link_one in response.xpath("//div[@class='cm-row']/ul[@class='cm-list clf']/li/a/@href").extract():
			logging.info("-------link2_one="+link_one)
			request_one = scrapy.Request(link_one, callback=self.parse_item3)
			yield request_one
		for link_two in response.xpath("//div[@class='phw-l-con']/dl/dt/a/@href").extract():
			logging.info("-------link2_two="+link_two)
			request_two = scrapy.Request(link_two, callback=self.parse_item3)
			yield request_two
		for link_three in response.xpath("//div[@class='mod-feature']/div[@class='mf-row js-extend'][1]/div[@class='mf-dd']/ul[@class='mf-list js-box clf']/li[@class='mf-itm']/a/@href").extract():
			link_three = "http://product.gongchang.com/c327/?gct=1.1.3-1-1-1-1.143"+link_three
			logging.info("-------link2_three="+link_three)
			request_tree = scrapy.Request(link_three, callback=self.parse_item3)
			yield request_tree

	#第三个页面
	def parse_item3(self, response):
		#global name 
		#filename = response.url.split("/")[-2]
		#open(filename, 'wb').write(response.body)
		for link in response.xpath("//li[@class='gg-itm']/div[@class='gg-con']/p[@class='gg-tit']/a/@href").extract():
			logging.info("----link3="+link)
			redis=RedisConnect()
			redis.setSadd(self.names,link)

				#获取页码集合
		pages = response.xpath("//a[@class='mp-num']/@href").extract()
		pages_next = ''
		try: 
			pages_next = response.xpath("//a[@class='mp-num']/text()").extract()[-1].encode('utf-8')
		except:
			pass
		if len(pages) > 2 and pages_next=='下一页':
			page_link = pages[-1]
			detail_link = 'http://product.gongchang.com/c1126/?gct=2.120.7-3-1-1-1-1.1%s' % page_link
			logging.info("-------page_link="+detail_link)
			request = scrapy.Request(detail_link, callback=self.parse_item3)
			yield request