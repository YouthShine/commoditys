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

class IspekSpider(scrapy.Spider):
<<<<<<< HEAD
<<<<<<< HEAD
	name = "spider_ispek_redis"
	url = GetUrls()
	start_urls = url.getUrls(name)
	#start_urls=["http://www.ispek.cn/item/93418.html"]
	def __init__(self):
		log.init_log(settings.get('LOG_DIR'))

	#Details page
	def parse(self, response):
		#Analytical framework
		sel = Selector(response)
		#Loop body
		speci_list = []
		pack_list = []
		intro_list = []
		details_list = []
		productClassification=""
		productName=""
		productBrand=""
		productModel=""
		productPrice=""
		productImagePath=""
		productAddres=""
		productId=""
		productCompany=""
		productPack=""
		price=""
		fileName="www_ispek_cn_data_info.json"
		#Instantiation CrawlertoolsItem object
		item=BaseItem()
		#Parse text
		productImagePath=sel.xpath(".//*[@id='picshower']/img/@src").extract()[0]
		if  len(sel.xpath(".//div[@id='sample-table-2_wrapper']")) == 0:
			try:
				tempSel=sel.xpath(".//*[@id='main-container']/div/div[1]/div[1]/a")
				i=1
				classificationStr=""
				while i < len(tempSel):
					classificationStr=classificationStr+tempSel[i].xpath("text()").extract()[0].strip()+"|||"
					i+=1
				productClassification=classificationStr.rstrip("|||")
				tempSel=sel.xpath(".//*[@id='main-container']/div/div[1]/div[2]/div[2]")
				if len(tempSel.xpath("form")):
					tempSel=tempSel.xpath("form")
					temps=tempSel.xpath("div[1]/div[1]/span/text()")[0].extract()
					productPrice=temps.split("/")[0].strip()
					productPrice=filter(lambda ch: ch in '0123456789.', productPrice)
					productCompany=temps.split("/")[1]
				else:
					temps=tempSel.xpath("div[1]/div[1]/text()")[0].extract().strip()
					productPrice=filter(lambda ch: ch in '0123456789.~', temps).split("~")
					productCompany=""

				productName=tempSel.xpath("h2/text()").extract()[0]
				productBrand=tempSel.xpath("div[2]/div/div[1]/a/text()").extract()[0]
				tempSel=tempSel.xpath("div[2]/div/div")
				i=2
				while i<len(tempSel):
					tempStr=""
					tempStr=tempSel[i].xpath("text()").extract()[0].strip().split(u"：")
					if tempStr[0]==u"型号":
						productModel=tempStr[1]
					if tempStr[0]==u"产地":
						productAddres=tempStr[1]
					if tempStr[0]==u"包装":
						productPack=tempStr[1]
					i+=1
				prices=productPrice.encode('utf-8').replace("\"","\'").strip().split("~")
				if len(prices) >1:
					price=str(float(prices[0])*100)+"~"+str(float(prices[1])*100)
				else:
					price=str(float(prices[0])*100)

			except Exception,e:
				print "-----------------yichang--------------->",e
			#Formatted data
			item['productUrl']=response.url
			item['productImagePath'] = "http://www.ispek.cn"+productImagePath.encode('utf-8').replace("\"","\'").strip() 
			item['productClassification'] =productClassification.encode('utf-8').replace("\"","\'").strip()
			item['productName'] =productName.encode('utf-8').replace("\"","\'").strip()
			item['productBrand'] =productBrand.encode('utf-8').replace("\"","\'").strip()
			item['productModel'] =productModel.encode('utf-8').replace("\"","\'").strip()
			item['productAddres'] =productAddres.encode('utf-8').replace("\"","\'").strip()
			item['productCompany'] =productCompany.encode('utf-8').replace("\"","\'").strip()
			item['productPrice'] =price
			item['fileName']=fileName
			item['productDetails']=""
			item['productPack']=productPack.encode('utf-8').replace("\"","\'").strip()
			item['productIntro']=""
			item['productSpeci']=""
			yield item
		else:
			try:
				tempSel=sel.xpath(".//*[@id='main-container']/div/div[1]/div[1]/a")
				i=1
				classificationStr=""
				while i < len(tempSel):
					classificationStr=classificationStr+tempSel[i].xpath("text()").extract()[0].strip()+"|||"
					i+=1
				productClassification=classificationStr.rstrip("|||")
			except Exception,e:
				print str(e)+"--------------"
			j=0
			tableList=sel.xpath(".//table[@id='sample-table-2']/tbody/tr")
			print len(tableList)
			while j<len(tableList):
				try:
					temps=tableList[j].xpath("td[9]/text()")[0].extract().strip()
					productPrice=filter(lambda ch: ch in '0123456789.~', temps).split("~")
					productCompany=""
				except Exception,e:
					print "-----------------yichang--------------->",e
				try:
					productName=tableList[j].xpath("td[2]/text()")[0].extract().strip()
					productBrand=tableList[j].xpath("td[4]/text()")[0].extract().strip()
				except Exception,e:
					print "-----------------yichang--------------->",e

				try:
					productModel=tableList[j].xpath("td[5]/text()")[0].extract().strip()
					productAddres=tableList[j].xpath("td[3]/text()")[0].extract().strip()
					productPack=tableList[j].xpath("td[7]/text()")[0].extract().strip()
				except Exception,e:
					print "-----------------yichang--------------->",e
				try:
					productPrice=tableList[j].xpath("td[9]/text()")[0].extract().strip()
					prices=filter(lambda ch: ch in '0123456789.', productPrice).encode('utf-8')
					price=str(float(prices[0])*100)
				except Exception,e:
					print "-----------------yichang--------------->",e
				#Formatted data
				item['productUrl']=response.url
				item['productImagePath'] = "http://www.ispek.cn"+productImagePath.encode('utf-8').replace("\"","\'").strip() 
				item['productClassification'] =productClassification.encode('utf-8').replace("\"","\'").strip()
				item['productName'] =productName.encode('utf-8').replace("\"","\'").strip()
				item['productBrand'] =productBrand.encode('utf-8').replace("\"","\'").strip()
				item['productModel'] =productModel.encode('utf-8').replace("\"","\'").strip()
				item['productAddres'] =productAddres.encode('utf-8').replace("\"","\'").strip()
				item['productCompany'] =productCompany.encode('utf-8').replace("\"","\'").strip()
				item['productPrice'] =price
				item['fileName']=fileName
				item['productDetails']=details_list
				item['productPack']=pack_list
				item['productIntro']=intro_list
				item['productSpeci']=speci_list
				yield item
				j+=1
=======
=======
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
    name = "spider_ispek_redis"
    url = GetUrls()
    start_urls = url.getUrls(name)
    #start_urls=["http://www.ispek.cn/item/93418.html"]
    def __init__(self):
        log.init_log(settings.get('LOG_DIR'))

    #Details page
    def parse(self, response):
        #Analytical framework
        sel = Selector(response)
        #Loop body
        productClassification=""
        productName=""
        productBrand=""
        productModel=""
        productPrice=""
        productImagePath=""
        productAddres=""
        productId=""
        productCompany=""
        productPack=""
        price=""
        fileName="www_ispek_cn_data_info.json"
        #Instantiation CrawlertoolsItem object
        item=BaseItem()
        #Parse text
        productImagePath=sel.xpath(".//*[@id='picshower']/img/@src").extract()[0]
        if  len(sel.xpath(".//div[@id='sample-table-2_wrapper']")) == 0:
            try:
                tempSel=sel.xpath(".//*[@id='main-container']/div/div[1]/div[1]/a")
                i=1
                classificationStr=""
                while i < len(tempSel):
                    classificationStr=classificationStr+tempSel[i].xpath("text()").extract()[0].strip()+"|||"
                    i+=1
                productClassification=classificationStr.rstrip("|||")
                tempSel=sel.xpath(".//*[@id='main-container']/div/div[1]/div[2]/div[2]")
                if len(tempSel.xpath("form")):
                    tempSel=tempSel.xpath("form")
                    temps=tempSel.xpath("div[1]/div[1]/span/text()")[0].extract()
                    productPrice=temps.split("/")[0].strip()
                    productPrice=filter(lambda ch: ch in '0123456789.', productPrice)
                    productCompany=temps.split("/")[1]
                else:
                    temps=tempSel.xpath("div[1]/div[1]/text()")[0].extract().strip()
                    productPrice=filter(lambda ch: ch in '0123456789.~', temps).split("~")
                    productCompany=""

                productName=tempSel.xpath("h2/text()").extract()[0]
                productBrand=tempSel.xpath("div[2]/div/div[1]/a/text()").extract()[0]
                tempSel=tempSel.xpath("div[2]/div/div")
                i=2
                while i<len(tempSel):
                    tempStr=""
                    tempStr=tempSel[i].xpath("text()").extract()[0].strip().split(u"：")
                    if tempStr[0]==u"型号":
                        productModel=tempStr[1]
                    if tempStr[0]==u"产地":
                        productAddres=tempStr[1]
                    if tempStr[0]==u"包装":
                        productPack=tempStr[1]
                    i+=1
                prices=productPrice.encode('utf-8').replace("\"","\'").strip().split("~")
                if len(prices) >1:
                    price=str(float(prices[0])*100)+"~"+str(float(prices[1])*100)
                else:
                    price=str(float(prices[0])*100)

            except Exception,e:
                print "-----------------yichang--------------->",e
            #Formatted data
            item['productUrl']=response.url
            item['productImagePath'] = "http://www.ispek.cn"+productImagePath.encode('utf-8').replace("\"","\'").strip() 
            item['productClassification'] =productClassification.encode('utf-8').replace("\"","\'").strip()
            item['productName'] =productName.encode('utf-8').replace("\"","\'").strip()
            item['productBrand'] =productBrand.encode('utf-8').replace("\"","\'").strip()
            item['productModel'] =productModel.encode('utf-8').replace("\"","\'").strip()
            item['productAddres'] =productAddres.encode('utf-8').replace("\"","\'").strip()
            item['productCompany'] =productCompany.encode('utf-8').replace("\"","\'").strip()
            item['productPrice'] =price
            item['fileName']=fileName
            item['productDetails']=""
            item['productPack']=productPack.encode('utf-8').replace("\"","\'").strip()
            item['productIntro']=""
            item['productSpeci']=""
            yield item
        else:
            try:
                tempSel=sel.xpath(".//*[@id='main-container']/div/div[1]/div[1]/a")
                i=1
                classificationStr=""
                while i < len(tempSel):
                    classificationStr=classificationStr+tempSel[i].xpath("text()").extract()[0].strip()+"|||"
                    i+=1
                productClassification=classificationStr.rstrip("|||")
            except Exception,e:
                print str(e)+"--------------"
            j=0
            tableList=sel.xpath(".//table[@id='sample-table-2']/tbody/tr")
            print len(tableList)
            while j<len(tableList):
                try:
                    temps=tableList[j].xpath("td[9]/text()")[0].extract().strip()
                    productPrice=filter(lambda ch: ch in '0123456789.~', temps).split("~")
                    productCompany=""
                except Exception,e:
                    print "-----------------yichang--------------->",e
                try:
                    productName=tableList[j].xpath("td[2]/text()")[0].extract().strip()
                    productBrand=tableList[j].xpath("td[4]/text()")[0].extract().strip()
                except Exception,e:
                    print "-----------------yichang--------------->",e

                try:
                    productModel=tableList[j].xpath("td[5]/text()")[0].extract().strip()
                    productAddres=tableList[j].xpath("td[3]/text()")[0].extract().strip()
                    productPack=tableList[j].xpath("td[7]/text()")[0].extract().strip()
                except Exception,e:
                    print "-----------------yichang--------------->",e
                try:
                    productPrice=tableList[j].xpath("td[9]/text()")[0].extract().strip()
                    prices=filter(lambda ch: ch in '0123456789.', productPrice).encode('utf-8')
                    price=str(float(prices[0])*100)
                except Exception,e:
                    print "-----------------yichang--------------->",e
                #Formatted data
                item['productUrl']=response.url
                item['productImagePath'] = "http://www.ispek.cn"+productImagePath.encode('utf-8').replace("\"","\'").strip() 
                item['productClassification'] =productClassification.encode('utf-8').replace("\"","\'").strip()
                item['productName'] =productName.encode('utf-8').replace("\"","\'").strip()
                item['productBrand'] =productBrand.encode('utf-8').replace("\"","\'").strip()
                item['productModel'] =productModel.encode('utf-8').replace("\"","\'").strip()
                item['productAddres'] =productAddres.encode('utf-8').replace("\"","\'").strip()
                item['productCompany'] =productCompany.encode('utf-8').replace("\"","\'").strip()
                item['productPrice'] =price
                item['fileName']=fileName
                item['productDetails']=""
                item['productPack']=productPack.encode('utf-8').replace("\"","\'").strip()
                item['productIntro']=""
                item['productSpeci']=""
                yield item
<<<<<<< HEAD
                j+=1
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
                j+=1
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
