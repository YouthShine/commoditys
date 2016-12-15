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
from commondity.lib.service.geturls import *
from selenium import webdriver
import time
from scrapy.http import HtmlResponse
import re

class AbizSpider(scrapy.Spider):
	name = "spider_gongboshi_redis"  
	url = GetUrls()
	start_urls = url.getUrls(name)


	def __init__(self):
		log.init_log(settings.get('LOG_DIR'))
		logging.info("spider start......")
		print "spider start......"
		logging.info("fafafa")

	#Details page
	def parse(self, response):
		item = BaseItem()
		speci_list = []
		pack_list = []
		intro_list = []
		details_list = []
		item['productUrl'] = ''
		item['productName'] = ''
		item['productBrand'] = ''
		item['productModel'] = ''
		item['productClassification'] = ''
		item['productPrice'] = ''
		item['productImagePath'] = ''
		item['productAddres'] = ""
		item['productCompany'] = ''
		item['fileName'] = ''
		item['productDetails'] = ""
		item['productPack'] = ""
		item['productIntro'] = ""
		item['productSpeci'] = ""
		classification_one = ''
		classification_two = ''
		classification_three = ''
		#print "PhantomJS is starting1..."
		#driver = webdriver.PhantomJS()
		#driver.get(response.url)
		#time.sleep(3)
		#body = driver.page_source
		#HtmlResponses = HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=response)
		try:
			item['productUrl'] = response.url
		except:
			pass
		try:
			item['productName'] = response.xpath("//h1[@id='title']/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			classification_one = response.xpath("//div[@class='pos']/a[3]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			classification_two = response.xpath("//div[@class='pos']/a[4]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			classification_three = response.xpath("//div[@class='pos']/a[5]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		classification = classification_one + '|||' + classification_two + '|||' + classification_three
		item['productClassification'] = classification
		try:
			item['productPrice'] = response.xpath("//span[@class='f_price px16']/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			item['productPrice'] = str(float(filter(lambda ch: ch in '0123456789.~', item['productPrice']))*100)
		except:
			pass
		try:
			imagePath = response.xpath("//div[@id='mid_div']/img/@src").extract()[0].encode('utf-8').replace("\"","\'").strip()
			item['productImagePath'] = imagePath
		except:
			pass
		try:
			item['productAddres'] = ""
		except:
			pass
		try:
			item['productCompany'] = ""
		except:
			pass
		names = self.name+'.json'
		try:
			item['fileName'] = names
		except:
			pass
		print "PhantomJS is starting1..."
		driver = webdriver.PhantomJS()
		driver.get(response.url)
		time.sleep(3)
		body = driver.page_source
		HtmlResponses = HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=response)
		list_brand = HtmlResponses.xpath("//table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr/td[1]").extract()
		list_speci_th = response.xpath("//div[@class='col-xs-12 nopadding border-ccc attrDiv']/div/p/text()").extract()
		list_detail = response.xpath("//div[@id='content']").extract()
		logging.info("----------list_detail_len=%i"%len(list_detail))
		list_intro = response.xpath("//div[@id='tbc_13']/div[@class='intro_box']").extract()
		logging.info("----------list_intro_len=%i"%len(list_intro))
		for j in range(1,len(list_brand)) :
			brand = HtmlResponses.xpath("//table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[%i]/td[1]/text()"%j).extract()[0].encode('utf-8').replace(":","\/").replace("\n","").replace("\"","").strip()
			if "型号" in brand :
				item['productModel'] = HtmlResponses.xpath("//table/tbody/tr[2]/td[3]/table/tbody/tr[%i]/td[2]/a[@class='b']/text()"%j).extract()[0].encode('utf-8').replace(":","\/").replace("\n","").replace("\"","").strip()
				continue
			if "品牌" in brand :
				item['productBrand'] = HtmlResponses.xpath("//table/tbody/tr[2]/td[3]/table/tbody/tr[%i]/td[2]/a[@class='b']/text()"%j).extract()[0].encode('utf-8').replace(":","\/").replace("\n","").replace("\"","").strip()
				break
		driver.close()
		#11.28
		brand = ''
		try:
			brand= response.xpath("//dl[@class='pro-info-prop pro-info-brand']/dd[@class='pro-info-cons']/text()").extract()[0].encode('utf-8').replace("\t","").replace("\n","").replace("\b","").replace("\r","").strip()
			item['productBrand'] = brand
		except:
			pass
		model = ''
		try:
			model= response.xpath("//dl[@class='pro-info-prop pro-info-model']/dd[@class='pro-info-cons']/text()").extract()[0].encode('utf-8').replace("\t","").replace("\n","").replace("\b","").strip()
			item['productModel'] = model
		except:
			pass
		#11.28
		for value_detail in list_detail:
			value_detail = value_detail.encode('utf-8').replace("\t","").replace("\n","").replace("\b","").replace("<br>","").replace("</br>","").replace("\r","").strip()
			dr = re.compile(r'<[^>]+>',re.S)
			dd_value_detail = dr.sub('',value_detail)
			details_list.append(dd_value_detail) 
		cancel = ''
		try:
			cancel_l = response.xpath("//p[@class='link-detail']/text()").extract()
			for cancel_s in cancel_l:
				cancel_s = cancel_s.encode('utf-8').replace("\t","").replace("\n","").replace("\b","").replace("<br>","").replace("</br>","").replace("\r","").strip()
				cancel+=cancel_s
		except:
			pass
		for value_intro in list_intro:
			value_intro = value_intro.encode('utf-8').replace("\t","").replace("\n","").replace("\b","").replace("<br>","").replace("</br>","").replace("\r","").strip()
			value_intro.replace(cancel,'')
			dr = re.compile(r'<[^>]+>',re.S)
			dd_value_intro = dr.sub('',value_intro)
			intro_list.append(dd_value_intro)

		item['productSpeci'] = speci_list
		item['productPack'] = pack_list
		item['productIntro'] = intro_list
		item['productDetails'] = details_list
		yield item