# -*- coding: utf-8 -*-
import scrapy
import math
import os
import time
from commondity.items.base_item import BaseItem
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from commondity.lib.service import log
import logging
from scrapy.conf import settings
from scrapy.http import Request
from selenium import webdriver
from commondity.lib.service.redisconnect import *
from commondity.lib.service.geturls import * 
import time
from scrapy.http import HtmlResponse
import os
import urllib
import codecs
import json
class LezSpider(scrapy.Spider):
	name = "spider_axmro_redis"
	url = GetUrls()
	start_urls = url.getUrls(name)
	def __init__(self):
	   
		log.init_log(settings.get('LOG_DIR'))
		logging.info("spider start......")
		print "spider start......"
		logging.info("fafafa")

	#Details page 

	def parse(self, response):
<<<<<<< HEAD
<<<<<<< HEAD
=======
		print "PhantomJS is starting1..."
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
		print "PhantomJS is starting1..."
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
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
		try:
			item['productUrl'] = response.url
		except:
			pass
		try:
			item['productName'] = response.xpath('//div[@class="goods_info"]/div/h1/text()').extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			item['productBrand'] = response.xpath("//div[@class='right']/p[@class='one']/text()").extract()[2].encode('utf-8').replace("品牌：","").strip()
		except:
			pass
		try:
			item['productModel'] = response.xpath("//div[@class='right']/p[@class='one']/text()").extract()[1].encode('utf-8').replace("原始型号：","").strip()
		except:
			pass
		try:
			classification_one = response.xpath("//div[@id='first']/ul/li[4]/a/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			classification_two = response.xpath("//div[@id='first']/ul/li[7]/a/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			classification_three = response.xpath("//div[@id='first']/ul/li[9]/a/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		classification = classification_one + '|||' + classification_two + '|||' + classification_three
		item['productClassification'] = classification
		try:
			item['productPrice'] = response.xpath("//div[@id='divXunjia']/font/b/text()").extract()[0].encode('utf-8').replace("价格：","").strip()
		except:
			pass
		if item['productPrice'] == '询价':
				item['productPrice'] =0.0
		if item['productPrice'] == '':
			try:
				item['productPrice'] = response.xpath("//div[@id='divPrice']/text()").extract()[1].encode('utf-8').strip()
			except:
				pass
		try:
			item['productPrice'] = str(float(filter(lambda ch: ch in '0123456789.~', item['productPrice']))*100)
		except:
			pass
		try:
<<<<<<< HEAD
<<<<<<< HEAD
			item['productImagePath'] = "http://www.axmro.com"+response.xpath("//div[@class='tool']/div[1]/img/@src").extract()[0].encode('utf-8').replace("\"","\'").replace("\\","").strip()
=======
			item['productImagePath'] = "http://www.axmro.com"+response.xpath("//div[@class='tool']/div[1]/img/@src").extract()[0].encode('utf-8').replace("\"","\'").strip()
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
			item['productImagePath'] = "http://www.axmro.com"+response.xpath("//div[@class='tool']/div[1]/img/@src").extract()[0].encode('utf-8').replace("\"","\'").strip()
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
		except:
			pass
		try:
			item['productAddres'] = response.xpath("//div[@class='right']/p[@class='one']/text()").extract()[1].encode('utf-8').replace("品牌所属地：","").strip()
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
		list_details = response.xpath("//div[@id='para']/table[1]/tbody[2]/tr/td/text()").extract()
		logging.info("-------list_details_len=%i" %len(list_details))
		list_pack = response.xpath("//div[@class='packageParameter tabContent']/div[@class='specsParameter-wrap']/table[@class='standardTable']/tbody/tr[@class='keyValue']/td/text()").extract()
		intro = response.xpath("//span[@id='PDescriptiion']/text()").extract()
		logging.info("-------intr_len=%i" %len(intro))
		speci = response.xpath("//span[@id='techParam']/text()").extract()
		logging.info("-------intr_len=%i" %len(speci))
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
			list_intro = list_intro.encode('utf-8').replace("\n","").replace("\"","").strip()
			list_intro = list_intro.split('：')
			for value_intro in list_intro :
				if num_two%2==1 :
					data2 = {}
					data2['attrkey'] = ''
					data2['keyname'] = ''
					if '商品名称' in value_intro:
						break
					if '品牌' in value_intro:
						break
					data2['attrkey']=value_intro
				else:
					data2['keyname']=value_intro
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

		product_intro = response.xpath("//span[@id='PDescription']/text()").extract()
		product_pack = response.xpath("//td[@id='imgDiv']/div[@id='div3']/font/b/text()").extract()
		filename = self.name+".txt"
		file = open("data/"+filename, 'a+')
		file.write("\n"+"productUrl:"+response.url+"\n")
		file.write("productIntro:"+"\n")
		for intro in product_intro:
			intro = intro.encode('utf-8').replace("\b","").replace("<br/>","").replace("<br>","").strip()
			file.write(intro+"\n")
		file.write("productPack:"+"\n")
		for pack in product_pack:
			pack = pack.encode('utf-8').replace("\"","").strip()
			file.write(pack+"\n")
		file.close()

		item['productSpeci'] = speci_list
		item['productPack'] = pack_list
		item['productIntro'] = intro_list
		item['productDetails'] = details_list
		yield item


