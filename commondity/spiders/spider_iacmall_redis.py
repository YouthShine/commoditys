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

class IacmallRedis(scrapy.Spider):
	name = "spider_iacmall_redis"  
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
			item['productUrl'] = response.url
		except:
			pass
		try:
			item['productName'] = response.xpath("//h1[@class='prodbaseinfo_title']/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()+"eoriutqirwe"
		except:
			pass
		try:
			item['productBrand'] = response.xpath("//ul[@class='ul_list']/li[@class='fg14'][1]/div[1]/a/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			item['productModel'] = response.xpath("//ul[@class='ul_list']/li[@class='fg14'][2]/p/font/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			classification_one = response.xpath("//div[@class='location']/a[2]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			classification_two = response.xpath("//div[@class='location']/a[3]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			classification_three = response.xpath("//div[@class='location']/a[4]/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
			item['productClassification'] = classification_one + '|||' + classification_two + '|||' +classification_three
		except:
			pass
		try:
			item['productPrice'] = response.xpath("//ul[@class='ul_list']/li[@class='fg14'][3]/p/span[@id='attr_price']/text()").extract()[0].encode('utf-8').replace("\"","\'").strip()
		except:
			pass
		try:
			item['productPrice'] = str(float(filter(lambda ch: ch in '0123456789.~', item['productPrice']))*100)
		except:
			pass
		try:
			item['productImagePath'] = response.xpath('//div[@id="wrap"]/a/@href').extract()[0].encode('utf-8').replace("\"","\'").strip()
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
		list_details = response.xpath("//div[@id='para']/table[1]/tbody[2]/tr/td/text()").extract()
		logging.info("-------list_details_len=%i" %len(list_details))
		list_pack = response.xpath("//div[@class='packageParameter tabContent']/div[@class='specsParameter-wrap']/table[@class='standardTable']/tbody/tr[@class='keyValue']/td/text()").extract()
		intro = []
		try:
			intro_p = response.xpath("//li[@class='pb10p']/blockquote/table[2]/tbody/tr/td/p/text()").extract()
			logging.info("-------intro_p_len=%i" %len(intro_p))
			intro = response.xpath("//li[@class='pb10pppp']/blockquote/table[2]/tbody/tr/td/text()").extract()
			logging.info("-------intro_len=%i" %len(intro))
		except:
			pass
		speci = []
		try:
			speci_p = response.xpath("//li[@class='pb10p']/blockquote/table[2]/td/p/text()").extract()
			logging.info("-------speci_p_len=%i" %len(speci_p))
			speci = response.xpath("//li[@class='pb10pppp']/blockquote/table[2]/tbody/text()").extract()
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

		num_two=1
		for list_intro in intro:
			list_intro = list_intro.encode('utf-8').replace("\n","").replace(":","").strip()
			if num_two%2==1:
				data2 = {}
				data2['attrkey'] = ''
				data2['keyname'] = ''
				if '型号' in list_intro:
					num_two +=1
					continue
				data2['attrkey']=list_intro
			else:
				if num_two == 3:
					num_two +=1
					continue
				data2['keyname']=list_intro
				if num_two == 4:
					num_two =6
					continue
				intro_list.append(data2)
			num_two +=1


		num_three=1
		for list_speci in speci:
			list_speci = list_speci.encode('utf-8').replace("\n","").replace("\"","").strip()
			if num_three%2==1 :
				data2 = {}
				data2['attrkey'] = ''
				data2['keyname'] = ''
				if '商品名称' in list_speci:
					break
				if '品牌' in list_speci:
					break
				data2['attrkey']=list_speci
			else:
				data2['keyname']=list_speci
				speci_list.append(data2)
			num_three+=1

		intro_file = response.xpath("//li[@class='pb10p']/blockquote/table[2]/tbody/tr/td/text()").extract()
		filename = self.name+".txt"
		file = open("data/"+filename, 'a+')
		file.write("\n"+"productUrl:"+response.url+"\n")
		file.write("\n"+"productIntro:"+"\n")
		for list_intro in intro_file:
			list_intro = list_intro.encode('utf-8').replace("\n","").replace(":","").strip()
			file.write(list_intro+"\n")
		file.close()

		item['productSpeci'] = speci_list
		item['productPack'] = pack_list
		item['productIntro'] = intro_list
		item['productDetails'] = details_list
		yield item


