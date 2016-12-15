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

class LezSpider(scrapy.Spider):
	name = "spider_grainger_redis"
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
			item['productName'] = response.xpath("//div[@id='name']/h1/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			item['productBrand'] = response.xpath("//li[@id='summary-brand']/div[@class='dd']/a/em[@class='hl_red bold']/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			item['productModel'] = response.xpath('//div[@class="m m1"]/div/ul/dt/li/text()').extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			classification_one = response.xpath("//div[@id='part_content']/div[@class='node_path']/a[3]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			classification_two = response.xpath("//div[@id='part_content']/div[@class='node_path']/a[4]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			classification_three = response.xpath("//div[@id='part_content']/div[@class='node_path']/a[5]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		classification = classification_one + '|||' + classification_two + '|||' +classification_three
		item['productClassification'] = classification
		try:
		#去空格 转分   去人民币符号
			item['productPrice'] = response.xpath("//li[@id='summary-price']/div[@class='dd']/strong/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			item['productPrice'] = str(float(filter(lambda ch: ch in '0123456789.~', item['productPrice']))*100)
		except:
			pass
		#图片连接
		try:
			item['productImagePath'] = response.xpath('//div[@id="spec-n1"]/a/@href').extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		#print item['image_urls'],"777777"
		try:
			item['productAddres'] = response.xpath("//div[@class='goods_content_a_l_r f_l']/div[@class='score'][1]/span[@class='brand']/text()").extract()[0]
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
		test_specis = response.xpath("//div[@id='main1']/blockquote[2]/div[@class='qyjstxt']/text()").extract()
		logging.info("-------specis_len=%i" %len(test_specis))
		test_details = response.xpath("//blockquote[@class='block']/div[@class='qyjstxt']/text()").extract()
		logging.info("-------details_len=%i" %len(test_details))
		specis = ''
		try:
			specis = response.xpath("//div[@id='main1']/blockquote[2]/div[@class='qyjst']/text()").extract()[0].encode('utf-8').replace("\n","").replace("\"","").strip()
		except:
			pass
		list_speci = specis.split('：')
		list_pack = response.xpath("//div[@class='packageParameter tabContent']/div[@class='specisParameter-wrap']/table[@class='standardTable']/tbody/tr[@class='keyValue']/td/text()").extract()
		num_one=1
		for speci in list_speci :
			if num_one%2==0 :
				data2 = {}
				data2['attrkey'] = ''
				data2['keyname'] = ''
				data2['attrkey'] = speci
			else:
				if num_one == 1:
					num_one+=1
					continue
				data2['keyname'] = speci
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

		product_intro = response.xpath("//div[@id='content_product']/div[@class='property']/text()").extract()
		filename = self.name+".txt"
		file = open("data/"+filename, 'a+')
		file.write("\n"+"productUrl:"+response.url+"\n")
		file.write("productIntro:"+"\n")
		for intro in product_intro:
			intro = intro.encode('utf-8').replace("\"","").strip()
			file.write(intro+"\n")
		file.close()

		item['productSpeci'] = speci_list
		item['productPack'] = pack_list
		item['productIntro'] = intro_list
		item['productDetails'] = intro_list
		yield item