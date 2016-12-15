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
	name = "spider_1ez_redis"  
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
			item['productName'] = response.xpath("//div[@class='center_title']/a/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			item['productBrand'] = response.xpath("//form[@id='ECS_FORMBUY_P']/div[@class='detail_center']/div[@class='center_txt']/div[@class='center_text']/p[1]/a/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			item['productModel'] = response.xpath('//div[@class="m m1"]/div/ul/dt/li/text()').extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			classification_one = response.xpath("//div[@class='location']/a[2]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			classification_two = response.xpath("//div[@class='location']/a[3]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			classification_three = response.xpath("//div[@class='location']/a[4]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		classification = classification_one + '|||' + classification_two + '|||' + classification_three
		item['productClassification'] = classification
		try:
			item['productPrice'] = response.xpath("//div[@class='center_text']/ul[@class='tm-fcs-panel']/li[1]/span[@id='ECS_GOODS_AMOUNT']/span/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			item['productPrice'] = str(float(filter(lambda ch: ch in '0123456789.~', item['productPrice']))*100)
		except:
			pass
		try:
			item['productImagePath'] = "http://www.1ez.com.cn/"+response.xpath('//img[@id="J_prodImg"]/@src').extract()[0].encode('utf-8').replace("\"","\'").strip()
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
		list_details = response.xpath("//ul[@class='inLeft_attributes']/li/text()").extract()
		details = response.xpath("//ul[@class='inLeft_attributes']/li/span/text()").extract()
		logging.info("-------list_details_len=%i" %len(list_details))
		logging.info("-------details_len=%i" %len(details))
		list_pack = response.xpath("//div[@class='packageParameter tabContent']/div[@class='specsParameter-wrap']/table[@class='standardTable']/tbody/tr[@class='keyValue']/td/text()").extract()
		intro = response.xpath("//span[@id='PDescription']/text()").extract()
		logging.info("-------intr_len=%i" %len(intro))
		speci = response.xpath("//span[@id='techParam']/text()").extract()
		logging.info("-------intr_len=%i" %len(speci))
		num_one=0
		value_details = ''
		for j in range(1,len(list_details)):
			try:
				value_details = response.xpath("//ul[@class='inLeft_attributes']/li[%i]/text()" %j).extract()[0].encode('utf-8').replace(":","").replace("\"","").replace("：","").strip()
			except:
				break
			if '品牌' in value_details:
				num_one+=1
				continue
			if '商品名称' in value_details:
				num_one+=1
				continue
			if '型号' in value_details:
				num_one+=1
				continue
			else:
				data2 = {}
				data2['attrkey'] = ''
				data2['keyname'] = ''
				data2['attrkey']=value_details
				data2['keyname']=details[num_one]
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

		item['productSpeci'] = speci_list
		item['productPack'] = pack_list
		item['productIntro'] = intro_list
		item['productDetails'] = details_list
		yield item


 