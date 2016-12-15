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

class NalipeiSpider(scrapy.Spider):
	name = "spider_nalipei_redis"  
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
		print "PhantomJS is starting1..."
		driver = webdriver.PhantomJS()
		driver.get(response.url)
		time.sleep(3)
		body = driver.page_source
		HtmlResponses = HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=response)
		try:
			item['productUrl'] = response.url
		except:
			pass
		try:
			item['productName'] = HtmlResponses.xpath("//div[@class='panel-heading panel-heading-div']/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			classification_one = response.xpath("//div[@class='crumbs']/span[2]/a/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			classification_two = response.xpath("//div[@class='crumbs']/span[3]/a/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			classification_three = response.xpath("//div[@class='crumbs']/span[4]/a/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		classification = classification_one + '|||' + classification_two + '|||' + classification_three
		item['productClassification'] = classification
		try:
			item['productPrice'] = HtmlResponses.xpath("//font[@class='price-font'][2]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			item['productPrice'] = str(float(filter(lambda ch: ch in '0123456789.~', item['productPrice']))*100)
		except:
			pass
		try:
			item['productImagePath'] = HtmlResponses.xpath("//img[@id='zoomimg']/@src").extract()[0].encode('utf-8').replace("\"","\'").strip()
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
		list_speci_tr = HtmlResponses.xpath("//div[@class='col-xs-12 nopadding border-ccc attrDiv']/div/b/text()").extract()
		list_speci_th = HtmlResponses.xpath("//div[@class='col-xs-12 nopadding border-ccc attrDiv']/div/p/text()").extract()
		list_detail = HtmlResponses.xpath("//div[@id='prd-desc-mdeditor']/p/text()").extract()
		driver.close()
		num_one=0
		for value_speci in list_speci_tr :
			data2 = {}
			value_speci = value_speci.encode('utf-8').replace(":","\/").replace("\n","").replace("\"","").strip()
			if "型号" in value_speci :
				item['productModel'] = list_speci_th[num_one]
				num_one += 1
				continue
			if "品牌" in value_speci :
				item['productBrand'] = list_speci_th[num_one]
				num_one += 1
				continue
			data2['attrkey']=value_speci
			data2['keyname']=list_speci_th[num_one]
			speci_list.append(data2)
			num_one+=1
		#11.28
		brand = ''
		try:
			brand= HtmlResponses.xpath("//div[@class='form-group margin-left_53 margin-bottom-0'][1]/div/p/font/text()").extract()[0].encode('utf-8').replace("\t","").replace("\n","").replace("\b","").strip()
			if '/' in brand and item['productBrand'] =='':
				item['productBrand'] = brand.split('/')[0]
			else:
				item['productBrand'] = brand
		except:
			pass
		model = ''
		try:
			model= HtmlResponses.xpath("//div[@class='form-group margin-left_53 margin-bottom-0'][1]/div/p/font/text()").extract()[0].encode('utf-8').replace("\t","").replace("\n","").replace("\b","").strip()
			if '/' in brand and item['productModel'] =='':
				item['productModel'] = model.split('/')[1]
		except:
			pass
		#11.28
		detail=' '
		for value_detail in list_detail:
			value_detail = value_detail.encode('utf-8').replace("\t","").replace("\n","").replace("\b","").replace("<br>","").replace("</br>","").strip()
			detail +=value_detail
		details_list.append(detail)

		item['productSpeci'] = speci_list
		item['productPack'] = pack_list
		item['productIntro'] = intro_list
		item['productDetails'] = details_list
		yield item