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
class deppreSpider(scrapy.Spider):
	name = "deppre"
	names = "spider_"+name + "_redis"
	allowed_domains = ["deppre.cn"]
	start_urls = [
		"http://www.deppre.cn"
	]
	#构造函数
	def __init__(self):
	   
		log.init_log(settings.get('LOG_DIR'))#
		logging.info("spider start......")
		print "spider start......"
		logging.info("fafafa")
	#主页面
	def parse(self, response):
		#sel是页面源代码，载入scrapy.selector
		sel = Selector(response)
		#每个连接，用@href属性
		for link in sel.xpath("//p[@class='parent_cat weiruanyahei']/a/@href").extract():
			#请求=Request(连接，parese_item)
			logging.info("-----linkzu="+link)
			request = scrapy.Request("http://www.deppre.cn/"+link, callback=self.parse_item2)
			yield request#返回请求

	#第二个页面
	def parse_item2(self, response):
		#filename = response.url.split("/")[-2]
		#open(filename, 'wb').write(response.body)
		for link in response.xpath("//ul[@class='goods_list clearfix']/li[@class='f_l']/p[@class='name']/a[@class='pro_name']/@href").extract():
			logging.info("----link2="+link)
			redis=RedisConnect()
			redis.setSadd(self.names,"http://www.deppre.cn/"+link)
		#获取页码集合
		pages = response.xpath("//div[@id='pager']/a[@class='pagebar_number']/@href").extract()
		#print('pages: %s' % pages)#打印页码
		if len(pages) >= 2:#如果页码集合>2
			page_link = pages[-2]#图片连接=读取页码集合的倒数第二个页码
			#page_link = page_link.replace('/a/', '')#图片连接=page_link（a替换成空）
			detail_link = 'http://www.deppre.cn/' + page_link
			#print detail_link+"---"
			logging.info("-----page_link="+detail_link)
			request = scrapy.Request(detail_link, callback=self.parse_item2)
			yield request
