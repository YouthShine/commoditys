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
class WangshanggouSpider(scrapy.Spider):

	#Reptile name (unique)
	name = 'spider_wangshanggou_redis'

	#Get Url object
	url = GetUrls()
	#Start path (crawler entry)
	start_urls=url.getUrls(name)
	#start_urls=["http://www.4006770558.com/index.php?app=goods&id=1297"]

	def __init__(self):
		log.init_log(settings.get('LOG_DIR'))

	#Analysis of the specific content of the web page
	def parse(self,response):
		#Analytical framework
		sel = Selector(response)
		modelList=sel.xpath(".//tbody[@id='specs_tbody']/tr")
		j=0

		while j<len(modelList):
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
			productClassification=""
			productName=""
			productBrand=""
			productModel=""
			productPrice=""
			productImagePath=""
			productAddres=""
			productId=""
			productCompany=""
			price=""
			#Instantiation CrawlertoolsItem object
			item=BaseItem()
			#Parse text
			
			productImagePath=sel.xpath(".//div[@class='ware_pic']/div[@class='big_pic']/a/span/img/@src").extract()[0]
			
			try:
				prodecAddress=sel.xpath(".//*[@id='right']/div[1]/div[2]/div/text()").extract()[8]
				prodecAddress=prodecAddress.replace("\t"," ").strip()
			except Exception,e:
				print e

			try:
				tempSel=sel.xpath(".//div[@id='left']/div[1]/div[1]/h2/text()")[0].extract().split("-")
				i=1
				classificationStr=""
				while i < len(tempSel):
					classificationStr=classificationStr+tempSel[i].strip()+"|||"
					i+=1
				productClassification=classificationStr.rstrip("|||")
			except :
				pass

			try:
				
				productName=sel.xpath(".//div[@class='ware_text']/h2/text()").extract()[0]
				productBrand=sel.xpath(".//div[@class='rate']/a/text()").extract()[0]
			except :
				pass

			try:
				productModel=modelList[j].xpath("./td[2]/text()")[0].extract()
				productCompany=modelList[j].xpath("./td[6]/text()")[0].extract()	
				prices=filter(lambda ch: ch in '0123456789.',modelList[j].xpath("./td[7]/text()")[0].extract())
				if  productCompany.encode('utf-8').replace("\"","\'").strip() == u"另询价".encode('utf-8'):
					productCompany=modelList[j].xpath("./td[5]/text()")[0].extract()	
					prices=filter(lambda ch: ch in '0123456789.',modelList[j].xpath("./td[6]/text()")[0].extract())
				
				
				if prices != "":
					productPrice=str(float(prices)*100)
			except :
				pass
				#productCompany=modelList[j].xpath("./td[5]/text()")[0].extract()				
				#productModel=modelList[j].xpath("./td[2]/text()")[0].extract()
			#Formatted data
			item['productUrl']=response.url
			item['productImagePath'] = "http://www.4006770558.com/"+productImagePath.encode('utf-8').replace("\"","\'").strip() 
			item['productClassification'] =productClassification.encode('utf-8').replace("\"","\'").strip()
			item['productName'] =productName.encode('utf-8').replace("\"","\'").strip()
			item['productBrand'] =productBrand.encode('utf-8').replace("\"","\'").strip()
			item['productModel'] =productModel.encode('utf-8').replace("\"","\'").strip()
			item['productCompany'] =productCompany.encode('utf-8').replace("\"","\'").strip()
			item['productPrice'] =productPrice.encode('utf-8').replace("\"","\'").strip()
			item['productAddres']=prodecAddress.encode('utf-8').replace("\"","\'").strip()
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
			j+=1