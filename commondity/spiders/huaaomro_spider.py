# -*- coding: utf-8 -*-
import scrapy
import math
import time
import os
from commondity.items.base_item import BaseItem
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from commondity.lib.service import log
import logging
from scrapy.conf import settings
from scrapy.http import Request
from selenium import webdriver
from commondity.lib.service.redisconnect import *

class YilongSpider(scrapy.Spider):
	name = "huaaomro"
	names = "spider_"+name + "_redis"
	allowed_domains = ["huaaomro.com"]
	start_urls = [
		"http://www.huaaomro.com/"
	]
	#构造函数
	def __init__(self):
	   
		log.init_log(settings.get('LOG_DIR'))#
		logging.info("spider start......")
		print "spider start......"
		logging.info("fafafa")
		#配置环境变量 并获得驱动
		#chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
		#os.environ["webdriver.chrome.driver"] = chromedriver
		#self.driver = webdriver.Chrome(chromedriver)

	#主页面
	def parse(self, response):
		#sel是页面源代码，载入scrapy.selector
		sel = Selector(response)
		#每个连接，用@href属性
		for link in sel.xpath("//div[@class='sideNav']/ul[@id='nav']/li/h3/a/@href").extract():
			#请求=Request(连接，parese_item)
			logging.info("-------linkzu="+link)
			request = scrapy.Request("http://www.huaaomro.com/"+link, callback=self.parse_item2)
			yield request#返回请求

	#第二个页面
	def parse_item2(self, response):
		#filename = response.url.split("/")[-2]
		#open(filename, 'wb').write(response.body)
		for link in response.xpath("//div[@class='Prolist mb30']/ul[@class='clearfix']/li/div[@class='name']/a/@href").extract():
			logging.info("-------link2="+link)
			redis=RedisConnect()
			redis.setSadd(self.names,"http://www.huaaomro.com/"+link)

		#获取页码集合
		pages = response.xpath("//div[@class='paging clearfix txt_R']/a/@href").extract()
		pages_next = ''
		try: 
			pages_next = response.xpath("//div[@class='paging clearfix txt_R']/a[@class='pagebar_number']/text()").extract()[0]
		except:
			pass
		#print('pages: %s' % pages)#打印页码
		if len(pages) >= 2 :#如果页码集合>2
			page_link = pages[-2]#图片连接=读取页码集合的倒数第二个页码
			#page_link = page_link.replace('/a/', '')#图片连接=page_link（a替换成空）
			detail_link = 'http://www.huaaomro.com/%s' % page_link
			#print detail_link+"---"
			logging.info("-------page_links="+detail_link)
			request = scrapy.Request(detail_link, callback=self.parse_item2)
			yield request
