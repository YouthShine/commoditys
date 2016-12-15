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
from commondity.tools import *

class IspekSpider(scrapy.Spider):
    #Reptile name (unique)
    name = 'ispek'

    names="spider_"+name+"_redis"
    #Allowable range
    allowed_domains=["ispek.cn"]

    #Start path (crawler entry)
    start_urls=["http://www.ispek.cn/list/1.html",
                "http://www.ispek.cn/list/2.html",
                "http://www.ispek.cn/list/3.html",
                "http://www.ispek.cn/list/4.html",
                "http://www.ispek.cn/list/5.html",
                "http://www.ispek.cn/list/6.html",
                "http://www.ispek.cn/list/7.html",
                "http://www.ispek.cn/list/8.html",
                "http://www.ispek.cn/list/9.html",
                "http://www.ispek.cn/list/15.html",
                "http://www.ispek.cn/list/16.html"]

    #Data container (for heavy)
    items=[]

    #Climb path
    visitedWebUrl=[]

    #No path
    noAccessURL=[]

    def __init__(self):
        log.init_log(settings.get('LOG_DIR'))


    def parse(self,response):
        #Analytical framework
        sel = Selector(response)
        tempContent=sel.xpath(".//*[@id='main-container']/div/div/div[2]/div[2]/div[5]/ul/li")
        
        #Loop body
        for temp in tempContent:
            #Instantiation CrawlertoolsItem object

            #Parse text
            commodityUrls=temp.xpath("p[1]/a/@href").extract()
            commodityUrl= ["http://www.ispek.cn/"+t.encode('utf-8').replace("\"","\'").strip() for t in commodityUrls] 
            #Check whether duplicate data
            commodityUrl=commodityUrl[0]
            if not commodityUrl in self.items:
                self.items.append(commodityUrl)
                #yield Request(commodityUrl,callback=self.content_parse)
                redis=RedisConnect()
                redis.setSadd(self.names,commodityUrl)
                print "-------------------------------------------------insert url in redis:",commodityUrl

            self.analysisUrl(response,sel)
            
            while len(self.noAccessURL) > 0:
                url=self.noAccessURL[0]
                self.visitedWebUrl.append(url)
                self.noAccessURL.pop(0)
                yield Request(url,callback=self.parse)

    #Analytic path
    def analysisUrl(self,response,selectors):
        urls=selectors.xpath(".//*[@id='main-container']/div/div/div[2]/div[2]/ul/li")
        urls=urls.xpath("a/@href").extract()
        i=0
        while i<len(urls):
            temp=urls[i].strip()
            if temp == "" :
                urls[i].pop(i)
                continue
            else:
                urls[i]=temp
                i+=1

        self.handleUrl(response,urls,"http://www.ispek.cn")

    #Hand path
    def handleUrl(self,response,urls,basicsUrlPath=""):
        self.visitedWebUrl.append(response.url)
        for url in urls:
            url=basicsUrlPath+url
            if not url in self.visitedWebUrl:
                if not url in self.noAccessURL:
                    self.noAccessURL.append(url)