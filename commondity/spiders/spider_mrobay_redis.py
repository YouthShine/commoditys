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
import sys 
reload(sys) 
sys.setdefaultencoding('utf-8')


#Crawling logic
class MrobaySpider(scrapy.Spider):

	#Reptile name (unique)
	name = 'spider_mrobay_redis'

	#Get Url object
	url = GetUrls()
	#Start path (crawler entry)
	start_urls=url.getUrls(name)
	#start_urls=["http://zc.mrobay.com/xianhuo/pick/show/1-GP0000764550.do"]

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
		temps=""
		productDetails=""
		productPack=""
		fileName="zc_mrobay_com_data_info.json"
		#Instantiation CrawlertoolsItem object
		item=BaseItem()
		#Parse text
		productImagePath=sel.xpath(".//*[@id='showPic']/@src").extract()[0]
		try:
			tempSel=sel.xpath(".//div[@class='Xh_xq']")
			productName=tempSel.xpath("h1/text()").extract()[0]
			productBrand=tempSel.xpath("div[2]/div[2]/ul/li[3]/text()").extract()[0]
			temps=tempSel.xpath("div[2]/div[2]/ul/li[1]/span/b/text()")[0].extract()
			productPrice=str(float(filter(lambda ch: ch in '0123456789.~', temps))*100)
			productCompany=u"套"				
			productModel=tempSel.xpath("div[2]/div[2]/ul/li[4]/p[1]/text()")[0].extract()
		except Exception,e:
			print "-----------------yichang--------------->",e
		
		try:
			productPack=sel.xpath(".//div[5]/div/div[2]/div[2]/ul/li[9]/text()").extract()[0]
			productPack=productPack.strip()
		except Exception,e:
			print e
		
		try:
			tempSel=sel.xpath(".//div[5]/div/div[2]/div[2]/ul/li[4]/p")
			j=0
			details=[]
			while j < len(tempSel):
				name=tempSel[j].xpath("span/text()").extract()[0].strip().encode('utf-8')
				value=tempSel[j].xpath("text()").extract()[0].strip().encode('utf-8')
				strd={name:value}
				details.append(strd)
				j+=1
		except Exception,e:
			print e	

		#Formatted data
		item['productUrl']=response.url
		item['productImagePath'] = productImagePath.encode('utf-8').replace("\"","\'").strip() 
		item['productName'] =productName.replace("\"","\'").replace("\t","").replace(" ","").replace("\r\n","").strip()
		item['productBrand'] =productBrand.replace("\"","\'").strip()
		item['productModel'] =productModel.replace("\"","\'").strip()
		item['productCompany'] =productCompany.replace("\"","\'").strip()
		item['productPrice'] =productPrice.replace("\"","\'").strip()
		item['fileName']=fileName
		item['productClassification']=""
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
		item['productDetails']=details
		item['productPack']=productPack.encode('utf-8').replace("\"","\'").strip()
		item['productIntro']=""
		item['productSpeci']=""
<<<<<<< HEAD
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
		yield item