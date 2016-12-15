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

class GomroSpider(scrapy.Spider):
	name = "gomro"
	names = "spider_"+name + "_redis"
	allowed_domains = ["gomro.cn"]
	start_urls = [
		"http://www.gomro.cn/?a=shop"
	]
	def __init__(self):
		log.init_log(settings.get('LOG_DIR'))#
		logging.info("spider start......")
		print "spider start......"
		logging.info("fafafa")
	#Main page
	def parse(self, response):
		sel = Selector(response)
		for link in response.xpath("//div[@class='item']/div[@class='item-inner clearfix']/em/a/@href").extract():
			link = "http://www.gomro.cn/"+link
			logging.info("-------linkzu="+link)
			request = scrapy.Request(link, callback=self.parse_item2)
			yield request

	#Second pages
	def parse_item2(self, response):
		logging.info("-------link2="+response.url)
		page_number = 0
		id = ''
		try:
			commodity_number = response.xpath("//div[@class='goods-filter clearfix']/div[@class='caption']/span[2]/text()").extract()[0].encode('utf-8')
		except:
			commodity_number = '0'
		logging.info("-------commodity_number =" +commodity_number)
		page_f_number = float(commodity_number)/20
		page_i_number = int(page_f_number)
		if page_f_number > page_i_number:
			page_number = page_i_number+2
			logging.info("-------page_number = %i" %page_number)
		if page_f_number == page_i_number:
			page_number = page_i_number
			logging.info("-------page_number = %i" %page_number)
		logging.info("-------link2="+response.url)
		classification = response.xpath("//div[@class='pathbox']/div[@class='path']/a[3]/text()").extract()[0].encode('utf-8')
		if '安全防护' in classification:
			id = '59037'
			print'-------1'+'安全防护'
		if '手工具' in classification:
			id = '59036'
			print'-------2'+'手工具'
		if '刀具' in classification:
			id = '59038'
			print'-------3'+'刀具'
		if '气动液压' in classification:
			id = '59039'
			print'-------4'+'气动液压'
		if '机械传动' in classification:
			id = '59040'
			print'-------5'+'机械传动'
		if '仓储包装' in classification:
			id = '59041'
			print'-------6'+'仓储包装'
		if '工控产品' in classification:
			id = '59042'
			print'-------7'+'工控产品'
		if '照明' in classification:
			id = '59043'
			print'-------8'+'照明'
		for j in range(1,page_number):
			link = "http://www.gomro.cn/?&a=category&id=%s&page=%i" %(id,j)
			request = scrapy.Request(link,callback=self.parse_item3)
			yield request
	#Add to redis
	def parse_item3(self, response):
		logging.info("-------page_link = "+response.url)
		for link in response.xpath("//div[@class='goods_list_box goods_list clearfix']/ul/li/div[@class='caption']/a/@href").extract():
			link = "http://www.gomro.cn/"+link
			logging.info("-------link3="+link)
			redis=RedisConnect()
			redis.setSadd(self.names,link)