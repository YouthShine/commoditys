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

class EhsySpider(scrapy.Spider):
	name = "spider_ehsy_redis_0"  
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
		try:
			item['productUrl'] = response.url
		except:
			pass
		try:
			item['productName'] = response.xpath("//div[@class='productDetail product-detail-repair']/h1/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
<<<<<<< HEAD
<<<<<<< HEAD
		#11.28
		brand = ''
		try:
			list_brand = response.xpath("//tr[@class='keyValue']/td[1]/text()").extract()
			for j in range(1,len(list_brand)):
				brand = response.xpath("//tr[@class='keyValue'][%i]/td[1]/text()" %j).extract()[0].encode('utf-8').replace("\"","\'").strip()
				if '品牌'  in brand:
					brand= response.xpath("//tr[@class='keyValue'][%i]/td[2]/text()"%j).extract()[0].encode('utf-8').replace("\"","\'").strip()
					item['productBrand'] = brand
					break
				else:
					brand= response.xpath("//div[@class='detail clearfix'][2]/span[@class='typeValue']/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
					item['productBrand'] = brand.split(' ')[0]
					break
			filter(str.isalnum,item['productBrand'])
		except Exception,e:
			print e
			print "1有数组越界"
		model = ''
		try:
			list_model = response.xpath("//tr[@class='keyValue']/td[1]/text()").extract()
			for k in range(1,len(list_model)):
				model = response.xpath("//tr[@class='keyValue'][%i]/td[1]/text()" %k).extract()[0].encode('utf-8').replace("\"","\'").strip()
				if '型号'  in model:
					model= response.xpath("//tr[@class='keyValue'][%i]/td[2]/text()"%k).extract()[0].encode('utf-8').replace("\"","\'").strip()
					item['productModel'] = model
					break
				else:
					model= response.xpath("//div[@class='detail clearfix'][2]/span[@class='typeValue']/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
					item['productModel'] = model.split(' ')[1]
					break
					#filter(str.isalnum,item['productModel'])
		except Exception,e:
			print e
			print "2有数组越界"
		#11.28
=======
=======
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
		list_brand = ''
		try:
			list_brand = response.xpath("//tr[@class='keyValue'][1]/td[1]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			if '品牌：'  in list_brand:
				brand= response.xpath("//tr[@class='keyValue'][1]/td[2]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
				item['productBrand'] = brand
			else:
				list_brand= response.xpath("//div[@class='detail clearfix'][2]/span[@class='typeValue']/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
				item['productBrand'] = list_brand.split(' ')[0]
				filter(str.isalnum,item['productBrand'])
		except:
			pass
		try:
			item['productModel'] = response.xpath("//div[@class='detailAndBuy']/div[@class='detail'][1]/span[@class='typeValue']/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
<<<<<<< HEAD
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
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
			item['productPrice'] = response.xpath("//span[@class='nowPrice-price']/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			item['productPrice'] = str(float(filter(lambda ch: ch in '0123456789.~', item['productPrice']))*100)
		except:
			pass
		try:
			item['productImagePath'] = response.xpath("//a[@class='magnifier-thumb-wrapper']/img/@src").extract()[0].encode('utf-8').replace("\"","\'").strip()
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
		list_speci = response.xpath("//div[@class='tabContent data-tab-index1']/div[@class='specsParameter-wrap']/table[@class='standardTable']/tr[@class='keyValue']/td/text()").extract()
		list_pack = response.xpath("//div[@class='tabContent data-tab-index2']/div[@class='specsParameter-wrap']/table[@class='standardTable']/tr[@class='keyValue']/td/text()").extract()
		num_one=1
		for value_speci in list_speci :
			value_speci = value_speci.encode('utf-8').replace(":","\/").replace("\n","").replace("\"","").strip()
			if num_one%2==2 :
				num_one = 1
				continue
			if num_one%2==1 :
				data2 = {}
				data2['attrkey'] = ''
				data2['keyname'] = ''
				if '品牌' in value_speci:
					num_one=0
					continue
				data2['attrkey']=value_speci
			else:
				if num_one ==0:
					num_one = 1
					continue
				data2['keyname']=value_speci
				speci_list.append(data2)
			num_one+=1
		num_two=1
		for value_pack in list_pack :
			value_pack = value_pack.encode('utf-8').replace(":","\/").replace("\n","").replace("\"","").strip()
			if num_two%2==1 :
				data2 = {}
				data2['attrkey'] = ''
				data2['keyname'] = ''
				data2['attrkey']=value_pack
			else :
				data2['keyname']=value_pack
				pack_list.append(data2)
			num_two+=1

		item['productSpeci'] = speci_list
		item['productPack'] = pack_list
		item['productIntro'] = intro_list
		item['productDetails'] = intro_list
		yield item
