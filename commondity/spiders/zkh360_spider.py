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

#Crawling logic
class ZkhSpider(scrapy.Spider):

	#Reptile name (unique)
	name = 'zkh360'

	#Set  redis key
	names="spider_"+name+"_redis"

	#Start path (crawler entry)
	start_urls=["http://www.zkh360.com/newzkh_catalog/2.html"]

	#Data container (for heavy)
	items=[]

	#Climb path
	visitedWebUrl=[]

	#No path
	noAccessURL=[]

	def __init__(self):
		log.init_log(settings.get('LOG_DIR'))


	def parse(self,response):
		#Analytical framework
		driver = webdriver.PhantomJS()
		#driver = webdriver.Chrome()
		driver.get(response.url)
		time.sleep(1)
		body = driver.page_source
		# driver.close()
		sel = HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=response)
		tempContent=sel.xpath(".//div[@id='div_products']/div[1]/ul/li")
		
		#Loop body
		for temp in tempContent:
			#Parse text
			commodityUrls=temp.xpath("a/@href").extract()
			commodityUrl= ["http://www.zkh360.com"+t.encode('utf-8').replace("\"","\'").strip() for t in commodityUrls] 

			#Check whether duplicate data
			commodityUrl=commodityUrl[0]
			if not commodityUrl in self.items:
				self.items.append(commodityUrl)
				#yield Request(commodityUrl,callback=self.content_parse)
				redis=RedisConnect()
				redis.setSadd(self.names,commodityUrl)
				print "-------------------------------------------------insert url in redis:",commodityUrl

			self.analysisUrl(response,sel)
			while len(self.noAccessURL) > 0:
				url=self.noAccessURL[0]
				self.visitedWebUrl.append(url)
				self.noAccessURL.pop(0)
				yield Request(url,callback=self.parse)


	def analysisUrl(self,response,selectors):
		urls=selectors.xpath(".//div[@id='page_navigation']/a/@href").extract()
		i=0
		while i<len(urls):
			temp=urls[i].strip()
			if temp == "" :
				urls[i].pop(i)
				continue
			else:
				urls[i]=temp
				i+=1

		self.handleUrl(response,urls,"http://www.zkh360.com/")


	def handleUrl(self,response,urls,basicsUrlPath=""):
		self.visitedWebUrl.append(response.url)
		for url in urls:
			url=basicsUrlPath+url
			if not url in self.visitedWebUrl:
				if not url in self.noAccessURL:
					self.noAccessURL.append(url)

		  