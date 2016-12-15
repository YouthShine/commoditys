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

class MctmallSpider(scrapy.Spider):
	name = "mctmall"
	names = "spider_"+name+"_redis"
	allowed_domains = ["mctmall.cn"]
	start_urls = [
		"http://www.mctmall.cn/"
	]
#Main page 
	def parse(self, response):
		sel = Selector(response)
		for link in sel.xpath("//dl[@class='cata-group-btn']/dt[@class='cata-group-head']/h3[@class='group-title']/a/@href").extract():
			link = "http://www.mctmall.cn"+link
			logging.info("-------linkzu="+link)
			request = scrapy.Request(link, callback=self.parse_item2)
			yield request
	#Constructor
	def __init__(self):
	   
		log.init_log(settings.get('LOG_DIR'))#
		logging.info("spider start......")
		print "spider start......"
		logging.info("fafafa")
	#Second pages
	def parse_item2(self, response):
		logging.info("-------link2="+response.url)
		page_number = 0
		category = ''
		cat = ''
		try:
			commodity_number = response.xpath("//b[@class='op-search-result']/text()").extract()[0].encode('utf-8')
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
		url = "http://www.mctmall.cn/gallery-ajax_get_goods.html"
		classification = response.xpath("//div[@id='navbar']/span[@class='now']/text()").extract()[0].encode('utf-8')
		if classification =='量具':
			cat_id = '9'
			print'-------1'+'量具'
		if classification =='刀具':
			cat_id = '10'
			print'-------2'+'刀具'
		if classification =='精密仪器':
			cat_id = '11'
			print'-------3'+'精密仪器'
		if classification =='机床及附件':
			cat_id = '13'
			print'-------4'+'机床及附件'
		if classification =='五金工具':
			cat_id = '12'
			print'-------5'+'五金工具'
		if classification =='磨具、磨料及模具':
			cat_id = '439'
			print'-------6'+'磨具、磨料及模具'
		if classification =='金属材料':
			cat_id = '704'
			print'-------7'+'金属材料'
		for i in range(1,page_number):
			formdata = {
				'cat_id':cat_id,
				'virtual_cat_id':'',
				'orderBy':'',
				'showtype':'grid',
				'page':str(i)
				}
			request = FormRequest(url,formdata=formdata,callback=self.parse_item3)
			yield request
	#Add to redis
	def parse_item3(self, response):
		for link in response.xpath("//div[@class='goods-info']/h3[@class='goods-name']/a/@href").extract():
			link = link.replace('\\','')
			link = link.replace('\"','')
			link = "http://www.mctmall.cn"+link
			logging.info("-------link3="+link)
			redis=RedisConnect()
			redis.setSadd(self.names,link)