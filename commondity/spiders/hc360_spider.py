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
	#���캯��
=======
	#构造函数
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
	#构造函数
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
	def __init__(self):
	   
		log.init_log(settings.get('LOG_DIR'))#
		logging.info("spider start......")
		print "spider start......"
		logging.info("fafafa")
<<<<<<< HEAD
<<<<<<< HEAD
	#��ҳ�� 
	def parse(self, response):
		#ÿ�����ӣ���@href����
		#print '-------------777777',HtmlResponses.xpath("//div[@class='headCategory']/div[@class='headCat']/div[@class='categoryList']//dl[@class='categoryList__category']/dd/div/div/div[@class='grandchildList']/ul[@class='grandchildList__category']/li/a/@href").extract()
		for link in response.xpath("//div[@id='category']/div/div/div/dl/dd/a/@href").extract():
			#����=Request(���ӣ�parese_item)
			logging.info("-------linkzu="+link)
			request = scrapy.Request(link, callback=self.parse_item2)
			yield request#��������

	#�ڶ���ҳ��
=======
=======
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
	#主页面 
	def parse(self, response):
		#每个连接，用@href属性
		#print '-------------777777',HtmlResponses.xpath("//div[@class='headCategory']/div[@class='headCat']/div[@class='categoryList']//dl[@class='categoryList__category']/dd/div/div/div[@class='grandchildList']/ul[@class='grandchildList__category']/li/a/@href").extract()
		for link in response.xpath("//div[@id='category']/div/div/div/dl/dd/a/@href").extract():
			#请求=Request(连接，parese_item)
			logging.info("-------linkzu="+link)
			request = scrapy.Request(link, callback=self.parse_item2)
			yield request#返回请求

	#第二个页面
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

		#��ȡҳ�뼯��
=======
			redis.setSadd(self.names,link)

		#获取页码集合
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
			redis.setSadd(self.names,link)

		#获取页码集合
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
		#print('pages: %s' % pages)#��ӡҳ��
		if len(pages) >= 2 and pages_next!='':#���ҳ�뼯��>2
			page_link = pages_nexts #ͼƬ����=��ȡҳ�뼯�ϵĵ����ڶ���ҳ��
			#page_link = page_link.replace('/a/', '')#ͼƬ����=page_link��a�滻�ɿգ�
=======
=======
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
		#print('pages: %s' % pages)#打印页码
		if len(pages) >= 2 and pages_next!='':#如果页码集合>2
			page_link = pages_nexts #图片连接=读取页码集合的倒数第二个页码
			#page_link = page_link.replace('/a/', '')#图片连接=page_link（a替换成空）
<<<<<<< HEAD
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
			detail_link = '%s' % page_link
			#print detail_link+"---"
			logging.info("-------page_links="+detail_link)
			request = scrapy.Request(detail_link, callback=self.parse_item2)
			yield request

	
   