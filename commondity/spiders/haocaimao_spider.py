# -*- coding: utf-8 -*-
import scrapy
import math
import logging
import time
import os
from scrapy.http import  Request
from commondity.items.base_item import BaseItem
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from commondity.lib.service import log
from scrapy.conf import settings
from selenium import webdriver
from commondity.lib.service.redisconnect import *

class HaocaimaoSpider(scrapy.Spider):
	name = "haocaimao"
	names = "spider_"+ name + "_redis"
	allowed_domains = ["haocaimao.com"]
	start_urls = [
		"http://www.haocaimao.com"
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

	#def __del__(self):
		#self.driver.close()

	#主页面
	def parse(self, response):
		#start browser
		#self.driver.get(response.url)
		#loading time interval
		#time.sleep(5)
		#sel是页面源代码，载入scrapy.selector
		sel = Selector(response)
		#每个连接，用@href属性
		for link in sel.xpath('//div[@class="mc_a"]/a[@class="a1"]/@href').extract():
			#请求=Request(连接，parese_item)
			logging.info("linkzu="+link)
			request = scrapy.Request("http://www.haocaimao.com"+link, callback=self.parse_item2)
			yield request#返回请求

	#第二个页面
	def parse_item2(self, response):
		#start browser
		#self.driver.get(response.url)
		#loading time interval
		#time.sleep(5)
		for link in response.xpath('//div[@class="mc"]/div[@class="item"]/ul/li/a/@href').extract():
			logging.info("link2="+link)
			request = scrapy.Request("http://www.haocaimao.com"+link, callback=self.parse_item3)
			yield request

	#第三个页面
	def parse_item3(self, response):
		#start browser
		#self.driver.get(response.url)
		#loading time interval
		#time.sleep(5)
		#self.driver.quit()
		for link in response.xpath('//div[@class="box1 cate"]/ul/li/a/@href').extract():
			logging.info("link3="+link)
			request = scrapy.Request("http://www.haocaimao.com"+link, callback=self.parse_item4)
			yield request

		#第四个界面
	def parse_item4(self, response):
		#start browser
		#self.driver.get(response.url)
		#loading time interval
		#time.sleep(5)
		for link in response.xpath('//div[@class="clearfix goodsBox"]/div/p/a/@href').extract():
			logging.info("link4="+link)
			redis=RedisConnect()
			redis.setSadd(self.names,"http://www.haocaimao.com"+link)

					#获取页码集合
		pages = response.xpath('//div[@class="pagin fr"]/a[@class="next"]/@href').extract()
		#print('pages: %s' % pages)#打印页码
		if len(pages) >= 2:#如果页码集合>2
			page_link = pages[-2]#图片连接=读取页码集合的倒数第二个页码
			#page_link = page_link.replace('/a/', '')#图片连接=page_link（a替换成空）
			detail_link = 'http://www.haocaimao.com%s' % page_link
			#print detail_link+"---"
			logging.info("detail_link==next_url="+detail_link)
			request = scrapy.Request(detail_link, callback=self.parse_item)
			yield request#返回请求  yield Request('http://www.haocaimao.com%s' %page_link, callback=self.parse_item4)
