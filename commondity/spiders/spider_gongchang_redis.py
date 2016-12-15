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

class LezSpider(scrapy.Spider):
	name = "spider_gongchang_redis"
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
			classification_one = response.xpath("//div[@class='layout']/div[@class='path']/a[2]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			classification_two = response.xpath("//div[@class='layout']/div[@class='path']/a[3]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			classification_three = response.xpath("//div[@class='layout']/div[@class='path']/a[4]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		classification = classification_one + '|||' + classification_two + '|||' +classification_three
		item['productUrl'] = response.url
		try:
			item['productName'] = response.xpath("//div[@class='prodetails']/h1[@class='protitle']/text()").extract()[0].encode('utf-8').replace("\"","\'").strip() 
		except:
			pass
		list_brand = []
		try:
			list_brand = response.xpath("//ul[@class='list2 clf']/li[@class='itm']/span[@class='dt']/text()").extract()
			for j in range(1,len(list_brand)):
				brand = response.xpath("//ul[@class='list2 clf']/li[@class='itm'][%i]/span[@class='dt']/text()" %j).extract()[0].encode('utf-8')
				model = response.xpath("//ul[@class='list2 clf']/li[@class='itm'][%i]/span[@class='dt']/text()" %j).extract()[0].encode('utf-8')
				if '品牌' in brand:
					item['productBrand'] = response.xpath("//ul[@class='list1 clf']/li[@class='itm'][%i]/span[@class='dd']/text()" %j).extract()[0].encode('utf-8').replace("\"","\'").strip() 
				if '型号' in model:
					item['productModel'] = response.xpath("//ul[@class='list1 clf']/li[@class='itm'][%i]/span[@class='dd']/text()" %j).extract()[0].encode('utf-8').replace("\"","\'").strip() 
		except:
			pass
		try:
			item['productClassification'] = classification
		except:
			pass
		try:
			price=response.xpath("//em[@class='prc']/b/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			if price == '':
				price = '0.0'
		except:
			pass
		try:
			item['productPrice'] = str(float(filter(lambda ch: ch in '0123456789.~', price))*100)
		except:
			pass
		try:
			item['productImagePath'] = "http:"+response.xpath("//li[@class='img-itm active']/div[@class='img-box']/img/@src").extract()[0].encode('utf-8').replace("\"","\'").strip() 
		except:
			pass
		item['productAddres'] = ""
		item['productCompany'] = ""
		names = self.name+'.json'
		item['fileName'] = names
		list_details = response.xpath("//ul[@class='list1 clf']/li[@class='itm']/span/text()").extract()
		logging.info("-------list_details_len=%i" %len(list_details))
		list_pack = response.xpath("//div[@class='packageParameter tabContent']/div[@class='specsParameter-wrap']/table[@class='standardTable']/tbody/tr[@class='keyValue']/td/text()").extract()
		intro = response.xpath("//span[@id='PDescriptiion']/text()").extract()
		logging.info("-------intr_len=%i" %len(intro))
		speci = response.xpath("//span[@id='techParam']/text()").extract()
		logging.info("-------intr_len=%i" %len(speci))
		num_one=1
		for value_details in list_details :
			value_details = value_details.encode('utf-8').replace(":","").replace("\n","").replace("\"","").strip()
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

		product_details = response.xpath("//div[@class='pro-main']/div[@class='con'][1]/text()").extract()
		filename = self.name+".txt"
		file = open("data/"+filename, 'a+')
		file.write("\n"+"productUrl:"+response.url+"\n")
		file.write("productDetails:"+"\n")
		for details in product_details:
			details = details.encode('utf-8').replace("\b","").replace("<br/>","").replace("<br>","").strip()
			file.write(details+"\n")
		file.close()

		item['productSpeci'] = speci_list
		item['productPack'] = pack_list
		item['productIntro'] = intro_list
		item['productDetails'] = details_list
		yield item


