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
from commondity.lib.service.redisconnect import *
from commondity.tools import *



#Crawling logic
class MroSpider(scrapy.Spider):

	#Reptile name (unique)
	name = '315mro'

	#Set  redis key
	names="spider_"+name+"_redis"

	#Allowable range
	allowed_domains=["315mro.com"]

	#Start path (crawler entry)
	start_urls=["http://www.315mro.com/ProductType/"]

	#Data container (for heavy)
	items=[]

	#Climb path
	visitedWebUrl=[]

	#No path
	noAccessURL=[]

	def __init__(self):
		log.init_log(settings.get('LOG_DIR'))

	#Get a list of pages
	def parse(self,response):
		#Analytical framework
		sel = Selector(response)
		tempContent=sel.xpath(".//div[@class='categorie_de_box']/div")
		
		#Loop body
		for temp in tempContent:
			temps=temp.xpath("div")
			i=0
			while i < len(temps):
				temps_a=temps.xpath("a/@href").extract()
				for x in temps_a:
					x=x.strip()
					if not x in self.visitedWebUrl:
						if not x in self.noAccessURL:
							self.noAccessURL.append("http://www.315mro.com"+x)
				i+=1
				
		while len(self.noAccessURL) > 0:
			url=self.noAccessURL[0]
			self.visitedWebUrl.append(url)
			self.noAccessURL.pop(0)
			yield Request(url,callback=self.sec_parse)

	def  sec_parse(self,response):
		#Analytical framework
		sel = Selector(response)
		tempContent=sel.xpath(".//div[@class='pro_show_list']/dl")
		
		#Loop body
		for temp in tempContent:
			#Parse text
			commodityUrls=temp.xpath("dd/p[1]/a/@href").extract()

			if len(commodityUrls)>0:
				commodityUrl= ["http://www.315mro.com"+t.encode('utf-8').replace("\"","\'").strip() for t in commodityUrls] 

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
					yield Request(url,callback=self.sec_parse)

	#Analytic path
	def analysisUrl(self,response,selectors):
		urls=selectors.xpath(".//div[@class='megas512']/a/@href").extract()
		i=0
		while i<len(urls):
			temp=urls[i].strip()
			if temp == "" :
				urls[i].pop(i)
				continue
			else:
				urls[i]=temp
				i+=1

		self.handleUrl(response,urls,"http://www.315mro.com/ProductList/")

	#Hand path
	def handleUrl(self,response,urls,basicsUrlPath=""):
		self.visitedWebUrl.append(response.url)
		for url in urls:
			url=basicsUrlPath+url
			if not url in self.visitedWebUrl:
				if not url in self.noAccessURL:
					self.noAccessURL.append(url)
		

		  