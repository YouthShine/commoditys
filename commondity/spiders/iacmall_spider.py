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
import codecs
import json
from scrapy.http import FormRequest
from scrapy.http import HtmlResponse
from commondity.lib.service.redisconnect import *
from commondity.lib.service.geturls import * 
from scrapy.http import HtmlResponse

class IacmallSpider(scrapy.Spider):
	name = "iacmall"
	names = "spider_"+name+"_redis"
	allowed_domains = ["iacmall.com"]
	start_urls = [
		"http://www.iacmall.com"
	]
	#Constructor
	def __init__(self):
		log.init_log(settings.get('LOG_DIR'))#
		logging.info("spider start......")
		print "spider start......"
		logging.info("fafafa")
#Main page 
	def parse(self, response):
		sel = Selector(response)
		for link in sel.xpath("//div[@class='menu_box']/div[@class='j-menu']/ul/li/a/@href").extract():
			logging.info("-------linkzu="+link)
			request = scrapy.Request(link, callback=self.parse_item2)
			yield request
	#Second pages
	def parse_item2(self, response):
		logging.info("-------link2="+response.url)
		page_number = 0
		category = ''
		cat = ''
		commodity_number = response.xpath("//span[@id='goods_count']/text()").extract()[0].encode('utf-8')
		commodity_number = filter(str.isalnum,commodity_number)
		logging.info("-------commodity_number =" +commodity_number)
		page_f_number = float(commodity_number)/48
		page_i_number = int(page_f_number)
		if page_f_number > page_i_number:
			page_number = page_i_number+2
			logging.info("-------page_number = %i" %page_number)
		if page_f_number == page_i_number:
			page_number = page_i_number
			logging.info("-------page_number = %i" %page_number)
		url = "http://www.iacmall.com/category.php"
		classification = response.xpath("//div[@class='goods_filter']/div[@class='filter_title clearfix']/h1/text()").extract()[0].encode('utf-8')
		if classification =='电工器材':
			category = '801'
			cat = '801'
			print'-------1'+'电工器材'
		if classification =='电气控制':
			category = '883'
			cat = '883'
			print'-------2'+'电气控制'
		if classification =='工控产品':
			category = '882'
			cat = '882'
			print'-------3'+'工控产品'
		if classification =='劳保用品':
			category = '197'
			cat = '197'
			print'-------4'+'劳保用品'
		if classification =='安防监控':
			category = '887'
			cat = '887'
			print'-------5'+'安防监控'
		if classification =='五金工具':
			category = '884'
			cat = '884'
			print'-------6'+'五金工具'
		if classification =='仪器仪表':
			category = '888'
			cat = '888'
			print'-------7'+'仪器仪表'
		if classification =='照明工业':
			category = '890'
			cat = '890'
			print'-------8'+'照明工业'
		if classification =='机械部件':
			category = '881'
			cat = '881'
			print'-------9'+'机械部件'
		for i in range(1,page_number):
			formdata = {
				'act':'ajax',
				'selpage':'',
				'category':category,
				'keywords':'',
				'sort':'goods_id',
				'order':'DESC',
				'cat':cat,
				'brand':'0',
				'price_min':'0',
				'price_max':'0',
				'filter_attr':'',
				'display':'grid',
				'page':str(i),
				'snumber':'0'
				}
			request = FormRequest(url,formdata=formdata,callback=self.parse_item3)
			yield request
	#Add to redis
	def parse_item3(self, response):
		for link in response.xpath("//a/@href").extract():
			link = link.replace('\\','')
			link = link.replace('\"','')
			logging.info("-------link3="+link)
			redis=RedisConnect()
			redis.setSadd(self.names,link)