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

class YilongSpider(scrapy.Spider):
	name = "hc360"
	names = "spider_"+name + "_redis"
	allowed_domains = ["hc360.com"]
	start_urls = [
		"http://www.hc360.com/"
	]
<<<<<<< HEAD
<<<<<<< HEAD
	#¹¹Ôìº¯Êı
=======
	#æ„é€ å‡½æ•°
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
	#æ„é€ å‡½æ•°
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
	def __init__(self):
	   
		log.init_log(settings.get('LOG_DIR'))#
		logging.info("spider start......")
		print "spider start......"
		logging.info("fafafa")
<<<<<<< HEAD
<<<<<<< HEAD
	#Ö÷Ò³Ãæ 
	def parse(self, response):
		#Ã¿¸öÁ¬½Ó£¬ÓÃ@hrefÊôĞÔ
		#print '-------------777777',HtmlResponses.xpath("//div[@class='headCategory']/div[@class='headCat']/div[@class='categoryList']//dl[@class='categoryList__category']/dd/div/div/div[@class='grandchildList']/ul[@class='grandchildList__category']/li/a/@href").extract()
		for link in response.xpath("//div[@id='category']/div/div/div/dl/dd/a/@href").extract():
			#ÇëÇó=Request(Á¬½Ó£¬parese_item)
			logging.info("-------linkzu="+link)
			request = scrapy.Request(link, callback=self.parse_item2)
			yield request#·µ»ØÇëÇó

	#µÚ¶ş¸öÒ³Ãæ
=======
=======
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
	#ä¸»é¡µé¢ 
	def parse(self, response):
		#æ¯ä¸ªè¿æ¥ï¼Œç”¨@hrefå±æ€§
		#print '-------------777777',HtmlResponses.xpath("//div[@class='headCategory']/div[@class='headCat']/div[@class='categoryList']//dl[@class='categoryList__category']/dd/div/div/div[@class='grandchildList']/ul[@class='grandchildList__category']/li/a/@href").extract()
		for link in response.xpath("//div[@id='category']/div/div/div/dl/dd/a/@href").extract():
			#è¯·æ±‚=Request(è¿æ¥ï¼Œparese_item)
			logging.info("-------linkzu="+link)
			request = scrapy.Request(link, callback=self.parse_item2)
			yield request#è¿”å›è¯·æ±‚

	#ç¬¬äºŒä¸ªé¡µé¢
<<<<<<< HEAD
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
	def parse_item2(self, response):
		#filename = response.url.split("/")[-2]
		#open(filename, 'wb').wri 
		for link in response.xpath("//div[@class='wrap-grid']/ul/li[@class='grid-list']/div/div[@class='seaNewList']/dl/dd[@class='newName']/a/@href").extract():
			logging.info("-------link2="+link)
			redis=RedisConnect()
<<<<<<< HEAD
<<<<<<< HEAD
			redis.lPush(self.names,link)

		#»ñÈ¡Ò³Âë¼¯ºÏ
=======
			redis.setSadd(self.names,link)

		#è·å–é¡µç é›†åˆ
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
			redis.setSadd(self.names,link)

		#è·å–é¡µç é›†åˆ
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
		pages = response.xpath("//div[@class='s-mod-page']/a/@href").extract()
		pages_next = ''
		pages_nexts = ''
		try: 
			pages_next = response.xpath("//div[@class='s-mod-page']/span[@class='page_next page-n']/a/text()").extract()[0]
			pages_nexts = response.xpath("//div[@class='s-mod-page']/span[@class='page_next page-n']/a/@href").extract()[0]
		except:
			pass
<<<<<<< HEAD
<<<<<<< HEAD
		#print('pages: %s' % pages)#´òÓ¡Ò³Âë
		if len(pages) >= 2 and pages_next!='':#Èç¹ûÒ³Âë¼¯ºÏ>2
			page_link = pages_nexts #Í¼Æ¬Á¬½Ó=¶ÁÈ¡Ò³Âë¼¯ºÏµÄµ¹ÊıµÚ¶ş¸öÒ³Âë
			#page_link = page_link.replace('/a/', '')#Í¼Æ¬Á¬½Ó=page_link£¨aÌæ»»³É¿Õ£©
=======
=======
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
		#print('pages: %s' % pages)#æ‰“å°é¡µç 
		if len(pages) >= 2 and pages_next!='':#å¦‚æœé¡µç é›†åˆ>2
			page_link = pages_nexts #å›¾ç‰‡è¿æ¥=è¯»å–é¡µç é›†åˆçš„å€’æ•°ç¬¬äºŒä¸ªé¡µç 
			#page_link = page_link.replace('/a/', '')#å›¾ç‰‡è¿æ¥=page_linkï¼ˆaæ›¿æ¢æˆç©ºï¼‰
<<<<<<< HEAD
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
			detail_link = '%s' % page_link
			#print detail_link+"---"
			logging.info("-------page_links="+detail_link)
			request = scrapy.Request(detail_link, callback=self.parse_item2)
			yield request

	
   