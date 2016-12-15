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
	name = "spider_huaaomro_redis"
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
			classification_one = response.xpath("//div[@class='siteUrl']/a[2]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			classification_two = response.xpath("//div[@class='siteUrl']/a[3]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			classification_three = response.xpath("//div[@class='siteUrl']/a[4]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		classification = classification_one + '|||' + classification_two + '|||' + classification_three
		print "PhantomJS is starting1..."
		driver = webdriver.PhantomJS()
		driver.get(response.url)
		#time.sleep(3)
		body = driver.page_source
		#driver.close()
		HtmlResponses = HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=response)
		try:
			item['productUrl'] = response.url
		except:
			pass
		try:
			item['productName'] = response.xpath("//div[@class='hd']/div/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			item['productBrand'] = response.xpath("//div[@class='dd']/em/a/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			item['productModel'] = response.xpath("//form[@id='ECS_FORMBUY']/div[@class='proInfo f_R']/div[@class='bd']/ul/li[2]/div[@class='dd']/em/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			item['productClassification'] = classification
		except:
			pass
		try:
		#去空格 转分   去人民币符号
			item['productPrice'] = HtmlResponses.xpath("//b[@id='ECS_GOODS_AMOUNT']/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			item['productPrice'] = str(float(filter(lambda ch: ch in '0123456789.~', item['productPrice']))*100)
		except:
			pass
		#图片连接
		try:
			item['productImagePath'] = "http://www.huaaomro.com/" + HtmlResponses.xpath('//div[@class="proSide f_L"]/div[@class="bd"]/img[@id="idImage2"]/@src').extract()[0].encode('utf-8').replace("\"","\'").strip()
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
		list_intro = response.xpath("//ul[@class='detail-list clearfix']/li/text()").extract()
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

		for list_intro_value in list_intro:
			list_intro_value = list_intro_value.encode('utf-8').replace("\n","").strip()
			intro = list_intro_value.split('：')
			data2 = {}
			data2['attrkey'] = ''
			data2['keyname'] = ''
			if '商品品牌' in intro[0]:
				continue
			if '商品型号' in intro[0]:
				continue
			if '商品名称' in intro[0]:
				continue
			data2['attrkey']=intro[0]
			data2['keyname']=intro[1]
			intro_list.append(data2)

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
