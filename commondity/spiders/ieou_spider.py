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
from commondity.lib.service.redisconnect import *

class IeouSpider(scrapy.Spider):
	name = "ieou"
	names = "spider_"+name + "_redis"
	allowed_domains = ["ieou.com.cn"]
	start_urls = [
		"http://www.ieou.com.cn"
	]
	#构造函数
	def __init__(self):
	   
		log.init_log(settings.get('LOG_DIR'))#
		logging.info("spider start......")
		print "spider start......"
		logging.info("fafafa")

	def get_item(self,i):
		page_link = "http://www.ieou.com.cn/products_list/&pmcId=1&pageNo_Product_list01-103="+i+"&pageSize_Product_list01-103=16.html"
		request = scrapy.Request(pages, callback=self.parse_item2)
		logging.info("-----page_links="+pages)
		yield request

	#主页面
	def parse(self, response):
		#sel是页面源代码，载入scrapy.selector
		sel = Selector(response)
		#每个连接，用@href属性
		for link in sel.xpath('//div[@class="cont-space"]/ul/li/h4/span/a/@href').extract():
			#请求=Request(连接，parese_item)
			logging.info("-----linkzu="+link)
			request = scrapy.Request("http://www.ieou.com.cn"+link, callback=self.parse_item2)
			yield request#返回请求

	#第二个页面
	def parse_item2(self, response):
		#filename = response.url.split("/")[-2]
		#open(filename, 'wb').write(response.body)
		print "999999"+response.url
		for link in response.xpath('//div[@class="Product_list01-d1_c1"]/ul/li/div/div[2]/ul/li[1]/strong/a/@href').extract():
			logging.info("----link2="+link)
			redis=RedisConnect()
			redis.setSadd(self.names,"http://www.ieou.com.cn"+link)

		#获取页码集合
		pages = response.xpath("//div[@class='number']/a/@onclick").extract()
		#末页
		page_link = pages[-1]
		detail_link = page_link.split('(')
		detail_link = detail_link[len(detail_link)-1]
		detail_link = detail_link.split(',')
		detail_link = detail_link[len(detail_link)-2]
		detail_link = int(detail_link)
		for i in range(2,detail_link):
			i = str(i)
			position = response.xpath('//div[@id="Public_breadCrumb01-1361323972998"]/a/text()').extract()
			print position[0] +'777777777777'
			if position[0].encode('gb2312') == '物料搬运':
				print'77777777我是物料搬运'
				pageNO = "http://www.ieou.com.cn/products_list/&pmcId=1&pageNo_Product_list01-103="+i+"&pageSize_Product_list01-103=16.html"
				logging.info("-------page_links---------="+pageNO)
				request = scrapy.Request(pageNO, callback=self.parse_item2)
				yield request
			if position[0].encode('gb2312') == '仓储设施':
				print'777777777777我是仓储设施'
				pageNO = "http://www.ieou.com.cn/products_list/&pmcId=2&pageNo_Product_list01-103="+i+"&pageSize_Product_list01-103=16.html"
				logging.info("-------page_links--------="+pageNO)
				request = scrapy.Request(pageNO, callback=self.parse_item2)
				yield request
			if position[0].encode('gb2312') == '环保安全':
				print'777777777777我是环保安全'
				pageNO = "http://www.ieou.com.cn/products_list/&pmcId=3&pageNo_Product_list01-103="+i+"&pageSize_Product_list01-103=16.html"
				logging.info("-------page_links----------="+pageNO)
				request = scrapy.Request(pageNO, callback=self.parse_item2)
				yield request
			if position[0].encode('gb2312') == '清洁用品':
				print'777777777777我是清洁用品'
				pageNO = "http://www.ieou.com.cn/products_list/&pmcId=4&pageNo_Product_list01-103="+i+"&pageSize_Product_list01-103=16.html"
				logging.info("-------page_links-----------="+pageNO)
				request = scrapy.Request(pageNO, callback=self.parse_item2)
				yield request
			if position[0].encode('gb2312') == '车间设施':
				print'777777777777我是车间设施'
				pageNO = "http://www.ieou.com.cn/products_list/&pmcId=15&pageNo_Product_list01-103="+i+"&pageSize_Product_list01-103=16.html"
				logging.info("-------page_links-------------="+pageNO)
				request = scrapy.Request(pageNO, callback=self.parse_item2)
				yield request
			if position[0].encode('gb2312') == '办公系列':
				print'777777777777我是办公系列'
				pageNO = "http://www.ieou.com.cn/products_list/&pmcId=16&pageNo_Product_list01-103="+i+"&pageSize_Product_list01-103=16.html"
				logging.info("-------page_links------------------="+pageNO)
				request = scrapy.Request(pageNO, callback=self.parse_item2)
				yield request
