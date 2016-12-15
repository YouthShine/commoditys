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

class AxmroSpider(scrapy.Spider):
	name = "axmro"
	names = "spider_"+name + "_redis"
	allowed_domains = ["axmro.com"]
	start_urls = [
		"http://www.axmro.com/"
	]
	#Constructor
	def __init__(self):
	   
		log.init_log(settings.get('LOG_DIR'))#
		logging.info("spider start......")
		print "spider start......"
		logging.info("fafafa")
	#Main pages
	def parse(self, response):
		sel = Selector(response)
		for link in sel.xpath("//div[@class='left_menu_div']/div[@class='allsort']/div/span/h3/a/@href").extract():
			logging.info("-------linkzu="+link)
			request = scrapy.Request("http://www.axmro.com"+link, callback=self.parse_item2)
			yield request
	#Second pages
	def parse_item2(self, response):
		logging.info("-------link2="+response.url)
		page_number = 0
		AspNetPager1_input = ''
		__EVENTARGUMENT = ''
		try:
			commodity_number = response.xpath("//span[@id='lblCount']/text()").extract()[0].encode('utf-8')
		except:
			commodity_number = '0'
		logging.info("-------commodity_number =" +commodity_number)
		page_f_number = float(commodity_number)/16
		page_i_number = int(page_f_number)
		if page_f_number > page_i_number:
			page_number = page_i_number+2
			logging.info("-------page_number = %i" %page_number)
		if page_f_number == page_i_number:
			page_number = page_i_number
			logging.info("-------page_number = %i" %page_number)
		logging.info("-------link2="+response.url)
		url = "http://www.axmro.com/product/ui_prolist.aspx?classid=802"
		for i in range(1,page_number):
			formdata = {
				'__EVENTTARGET':'AspNetPager1',
				'__EVENTARGUMENT':str(i),
				'seach':'',
				'hidzhuangtai':'all',
				'hidpinpai':'all',
				'hidprice':'all',
				'hidclass':'all',
				'hidkeyclass':'',
				'hidkey':'all',
				'AspNetPager1_input':str(i-1)
				}
			request = FormRequest(url,formdata=formdata,callback=self.parse_item3)
			yield request
	#Add to redis
	def parse_item3(self, response):
		for link in response.xpath("//div[@id='main']/div[@id='content']/div[@id='second']/dl/dd[1]/a/@href").extract():
			link = link.replace('\\','')
			link = link.replace('\"','')
			link = "http://www.axmro.com/product/"+link
			logging.info("-------link3="+link)
			redis=RedisConnect()
			redis.setSadd(self.names,link)