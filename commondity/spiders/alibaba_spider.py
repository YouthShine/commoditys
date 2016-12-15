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

class AlibabaSpider(scrapy.Spider):
	name = "alibaba"
	names = "spider_"+name + "_redis"
	allowed_domains = ["1688.com"]
	start_urls = [
		"http://page.1688.com/channel/imall/index.html"
	]
	#构造函数
	def __init__(self):
	   
		log.init_log(settings.get('LOG_DIR'))#
		logging.info("spider start......")
		print "spider start......"
		logging.info("fafafa")
	#主页面 

	#第二个页面
	def parse(self, response):
		print "PhantomJS is starting2..."
		driver = webdriver.Chrome()
		driver.get("https://login.1688.com/member/signin.htm?from=sm&Done=https%3A%2F%2Fsec.1688.com%2Fquery.htm%3Faction%3DQueryAction%26event_submit_do_login%3Dok%26smApp%3Dsearchweb2%26smPolicy%3Dsearchweb2-selloffer-anti_Spider-seo-html-checklogin%26smCharset%3DGBK%26smTag%3DMjIyLjE4MS4xMS4xNzIsLDVlZmFiZDUzZDYxNjQ4NjJhYjM5NDIwNGM5OWQ0MDU1%26smReturn%3Dhttps%253A%252F%252Fs.1688.com%252Fselloffer%252F--1036657.html%253Fspm%253Da260b.1103857.1998051674.11.LL2sE6%26smSign%3D93vNPQCN7TtGpd1FpSyaOA%253D%253D")
		time.sleep(5)
		body = driver.page_source
		HtmlResponses = HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=response)  
		driver.find_element_by_xpath("//input[@id='TPL_username_1']").send_keys("18883174492")
		driver.find_element_by_xpath("//input[@id='TPL_password_1']").send_keys("520cf1314520PPDD")
		driver.find_element_by_class_name("J_Submit").click()
		time.sleep(20)
		body = driver.page_source
		HtmlResponses = HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=response)

		#获取页码集合
		pages = response.xpath("//div[@id='product-list']/div[@class='showPagintion']/div[@class='pagintion']/li/a/@href").extract()
		pages_next = ''
		try: 
			pages_next = response.xpath("//div[@id='product-list']/div[@class='showPagintion']/div[@class='pagintion']/li[@class='pg-next']/a/text()").extract()[0]
		except:
			pass
		if len(pages) >= 2 and pages_next!='':
			page_link = pages[-1]
			#page_link = page_link.replace('/a/', '')
			detail_link = 'http://www.ehsy.com%s' % page_link
			#print detail_link+"---"
			logging.info("-------page_links="+detail_link)
			request = scrapy.Request(detail_link, callback=self.parse_item2)
			yield request
	
  