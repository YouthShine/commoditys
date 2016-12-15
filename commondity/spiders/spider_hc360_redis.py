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

class LezSpider(scrapy.Spider):
	name = "spider_hc360_redis"
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
		#driver = webdriver.PhantomJS()
		driver = webdriver.PhantomJS()
		driver.get(response.url)
		time.sleep(3)
		body = driver.page_source
		#driver.close()
		HtmlResponses = HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=response)
		try:
			item['productUrl'] = response.url
		except:
			pass
		try:
			item['productName'] = HtmlResponses.xpath("//h1[@id='comTitle']/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		list_brand = ''
		for j in range(1,20):
			try:
				list_brand = response.xpath("//div[@id='pdetail']/div/table/tr[%i]/th/h4/text()" %j).extract()[0].encode('utf-8').replace("\"","\'").strip()
				if '品牌：' in list_brand:
					item['productBrand'] = response.xpath("//div[@id='pdetail']/div/table/tr[%i]/td/text()" %j).extract()[0].encode('utf-8').replace("\"","\'").strip()
					break
			except:
				pass
		list_model = ''
		for j in range(1,20):
			try:
				list_model = response.xpath("//div[@id='pdetail']/div/table/tr[%i]/th/h4/text()" %j).extract()[0].encode('utf-8').replace("\"","\'").strip()
				if '型号：' in list_model:
					item['productModel'] = response.xpath("//div[@id='pdetail']/div/table/tr[%i]/td/text()" %j).extract()[0].encode('utf-8').replace("\"","\'").strip()
					break
			except:
				pass
		try:
			classification_one = response.xpath("//div[@id='head']/div[@id='path']/a[2]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			classification_two = response.xpath("//div[@id='head']/div[@id='path']/a[3]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			classification_three = response.xpath("//div[@id='head']/div[@id='path']/a[4]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		classification = classification_one + '|||' + classification_two + '|||' +classification_three
		item['productClassification'] = classification
		try:
		#去空格 转分   去人民币符号
			item['productPrice'] = response.xpath("//div[@id='oriPriceTop']/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			item['productPrice'] = str(float(filter(lambda ch: ch in '0123456789.~', item['productPrice']))*100)
		except:
			pass
		#图片连接
		try:
			item['productImagePath'] = HtmlResponses.xpath("//a[@id='imgContainer']/@hrefs").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		#print item['image_urls'],"777777"
		try:
			item['productAddres'] = response.xpath("//div[@id='pdetail']/div[@class='d-vopy']/table/tbody/tr[4]/td/text()").extract()[0]
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
		item['productAddres'] = ""
		item['productCompany'] = ""
		names = self.name+'.json'
		item['fileName'] = names

		list_details = response.xpath("//div[@class='d-vopy']/table/tr/th/h4/text()").extract()
		logging.info("-------list_details_len=%i" %len(list_details))
		details = response.xpath("//div[@class='d-vopy']/table/tr/td/text()").extract()
		logging.info("-------details_len=%i" %len(details))
		list_pack = response.xpath("//div[@class='packageParameter tabContent']/div[@class='specsParameter-wrap']/table[@class='standardTable']/tbody/tr[@class='keyValue']/td/text()").extract()
		list_intro = response.xpath("//table[@class='goods-items']/tr[1]/th/text()").extract()
		logging.info("-------list_intro_len=%i" %len(list_intro))
		intro = response.xpath("//div[@class='goods']/table[@class='goods-items']/tr[2]/td/text()").extract()
		logging.info("-------intr_len=%i" %len(intro))
		speci = response.xpath("//span[@id='techParam']/text()").extract()
		logging.info("-------intr_len=%i" %len(speci))
		num_one=0
		for list_details_value in list_details:
			list_details_value = list_details_value.encode('utf-8').replace("\n","").replace("\"","").strip()
			data2 = {}
			data2['attrkey'] = ''
			data2['keyname'] = ''
			if '品牌' in list_details_value:
				num_one+=1
				continue
			if '价格' in list_details_value:
				num_one+=1
				continue
			if '供应商' in list_details_value:
				num_one=0
				continue
			if '保修期' in list_details_value:
				break
			data2['attrkey']=list_details_value
			data2['keyname']=details[num_one]
			details_list.append(data2)
			num_one+=1

		num_two=0
		for list_intro_value in list_intro:
			list_intro_value = list_intro_value.encode('utf-8').replace("\n","").replace("\"","").strip()
			data2 = {}
			data2['attrkey'] = ''
			data2['keyname'] = ''
			if '品牌' in list_intro_value:
				num_two+=1
				continue
			if '价格' in list_intro_value:
				num_two+=1
				continue
			if '供应商' in list_intro_value:
				num_two=0
				continue
			if '保修期' in list_intro_value:
				break
			data2['attrkey']=list_intro_value
			data2['keyname']=intro[num_two]
			intro_list.append(data2)
			num_two+=1

		num_three=1
		for list_speci in speci:
			list_speci = list_speci.encode('utf-8').replace("\n","").replace("\"","").strip()
			list_speci = list_speci.split('：')
			for value_speci in list_speci :
				if num_three%2==1 :
					data2 = {}
					data2['attrkey'] = ''
					data2['keyname'] = ''
					if '商品名称' in value_speci:
						break
					if '品牌' in value_speci:
						break
					data2['attrkey']=value_speci
				else:
					data2['keyname']=value_speci
					speci_list.append(data2)
				num_three+=1

		item['productSpeci'] = speci_list
		item['productPack'] = pack_list
		item['productIntro'] = intro_list
		item['productDetails'] = details_list
		yield item


	   