# -*- coding: utf-8 -*-
import scrapy
import math
import os
import time
from commondity.items.base_item import BaseItem
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from commondity.lib.service import log
import logging
from scrapy.conf import settings
from scrapy.http import Request
from selenium import webdriver
from commondity.lib.service.redisconnect import *

class GoxSpider(scrapy.Spider):
	name = "grainger"
	names = "spider_"+name + "_redis"
	allowed_domains = ["grainger.cn"]
	start_urls = [
		"http://www.grainger.cn/"
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
		#start browser
		#self.driver.get(response.url)
		#loading time interval
		#time.sleep(5)
		#self.driver.quit()
		#每个连接，用@href属性
		for link in sel.xpath("//div[@class='nav-bg']/div[@class='nav']/div[@id='category']/h2/a/@href").extract():
			#请求=Request(连接，parese_item)
			logging.info("-------linkzu="+link)
			request = scrapy.Request(link, callback=self.parse_item2)
			yield request#返回请求

	#第二个页面
	def parse_item2(self, response):
		#filename = response.url.split("/")[-2]
		#open(filename, 'wb').write(response.body)
		#print '7777777777'
		#start browser
		#self.driver.get(response.url)
		#loading time interval
		#time.sleep(5)
		for link in response.xpath("//div[@class='sitemap']/div/dl/dd/a[1]/@href").extract():
			logging.info("-------link2="+link)
			request = scrapy.Request("http://item.grainger.cn"+link, callback=self.parse_item3)
			yield request

	#第三个页面
	def parse_item3(self, response):
		#filename = response.url.split("/")[-2]
		#open(filename, 'wb').write(response.body)
		#print '7777777777'
		#start browser
		#self.driver.get(response.url)
		#loading time interval
		#time.sleep(5)
		for link in response.xpath("//div[@class='product_grid_box item']/h3[@class='txt']/a/@href").extract():
			logging.info("-------link3="+link)
			redis=RedisConnect()
			redis.setSadd(self.names,"http://item.grainger.cn"+link)

		#获取页码集合
		pages = response.xpath("//div[@class='page_curl page_curl_box']/p[@class='page_curl_number']/a/@href").extract()
		pages_next = ''
		try: 
			pages_next = response.xpath("//div[@class='page_curl page_curl_box']/p[@class='page_curl_number']/a[@class='page_curl_btn']/text()").extract()[0]
		except:
			pass
		#print('pages: %s' % pages)#打印页码
		if len(pages) > 2 and pages_next!='' :#如果页码集合>2
			page_link = pages[-1]#图片连接=读取页码集合的倒数第二个页码
			#page_link = page_link.replace('/a/', '')#图片连接=page_link（a替换成空）
			detail_link = 'http://item.grainger.cn%s' % page_link
			#print detail_link+"---"
			logging.info("-------page_links="+detail_link)
			request = scrapy.Request(detail_link, callback=self.parse_item3)
			yield request