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
	name = "spider_lbgoo_redis"
	url = GetUrls()
	start_urls = url.getUrls(name)
	def __init__(self):
	   
		log.init_log(settings.get('LOG_DIR'))
		logging.info("spider start......")
		print "spider start......"
		logging.info("fafafa")

	#Details page 

	def parse(self, response):
		item = BaseItem()
		item = BaseItem()
		item['productUrl'] = ''
		item['productName'] = ''
		item['productBrand'] = ''
		item['productModel'] = ''
		item['productClassification'] = ''
		item['productPrice'] = ''
		item['productImagePath'] = ''
		item['productAddres'] = ""
		item['productCompany'] = ''
		item['fileName'] = ''
		classification_one = ''
		classification_two = ''
		classification_three = ''
		try:
			classification_two = response.xpath("//dd[@class='crumb_item'][1]/a/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			classification_three = response.xpath("//div[@class='crumb']/dl/dd[@class='crumb_item'][2]/a/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			classification_one = response.xpath("//dd[@class='crumb_item'][13]/a/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		classification = classification_one + '|||' + classification_two + '|||' +classification_three
		try:
			item['productUrl'] = response.url
		except:
			pass
		try:
			item['productName'] = response.xpath("//form[@id='form1']/ul/li[@class='tit']/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		list_brand = ''
		for j in range(1,20):
			try:
				list_brand = response.xpath("//form[@id='form1']/ul/li[%i]/label/text()" %j).extract()[0].encode('utf-8').replace("\"","\'").strip()
				if '品    牌:' == list_brand:
					item['productBrand'] = response.xpath("//form[@id='form1']/ul/li[%i]/text()" %j).extract()[0].encode('utf-8').replace("\"","\'").strip()
					break
			except:
				pass
		try:
			item['productModel'] = response.xpath('//div[@class="m m1"]/div/ul/dt/li/text()').extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			item['productClassification'] = classification
		except:
			pass
		try:
		#去空格 转分   去人民币符号
			item['productPrice'] = response.xpath("//strong[@class='orange price_tit']/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			item['productPrice'] = str(float(filter(lambda ch: ch in '0123456789.~', item['productPrice']))*100)
		except:
			pass
		#图片连接
		try:
			item['productImagePath'] = response.xpath("//div[@class='bd']/div/div/p/span/img/@src").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		#print item['image_urls'],"777777"
		try:
			item['productAddres'] = response.xpath("//form[@id='form1']/ul/li[4]/text()").extract()[0]
		except:
			pass
		try:
			item['productCompany'] = ""
		except:
			pass
		names = self.name+'.json'
		try:
			item['fileName'] = names
		except:
			pass
		yield item	
