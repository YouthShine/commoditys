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

class NalipeiSpider(scrapy.Spider):
	name = "nalipei"
	names = "spider_"+name + "_redis"
	allowed_domains = ["nalipei.com"]
	start_urls = [
		"http://www.nalipei.com"
	]
	#构造函数
	def __init__(self):
	   
		log.init_log(settings.get('LOG_DIR'))#
		logging.info("spider start......")
		print "spider start......"
		logging.info("fafafa")
	#主页面 
	def parse(self, response):
		#print "PhantomJS is starting1..."
		#driver = webdriver.PhantomJS()
		#driver = webdriver.PhantomJS()
		#driver.get(response.url)
		#time.sleep(3)
		#body = driver.page_source
		#driver.close()
		#HtmlResponses = HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=response)
		for link in response.xpath("//section[@id='category']/div/div/div/div//@href").extract():
			link = "http://www.nalipei.com"+link
			logging.info("-------linkzu="+link)
			request = scrapy.Request(link, callback=self.parse_item2)
			yield request#返回请求

	#第二个页面
	def parse_item2(self, response):
		logging.info("-------link2="+response.url)
		print "PhantomJS is starting1..."
		driver = webdriver.PhantomJS()
		driver = webdriver.PhantomJS()
		driver.get(response.url)
		time.sleep(3)
		body = driver.page_source
		#driver.close()
		HtmlResponses = HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=response)
		driver.close()
		page = HtmlResponses.xpath("//ul[@id='pagination_end']/li/a/text()").extract()
		print "3333333333",len(page),"------",page
		page_i_number = 1
		try:
			if "尾页" in page[-1].encode('utf-8'):
				page_s_number = page[-3].encode('utf-8')
			else:
				page_s_number = page[-1].encode('utf-8')
			page_i_number = int(page_s_number)
		except:
			pass
		url = "http://www.nalipei.com/categorylist/categoryList"
		for i in range(1,page_i_number):
			formdata = {
				'grade':'3',
				'itemid':'10094',
				'attrVals':'',
				'itemids':'1580/10064/10094',
				'sortField':'',
				'sortWay':'',
				'brandId':'',
				'cateId':'',
				'showView':'view',
				't':'1480469648652',
				'pageNumber':str(i)
				}
			request = FormRequest(url,formdata=formdata,callback=self.parse_item3)
			yield request

		#获取页码集合
		

	#Add to redis
	def parse_item3(self, response):
		logging.info("-------page_link="+response.url)
		for link in response.xpath("//div[@class='col-xs-12']/div/div/span/a[@class='blacklink']/@href").extract():
			link = "http://www.nalipei.com"+link
			logging.info("-------link3="+link)
			redis=RedisConnect()
			redis.setSadd(self.names,link)