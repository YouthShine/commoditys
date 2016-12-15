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

class VipmroSpider(scrapy.Spider):
	name = "vipmro"
	names = "spider_"+name + "_redis"
	allowed_domains = ["vipmro.com"]
	start_urls = [
		"http://www.vipmro.com/"
	]
	#构造函数
	def __init__(self):
		log.init_log(settings.get('LOG_DIR'))#
		logging.info("spider start......")
		print "spider start......"
		logging.info("fafafa")
	#主页面
	def parse(self, response):
		print "PhantomJS is starting1..."
		driver = webdriver.PhantomJS()
		#driver = webdriver.Chrome()
		driver.get(response.url)
		time.sleep(3)
		body = driver.page_source
		#driver.close()
		HtmlResponses = HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=response)
		for link in HtmlResponses.xpath("//div[@class='nav-main-right hide J_cate_right']/div/div/ul/li/a/@href").extract():
			#请求=Request(连接，parese_item)
			logging.info("-----linkzu="+link)
			request = scrapy.Request(link, callback=self.parse_item2)
			yield request#返回请求

	#第二个页面
	def parse_item2(self, response):
		print "PhantomJS is starting2..."
		driver = webdriver.PhantomJS()
		driver.get(response.url)
		time.sleep(3)
		body = driver.page_source
		HtmlResponses = HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=response)
		#获取页码集合
		page_number = 0
		pages_next = ''
		while True:
			logging.info("----current_link="+response.url)
			for link in HtmlResponses.xpath("//div[@class='list-main-box-cont']/a/@href").extract():
				logging.info("----link2="+link)
				redis=RedisConnect()
				redis.setSadd(self.names,link)
			page_next = HtmlResponses.xpath("//div[@class='list-page J_page']/a/text()").extract()
			try:
				pages_next = page_next[-2].encode('utf-8')
			except:
				pass
			page_number = page_number +1
			sum_page_number = page_number
			page_s_number = str(sum_page_number)
			if pages_next != '下一页':
				break
			driver.find_element_by_link_text('下一页').click()
			time.sleep(3)
			body = driver.page_source
			HtmlResponses = HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=response)
			logging.info("-----page_link="+page_s_number)

