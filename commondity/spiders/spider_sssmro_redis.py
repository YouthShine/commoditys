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

class LezSpider(scrapy.Spider):
	name = "spider_sssmro_redis"  
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
			item['productName'] = response.xpath("//form[@id='ECS_FORMBUY']/ul/li[1]/dd/div/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			item['productBrand'] = response.xpath("//ul[@class='ul1']/li[@class='clearfix'][2]/dd/div[@class='f_r goos_news']/a/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			item['productModel'] = response.xpath("//ul[@class='ul1']/li[@class='clearfix'][3]/dd/div[@class='f_l']/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			classification_one = response.xpath("//div[@id='ur_here']/a[2]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			classification_two = response.xpath("//div[@id='ur_here']/a[3]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			classification_three = response.xpath("//div[@id='ur_here']/a[4]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			item['productClassification'] = classification_one + '|||' + classification_two + '|||' +classification_three
		except:
			pass
		try:
			item['productPrice'] = response.xpath("//font[@id='ECS_SHOPPRICE']/text()").extract()[1].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			item['productPrice'] = str(float(filter(lambda ch: ch in '0123456789.~', item['productPrice']))*100)
		except:
			pass
		#Í¼Æ¬Á¬½Ó
		try:
			item['productImagePath'] = "http://www.sssmro.com/"+response.xpath('//div[@id="preview"]/div[@class="jqzoom"]/img/@src').extract()[0].encode('utf-8').replace("\"","\'").strip()
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
		test_specis = response.xpath("//div[@id='main1']/blockquote[2]/div[@class='qyjstxt']/text()").extract()
		logging.info("-------specis_len=%i" %len(test_specis))
		test_details = response.xpath("//blockquote[@class='block']/div[@class='qyjstxt']/text()").extract()
		logging.info("-------details_len=%i" %len(test_details))
		specis = ''
		try:
			specis = response.xpath("//div[@id='main1']/blockquote[2]/div[@class='qyjst']/text()").extract()[0].encode('utf-8').replace("\n","").replace("\"","").strip()
		except:
			pass
		list_speci = specis.split('£º')
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


		product_intro = response.xpath("//div[@class='formwork_bt'][1]/p/text()").extract()
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