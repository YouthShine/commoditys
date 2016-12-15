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
	name = "spider_zhaogongye_redis"  
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
			item['productName'] = response.xpath("//h1[@class='lh40 col59 f18']/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		list_brand = ''
		try:
			list_brand = response.xpath("//tr[@class='keyValue'][1]/td[1]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			if '涂层手套' not in list_brand:
				brand= response.xpath("//div[@class='detailAndBuy']/div[@class='detail'][1]/span[@class='typeValue']/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
				item['productBrand'] = brand.split(' ')[0]
			else:
				item['productBrand'] = response.xpath("//tr[@class='keyValue'][1]/td[2]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
				filter(str.isalnum,item['productBrand'])
		except:
			pass
		try:
			item['productModel'] = response.xpath("//div[@class='cpzstm']/b/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
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
			item['productPrice'] = response.xpath("//span[@id='show-price']/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			item['productPrice'] = str(float(filter(lambda ch: ch in '0123456789.~', item['productPrice']))*100)
		except:
			pass
		try:
			item['productImagePath'] = 'http://www.zhaogongye.cn'+response.xpath("//span[@class='jqzoom']/img/@src").extract()[0].encode('utf-8').replace("\"","\'").strip()
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

		product_details = response.xpath("//blockquote[@class='block']/div[@class='qyjstxt']/text()").extract()
		product_speci = response.xpath("//div[@id='main1']/blockquote[2]/div[@class='qyjstxt']/text()").extract()
		filename = self.name+".txt"
		file = open("data/"+filename, 'a+')
		file.write("\n"+"productUrl:"+response.url+"\n")
		file.write("productDetails:"+"\n")
		for details in product_details:
			details = details.encode('utf-8').replace("\b","").replace("<br/>","").replace("<br>","").strip()
			file.write(details+"\n")
		file.write("productSpeci:"+"\n")
		for speci in product_speci:
			speci = speci.encode('utf-8').replace("\"","").strip()
			file.write(speci+"\n")
		file.close()

		item['productSpeci'] = speci_list
		item['productPack'] = pack_list
		item['productIntro'] = intro_list
		item['productDetails'] = intro_list
		yield item