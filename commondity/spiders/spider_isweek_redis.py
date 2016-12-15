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
	name = "spider_isweek_redis"
	url = GetUrls()
	start_urls = url.getUrls(name)

	def __init__(self):
		log.init_log(settings.get('LOG_DIR'))
		logging.info("spider start......")
		print "spider start......"
<<<<<<< HEAD
<<<<<<< HEAD
=======
		print "......"+self.name+" members is "+self.url_members
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
		print "......"+self.name+" members is "+self.url_members
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
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
			classification_one = response.xpath("//div[@class='w-fly-cnt']/div[@class='position']/a[2]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			classification_two = response.xpath("//div[@class='w-fly-cnt']/div[@class='position']/a[3]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			classification_three = response.xpath("//div[@class='w-fly-cnt']/div[@class='position']/a[4]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		classification = classification_one + '|||' + classification_two + '|||' +classification_three
		item['productUrl'] = response.url
		try:
			item['productName'] = response.xpath("//div[@class='prodetails']/h1[@class='protitle']/text()").extract()[0].encode('utf-8').replace("\"","\'").strip() 
		except:
			pass
		try:
			item['productBrand'] = response.xpath('//ul[@class="list_pic"]/li/dl/dt/a/text()').extract()[0].encode('utf-8').replace("\"","\'").strip() 
		except:
			pass
		try:
			item['productModel'] = response.xpath("//div[@class='fn-fr']/div[@class='add-to-basket']/dl[@class='fn-clearfix atb-dl-01']/dd/text()").extract()[0].encode('utf-8').replace("\"","\'").strip() 
		except:
			pass
		try:
			item['productClassification'] = classification
		except:
			pass
		try:
			price=response.xpath("//font[@id='ECS_GOODS_AMOUNT']/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			item['productPrice'] = str(float(filter(lambda ch: ch in '0123456789.~', price))*100)
		except:
			pass
		try:
			item['productImagePath'] = "http://www.isweek.cn/"+response.xpath('//a[@class="jqzoom"]/img/@src').extract()[0].encode('utf-8').replace("\"","\'").strip() 
		except:
			pass
		item['productAddres'] = ""
		item['productCompany'] = ""
		names = self.name+'.json'
		item['fileName'] = names
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

		product_intro = response.xpath("//div[@class='prodesc']/p/span/text()").extract()
		product_pack = response.xpath("//td[@id='imgDiv']/div[@id='div3']/font/b/text()").extract()
		product_speci = response.xpath("//div[@class='fn-fr']/div[@class='info']/p/text()").extract()
		filename = self.name+".txt"
		file = open("data/"+filename, 'a+')
		file.write("\n"+"productUrl:"+response.url+"\n")
		file.write("productIntro:"+"\n")
		for intro in product_intro:
			intro = intro.encode('utf-8').replace("\b","").replace("<br/>","").replace("<br>","").strip()
			file.write(intro+"\n")
		file.write("productSpeci:"+"\n")
		for speci in product_speci:
			speci = speci.encode('utf-8').replace("\"","").strip()
			file.write(speci+"\n")
		file.close()

		item['productSpeci'] = speci_list
		item['productPack'] = pack_list
		item['productIntro'] = intro_list
		item['productDetails'] = details_list
		yield item


