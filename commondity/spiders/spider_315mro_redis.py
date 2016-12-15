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



#Crawling logic
class MroSpider(scrapy.Spider):

	#Reptile name (unique)
	name = 'spider_315mro_redis'

	#Get Url object
	url = GetUrls()
	#Start path (crawler entry)
<<<<<<< HEAD
<<<<<<< HEAD
	start_urls=['http://www.315mro.com/Product/P16684.html']
=======
	start_urls=url.getUrls(name)
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
	start_urls=url.getUrls(name)
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
	#start_urls=["http://www.315mro.com/product/p54735.html"]

	def __init__(self):
		log.init_log(settings.get('LOG_DIR'))

	#Analysis of the specific content of the web page
	def parse(self,response):
		#Analytical framework
		sel = Selector(response)
		#Loop body
<<<<<<< HEAD
<<<<<<< HEAD
		speci_list = []
		pack_list = []
		intro_list = []
		details_list = []
=======
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
		productName=""
		productBrand=""
		productModel=""
		productPrice=""
		productImagePath=""
		productId=""
		productCompany=""
		productAddres=""
		productPack=""
		temps=""
		fileName="www_315mro_com_data_info.json"
		#Instantiation CrawlertoolsItem object
		item=BaseItem()
		#Parse text
		productImagePath=sel.xpath(".//div[@class='img_show']/div[1]/span/img/@src").extract()[0]
		try:
			tempSel=sel.xpath(".//div[@class='buy_right']/div[1]")
			productName=tempSel.xpath("p[3]/label/text()").extract()[0]
			productBrand=tempSel.xpath("p[1]/text()").extract()[0]
			productModel=tempSel.xpath("p[2]/text()")[0].extract()
			productCompany=tempSel.xpath("p[4]/text()")[0].extract()
			temps=sel.xpath(".//div[@class='buy_right']/div[2]/div[1]/p/span/text()").extract()[0].strip()
			productPrice=str(float(filter(lambda ch: ch in '0123456789.~', temps))*100)
		except Exception,e:
			print "-----------------yichang--------------->",e

		#Formatted data
		item['productUrl']=response.url
<<<<<<< HEAD
<<<<<<< HEAD
		item['productImagePath'] = productImagePath.encode('utf-8').replace("\"","\'").strip()
=======
		item['productImagePath'] = productImagePath.encode('utf-8').replace("\"","\'").strip() 
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
		item['productImagePath'] = productImagePath.encode('utf-8').replace("\"","\'").strip() 
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
		item['productName'] =productName.encode('utf-8').replace("\"","\'").replace("\r\n","").strip()
		item['productBrand'] =productBrand.encode('utf-8').replace("\"","\'").strip()
		item['productModel'] =productModel.encode('utf-8').replace("\"","\'").strip()
		item['productCompany'] =productCompany.encode('utf-8').replace("\"","\'").strip()
		item['productPrice'] =productPrice.encode('utf-8').replace("\"","\'").strip()
		item['productClassification'] =""
		item['fileName']=fileName
		item['productAddres']=""
<<<<<<< HEAD
<<<<<<< HEAD
		item['productDetails']=details_list
		item['productPack']=pack_list
		item['productIntro']=intro_list
		item['productSpeci']=speci_list
=======
=======
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
		item['productDetails']=""
		item['productPack']=""
		item['productIntro']=""
		item['productSpeci']=""
<<<<<<< HEAD
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
		yield item