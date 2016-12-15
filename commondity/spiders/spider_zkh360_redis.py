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
#Crawling logic
class ZkhSpider(scrapy.Spider):

	#Reptile name (unique)
	name = 'spider_zkh360_redis'

	#Get Url object
	url = GetUrls()

	#Start path (crawler entry)
	start_urls=url.getUrls(name)
	#start_urls=["http://www.zkh360.com/zkh_product_group/100083138.html","http://www.zkh360.com/zkh_product_group/34292760.html"]

	def __init__(self):
		log.init_log(settings.get('LOG_DIR'))

	#Analysis of the specific content of the web page
	def parse(self,response):
		#Analytical framework
		driver = webdriver.PhantomJS()
		#driver = webdriver.Chrome()
		driver.get(response.url)
		time.sleep(1)

		body = driver.page_source
		# driver.close()
		#sel = HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=response)
		sel = HtmlResponse(response.url, body=body, encoding='utf-8', request=response)
		modelList=sel.xpath(".//table[@id='tblPrice']/tbody/tr")
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
			productDetails=""
			productPack=""
			productIntro=""
			productSpeci=""
			#Instantiation CrawlertoolsItem object
			item=BaseItem()
			#Parse text
			
			productImagePath=sel.xpath(".//img[@id='current_img']/@src").extract()[0]
			

			try:
				tempSel=sel.xpath(".//div[@class='clearfix inner']/div[1]/a/text()").extract()
				i=0
				classificationStr=""
				while i < len(tempSel):
					classificationStr=classificationStr+tempSel[i].strip()+"|||"
					i+=1
				productClassification=classificationStr.rstrip("|||")
			except :
				pass

			try:
				
				productName=sel.xpath(".//div[@class='proview_name']/h1/text()").extract()[0]
				productBrand=sel.xpath(".//div[@class='proview_canshu']/li/text()").extract()[0]
			except :
				pass

			try:
				productModel=modelList[j].xpath("./td[2]/a/text()")[0].extract()
				productCompany=modelList[j].xpath("./td[5]/text()")[0].extract()	
				prices=filter(lambda ch: ch in '0123456789.',modelList[j].xpath("./td[6]/text()")[0].extract())
				if prices != "":
					productPrice=str(float(prices)*100)
			except :
				pass
				#productCompany=modelList[j].xpath("./td[5]/text()")[0].extract()				
				#productModel=modelList[j].xpath("./td[2]/text()")[0].extract()
			try:
				productIntro=sel.xpath(".//div[5]/div[4]/div[5]/div[1]/div[1]/text()").extract()[0]
				productIntro=productIntro.strip().replace("\n","").replace("\t"," ").replace("\\","").replace(" ","")
			except Exception,e:
				print e
			#Formatted data
			item['productUrl']=response.url
			item['productImagePath'] = "http://www.zkh360.com"+productImagePath.encode('utf-8').replace("\"","\'").strip() 
			item['productClassification'] =productClassification.encode('utf-8').replace("\"","\'").strip()
			item['productName'] =productName.encode('utf-8').replace("\"","\'").strip()
			item['productBrand'] =productBrand.encode('utf-8').replace("\"","\'").strip()
			item['productModel'] =productModel.encode('utf-8').replace("\"","\'").strip()
			item['productCompany'] =productCompany.encode('utf-8').replace("\"","\'").strip()
			item['productPrice'] =productPrice.encode('utf-8').replace("\"","\'").strip()
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
			item['productIntro']=productIntro.encode('utf-8').replace("\"","\'").strip()
			item['productSpeci']=""
<<<<<<< HEAD
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
			yield item
			j+=1
