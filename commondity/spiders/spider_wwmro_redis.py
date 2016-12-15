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
	name = "spider_wwmro_redis"
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
		details_list = []
		pack_list = []
		intro_list = []
		speci_list = []
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
			classification_one = response.xpath("//div[@class='breadcrumbs']/a[3]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			classification_two = response.xpath("//div[@class='breadcrumbs']/a[4]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			classification_three = response.xpath("//div[@class='breadcrumbs']/a[5]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		classification = classification_one + '|||' + classification_two + '|||' +classification_three
		try:
			item['productUrl'] = response.url
		except:
			pass
		try:
			item['productName'] = response.xpath('//div[@class="tl-wrap-g"]/div[@class = "title"]/h3/b/text()').extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
<<<<<<< HEAD
<<<<<<< HEAD
		#11.28
		brand = ''
		try:
			list_brand = response.xpath("//table[@class='nc-goods-sort-table']/tbody/tr/th/text()").extract()
			for j in range(1,len(list_brand)):
				num = 0
				knum = 0 
				brand_l = response.xpath("//table[@class='nc-goods-sort-table']/tbody/tr[%i]/th/text()" %j).extract()
				for brand_tr in brand_l:
					knum += 1
					brand_tr = brand_tr.encode('utf-8').replace("\"","\'").strip()
					if '品牌'  in brand_tr:
						num = j
						brand= response.xpath("//table[@class='nc-goods-sort-table']/tbody/tr[%i]/td[%i]/text()" %(num,knum)).extract()[0].encode('utf-8').replace("\"","\'").strip()
						item['productBrand'] = brand
						break
					else:
						continue
				break
		except Exception,e:
			print e
			print "1有数组越界"
		if item['productBrand'] == '':
			try:
				brand= response.xpath("//form[@id='ECS_FORMBUY']/ul[@class='ul1']/li[@class='clearfix'][4]/dd/a/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
				item['productBrand'] = brand
			except Exception,e:
				print e
				print "2越界"
			if item['productBrand'] =='': 
				try:
					item['productBrand'] = response.xpath("//div[@class='tl-left']/b/a/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
				except:
					pass
		model = ''
		try:
			list_model = response.xpath("//table[@class='nc-goods-sort-table']/tbody/tr/th/text()").extract()
			for j in range(1,len(list_model)):
				num = 0
				knum = 0 
				model_l = response.xpath("//table[@class='nc-goods-sort-table']/tbody/tr[%i]/th/text()" %j).extract()
				for model_tr in model_l:
					knum += 1
					model_tr = model_tr.encode('utf-8').replace("\"","\'").strip()
					if '型号'  in model_tr:
						num = j
						model= response.xpath("//table[@class='nc-goods-sort-table']/tbody/tr[%i]/td[%i]/text()" %(num,knum)).extract()[0].encode('utf-8').replace("\"","\'").strip()
						item['productModel'] = model
						break
					else:
						continue
				break
		except Exception,e:
			print e
			print "1有数组越界"
		#11.28
=======
=======
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
		try:
			item['productBrand'] = response.xpath("//table[@class='content']/tbody/tr[@class='tl-tbody-tr'][1]/td[3]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			item['productModel'] = response.xpath("//table[@class='content']/tbody/tr[@class='tl-tbody-tr'][1]/td[4]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
<<<<<<< HEAD
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
		try:
			item['productClassification'] = classification
		except:
			pass
		try:
		#去空格 转分   去人民币符号
			item['productPrice'] = response.xpath('//dl[@class="tl_dl nc-detail-price"]/dd/strong/text()').extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			item['productPrice'] = str(float(filter(lambda ch: ch in '0123456789.~', item['productPrice']))*100)
		except:
			pass
		#图片连接
		try:
			item['productImagePath'] = response.xpath('//nav[@class="zoom-desc"]/ul/li[1]/a/@href').extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		#print item['image_urls'],"777777"
		try:
			item['productAddres'] = response.xpath("//form[@id='form1']/ul/li[4]/text()").extract()[0]
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
		intro_two = response.xpath("//table[@class='nc-goods-sort-table']/tbody/tr/td/text()").extract()
		intro_one = response.xpath("//table[@class='nc-goods-sort-table']/tbody/tr/th/text()").extract()
		logging.info("-------intro_len=%i" %len(intro_one))
		speci = []
		try:
			speci = response.xpath("//div[@class='param-defaul']/text()").extract()
			logging.info("-------speci_len=%i" %len(speci))
		except:
			pass
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

		num_two=0
		for list_intro in intro_one:
			list_intro = list_intro.encode('utf-8').replace("\n","").replace(":","").strip()
			data2 = {}
			data2['attrkey'] = ''
			data2['keyname'] = ''
			if '型号' in list_intro:
				num_two +=1
				continue
			if '品牌' in list_intro:
				num_two +=1
				continue
			if ' ' in list_intro:
				num_two +=1
				break
			data2['attrkey']=list_intro
			try:
				data2['keyname']=intro_two[num_two].encode('utf-8').replace("\n","").replace(":","").strip()
			except:
				pass
			intro_list.append(data2)
			num_two +=1


		num_three=1
		for list_speci in speci:
			list_speci = list_speci.encode('utf-8').replace("\n","").replace("\"","").strip()
			list_speci = list_speci.split(' ')
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


