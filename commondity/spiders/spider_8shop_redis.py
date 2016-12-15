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
import json
from selenium import webdriver
import time
from scrapy.http import HtmlResponse

class LezSpider(scrapy.Spider):
	name = "spider_8shop_redis"
	url = GetUrls()
	start_urls = url.getUrls(name)
	data1 = []
	data3 = []
	def __init__(self):
	   
		log.init_log(settings.get('LOG_DIR'))
		logging.info("spider start......")
		print "spider start......"
		logging.info("fafafa")
		
	#Details page

	def parse(self, response):
		p = open('aa.html','a+')
		p.write(response.body)
		item = BaseItem()
		details_list = []
		pack_list = []
		intro_list = []
		speci_list = []
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
		#time.sleep(3)
		body = driver.page_source
		#driver.close()
		HtmlResponses = HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=response)
		try:
			item['productUrl'] = response.url
		except:
			pass
		try:
			item['productName'] = HtmlResponses.xpath("//h1[@class='ware_title']/a/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		brand = ''
		try:
			brand = HtmlResponses.xpath("//div[@class='ware_text']/div/text()")[3].extract().encode('utf-8').replace("\r\n","\'").strip()
		except:
			pass
		item['productBrand'] = brand
		model = ''
		try:
			model = HtmlResponses.xpath("//div[@class='ware_text']/div/text()").extract()[6].encode('utf-8').strip()
			if '型号' in model:
				item['productModel'] =  HtmlResponses.xpath("//div[@class='ware_text']/div/text()").extract()[6].encode('utf-8').replace("型号:","").strip()
			else:
				item['productModel'] =  HtmlResponses.xpath("//div[@class='ware_text']/div/text()").extract()[5].encode('utf-8').replace("型号:","").strip()
		except:
			pass
		try:
			classification_one = HtmlResponses.xpath("//div[@id='head']/div[@id='path']/a[2]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			classification_two = HtmlResponses.xpath("//div[@id='head']/div[@id='path']/a[3]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			classification_three = HtmlResponses.xpath("//div[@id='head']/div[@id='path']/a[4]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		classification = classification_one + '|||' + classification_two + '|||' +classification_three
		if classification not in self.data1:
			self.data1.append(classification)
			item['productClassification'] = classification
		
		try:
			item['productPrice'] = response.xpath("//div[@class='rate']/span[@class='fontColor3'][2]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			item['productPrice'] = str(float(filter(lambda ch: ch in '0123456789.~', item['productPrice']))*100)
		except:
			pass
		try:
			item['productImagePath'] = response.xpath('//span[@class="jqzoom"]/img/@src').extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		#print item['image_urls'],"777777"
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
		list_details = HtmlResponses.xpath("//div[@id='para']/table[1]/tbody[2]/tr/td/text()").extract()
		logging.info("-------list_details_len=%i" %len(list_details))
		list_pack = HtmlResponses.xpath("//div[@class='packageParameter tabContent']/div[@class='specsParameter-wrap']/table[@class='standardTable']/tbody/tr[@class='keyValue']/td/text()").extract()
		intro = HtmlResponses.xpath("//div[@id='para']/p[2]/font/text()").extract()
		logging.info("-------intr_len=%i" %len(intro))
		driver.close
		num_one=1
		for value_details in list_details :
			value_details = value_details.encode('utf-8').replace(":","\/").replace("\n","").replace("\"","").strip()
			if num_one%2==2 :
				num_one = 1
				continue
			if num_one%2==1 :
				data2 = {}
				data2['attrkey'] = ''
				data2['keyname'] = ''
				if '品牌' in value_details:
					num_one=0
					continue
				if '型号' in value_details:
					num_one=0
					continue
				data2['attrkey']=value_details
			else:
				if num_one ==0:
					num_one = 1
					continue
				data2['keyname']=value_details
				details_list.append(data2)
			num_one+=1
		num_two=1
		for list_intro in intro:
			list_intro = list_intro.encode('utf-8').replace(":","\/").replace("\n","").replace("\"","").strip()
			list_intro = list_intro.split('：')
			for value_intro in list_intro :
				if num_two%2==1 :
					data2 = {}
					data2['attrkey'] = ''
					data2['keyname'] = ''
					data2['attrkey']=value_intro
				else:
					data2['keyname']=value_intro
					intro_list.append(data2)
				num_two+=1

		item['productSpeci'] = speci_list
		item['productPack'] = pack_list
		item['productIntro'] = intro_list
		item['productDetails'] = intro_list
		yield item

