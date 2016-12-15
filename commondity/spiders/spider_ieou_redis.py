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
	name = "spider_ieou_redis"
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
			classification_one = response.xpath("//div[@id='Public_breadCrumb01-110']/a[@class='arrowbg1']/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			classification_two = response.xpath("//div[@id='Public_breadCrumb01-110']/a[@class='arrowbg2']/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			classification_three = response.xpath("//div[@id='Public_breadCrumb01-110']/a[@class='arrowbg3']/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		classification = classification_one + '|||' + classification_two + '|||' +classification_three
		try:
			item['productUrl'] = response.url
		except:
			pass
		try:
			item['productName'] = response.xpath("//div[@id='ProductDetail_basic01-101']/h1[@class='htmlinline']/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			item['productBrand'] = response.xpath('//ul[@class="list_pic"]/li/dl/dt/a/text()').extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			item['productModel'] = response.xpath("//li[@class='number']/em/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			item['productClassification'] = classification
		except:
			pass
		try:
		#去空格 转分   去人民币符号
			item['productPrice'] = response.xpath("//li[@class='retailprice']/em/strong").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			item['productPrice'] = str(float(filter(lambda ch: ch in '0123456789.~', item['productPrice']))*100)
		except:
			pass
		#图片连接
		try:
			item['productImagePath'] = "http://www.ieou.com.cn" + response.xpath('//div[@class="jqzoom"]/img/@src').extract()[0].encode('utf-8').replace("\"","\'").strip()
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
		list_details = response.xpath("//div[@class='extend']/ul/li/label/text()").extract()
		logging.info("-------list_details_len=%i" %len(list_details))
		details = response.xpath("//div[@class='extend']/ul/li/span/text()").extract()
		logging.info("-------details_len=%i" %len(details))
		list_pack = response.xpath("//div[@class='packageParameter tabContent']/div[@class='specsParameter-wrap']/table[@class='standardTable']/tbody/tr[@class='keyValue']/td/text()").extract()
		intro = response.xpath("//div[@class='descreibe htmledit']/ul/li/span/span/text()").extract()
		logging.info("-------intr_len=%i" %len(intro))
		speci = response.xpath("//div[@class='desceribe htmleit']/ul/li/span/span/span/text()").extract()
		logging.info("-------intr_len=%i" %len(speci))
		num_one=0
		for value_details in list_details :
			value_details = value_details.encode('utf-8').replace(":","").replace("\n","").replace("\"","").strip()
			data2 = {}
			data2['attrkey'] = ''
			data2['keyname'] = ''
			if '品牌' in value_details:
				num_one+=1
				continue
			if '型号' in value_details:
				num_one+=1
				continue
			data2['attrkey']=value_details
			data2['keyname']=details[num_one].encode('utf-8').replace(":","").replace("\n","").replace("\"","").strip()
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

		product_intro = response.xpath("//div[@class='describe htmledit']/ul/li/span/span/text()").extract()
		product_details = response.xpath("//div[@class='describe htmledit']/p/span/text()").extract()
		product_speci = response.xpath("//div[@class='describe htmledit']/p/span/strong/text()").extract()
		if len(product_speci) ==0:
			product_speci = response.xpath("//div[@class='describe htmledit']/p/strong/span/text()").extract()
		product_pack = response.xpath("//td[@id='imgDiv']/div[@id='div3']/font/b/text()").extract()
		filename = self.name+".txt"
		file = open("data/"+filename, 'a+')
		file.write("\n"+"productUrl:"+response.url+"\n")
		file.write("productIntro:"+"\n")
		for intro in product_intro:
			intro = intro.encode('utf-8').replace("\b","").replace("<br/>","").replace("<br>","").strip()
			file.write(intro+"\n")
		file.write("productDetails:"+"\n")
		for details in product_details:
			details = details.encode('utf-8').replace("\"","").strip()
			file.write(details+"\n")
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