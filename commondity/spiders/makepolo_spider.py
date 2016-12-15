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
	name = "makepolo"
	names = "spider_"+name + "_redis"
	allowed_domains = ["makepolo.com"]
	start_urls = [
		"http://china.makepolo.com/"
	]
	#Constructor
	def __init__(self):
	   
		log.init_log(settings.get('LOG_DIR'))#
		logging.info("spider start......")
		print "spider start......"
		logging.info("fafafa")

	#Main pages
	def parse(self, response):
		for j in range(1,15):
			link_text = ''
			try:
				if j==12:
					j=13
					link_text = response.xpath("//div[@class='industry clearfix']/dl[%i]/dt/span/a/text()" %j).extract()[0].encode('utf-8')
			except:
				pass
			link_text = response.xpath("//div[@class='industry clearfix']/dl[%i]/dt/span/a/text()" %j).extract()[0].encode('utf-8')
			print '0000000000',link_text
			if '建筑' in link_text:
				link = ''
				logging.info("-------linkzu="+link+'1111111111111') 
				continue
			if '商务服务' == link_text:
				link = ''
				logging.info("-------linkzu="+link+'22222222222') 
				continue
			if '生活消费' == link_text:
				link = ''
				logging.info("-------linkzu="+link+'3333333333333333') 
				continue
			if '企业贷款' in link_text:
				link = ''
				logging.info("-------linkzu="+link+'44444444444444') 
				continue
			if '酒店' == link_text:
				link = ''
				logging.info("-------linkzu="+link+'55555555555555555') 
				continue
			if '包装' in link_text:
				link = response.xpath("//div[@id='j_tips']/div[@class='industry clearfix']/dl[%i]/dt/span/a/@href" %j).extract()[0].encode('utf-8').replace("\"","\'").strip()
				logging.info("-------linkzu="+link+'777777777777777')
				request = scrapy.Request(link, callback=self.parse_item3)
				yield request
				continue
			if '泵' in link_text:
				link = response.xpath("//div[@id='j_tips']/div[@class='industry clearfix']/dl[%i]/dt/span/a/@href" %j).extract()[0].encode('utf-8').replace("\"","\'").strip()
				logging.info("-------linkzu="+link+'666666666666666666')
				request = scrapy.Request(link, callback=self.parse_item3)
				yield request
				continue
			link = ''
			try:
				link = response.xpath("//div[@class='industry clearfix']/dl[%i]/dt/span/a/@href" %j).extract()[0].encode('utf-8')
			except:
				pass
			logging.info("-------linkzu="+link+'8888888888888888')
			request = scrapy.Request(link, callback=self.parse_item2)
			yield request

	#Second pges
	def parse_item2(self, response):
		for link in response.xpath("//div[@class='category clearfix']/dl/dt/a/@href").extract():
			logging.info("-------link2="+link)
			request = scrapy.Request(link, callback=self.parse_item3)
			yield request

	#Third pages
	def parse_item3(self, response):
		for link in response.xpath("//div[@class='s_product_item']/div[@class='s_product_content ']/div[@class='s_product_title']/a[@class='plistk f14']/@href").extract():
			logging.info("-------link3="+link)
			redis=RedisConnect()
			redis.setSadd(self.names,link)
		pages = response.xpath("//div[@class='s_m clearfix']/div[@class='s_l']/div[@class='nextpage']/a/@href").extract()
		if len(pages) >= 2:
			page_link = pages[-1]
			detail_link = '%s' % page_link
			#print detail_link+"---"
			logging.info("-------page_links="+detail_link)
			request = scrapy.Request(detail_link, callback=self.parse_item3)
			yield request