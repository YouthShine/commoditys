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
from scrapy.http import FormRequest
import requests

class AlibabaSpider(scrapy.Spider):
	name = "mayun"
	names = "spider_"+name + "_redis"
	allowed_domains = ["1688.com"]
	start_urls = [
		"http://page.1688.com/channel/imall/index.html"
	]
	#构造函数
	def __init__(self):
	   
		log.init_log(settings.get('LOG_DIR'))#
		logging.info("spider start......")
		print "spider start......"
		logging.info("fafafa")
	#主页面 

	#第二个页面
	def parse(self, response):
		for link in response.xpath("//div[@class='menu-sub-box']/div[@class='subject-box']/dl/dd/ul/li/a/@href").extract():
			logging.info("-----linkzu--------="+link)
			request = scrapy.Request(link, callback=self.parse_item2)
			print "-------------------watting1--------3s------------"
			time.sleep(3)
			yield request

	def parse_item2(self, response):
		logging.info("-----login_page------="+response.url)
		print "-------------------watting2--------3s------------"
		time.sleep(3)
		cookies= {
		'__sw_sdby_count__':'1', 
		'cna':'LCUnECVrmU4CAX1U7XU23Aba',
		'ali_beacon_id':'222.181.11.172.1474953821675.666449.6',
		'hp_ab_is_marked_2016':'1', 
		'ad_prefer':'"2016/09/27 15:22:42"', 
		'h_keys':'"%u52b3%u4fdd%u624b%u5957"', 
		'ali_apache_track':'"c_ms=1|c_mt=3|c_mid=b2b-2261990693|c_lid=%E6%88%91%E4%BB%AC%E4%B8%8D%E6%95%A3726"', 
		'JSESSIONID':'9L78ybdu1-NbQW0QDMARlR6PEes5-y3Kg3yP-5EL4', 
		'ali_apache_tracktmp':'"c_w_signed=Y"',
		'_is_show_loginId_change_block_':'b2b-2261990693_false', 
		'_show_force_unbind_div_':'b2b-2261990693_false',
		'_show_sys_unbind_div_':'b2b-2261990693_false',
		'_show_user_unbind_div_':'b2b-2261990693_false',
		'ali_ab':'222.181.11.172',
		'alisw':'swIs1200%3D1%7C',
		'__rn_alert__':'false',
		'alicnweb':'touch_tb_at%3D1475028932646%7Clastlogonid%3D%25E6%2588%2591%25E4%25BB%25AC%25E4%25B8%258D%25E6%2595%25A3726%7Cshow_inter_tips%3Dfalse', 
		'l':'AkZGLxgBm2TQhF7Fzxi1sl8rFjbIhIph', 
		'isg':'AkhIJ1Rmi4AVzecGXSzom5LrGbYf4qz7viUvuAL5t0O23ehHqgF8i96VIwJX',
		'__cn_logon__':'true', 
		'__cn_logon_id__':'%E6%88%91%E4%BB%AC%E4%B8%8D%E6%95%A3726',
		'cn_tmp':'"Z28mC+GqtZ24XmL/L6p+JQToKjesSD6zOa0Hs34Hd4+ylBJ4fy6O4EGtxTzOOaWD5MVcHmFQQjyD5txZ0DGIoKjNJXt63xGOyeeZlfXtGVqcpUT74mvhckHy4Bq3v0hnU1LtUVXZboiGrmH2CFmNpCDCBFUyV2Vs9ORA/H//ggNs11384nGDStQhe+7Fm4CQFx/zTX8/vDcTj8dQfax9iTkxo7BhhxLmkR9+rM5PrvHXyYbkheEQOw=="',
		'_cn_slid_':'"FiEc47C%2FBR"', 
		'_nk_':'"c0f4UE7gVFYvBLTsKJTV%2FQ%3D%3D"', 
		'tbsnid':'GBJgrwTyoXBIT2lwP5ejwNcHqehxWMd1r3cQhZQKdZM6sOlEpJKl9g%3D%3D', 
		'LoginUmid':'"RXJz9a4XkAUJBO5lizngnInZJenv%2B65StmOOpYkZMIjmkdAiNY8Cqw%3D%3D"',
		'userID':'"Gpze%2FNsP2bYNDTJXRMGxsK1RLM9kkLmp8nxqzrjCnf46sOlEpJKl9g%3D%3D"', 
		'last_mid':'b2b-2261990693',
		'unb':'2261990693', 
		'userIDNum':'"5qTF1iCw%2F2a6o%2F7uRMwTmg%3D%3D"',
		'__last_loginid__':'"%E6%88%91%E4%BB%AC%E4%B8%8D%E6%95%A3726"',
		'login':'"kFeyVBJLQQI%3D"',
		'_csrf_token':'1475029899220', 
		'_tmp_ck_0':'"1CjJCWAHY0ScC6AdjqDU%2BTKqcMHsgQuBZrOXFszDRRiVbasYiTp5JKfScGy%2B164NPsGA0UfZl2QW0AZv4IEHnkYVYVQcFj3x5ixslsnYIWgtY7pK0GDhQY%2BL6P7H9mJi%2FRAuEAlqCE9jTVZvW6Re9yTFUO2hhwHyE9VoCiei1Sa4eoZD%2BtJ8vmwQHf2%2FDZ52D3nW4UvG3t3tvgqX%2F6zuzEfUaF4fm2IAwPDE5a2Yba5n8Iala%2F9cmQ2C%2FHaGUXx71Osv4PjFYNBbkPqp7Q7MDpyj0IvkswAquWStfWkMlo3nS%2BpaxMJopyQ%2FXDsn97GPNQbAkTrVmu%2BsyYP55WkFTrded%2BaYnTetoI24xEFugHebnPL6grp2ltJW5R7zWcnYxsVVucYlQ%2FrqhpFGHGzQk9bG0q1BarH8qbI19%2BnUZwy%2FfPX%2Bv%2BpDF4ZnlCzIMePVNDJfhzkO%2FlMBkCAk31K3KJy3smwCaZkiC9VqYuOK2l%2B4VszeLgXo3Wl6z%2BtxwNxYh%2BEZ%2BkUFPjzXTcyuthvwhG2gk0Dly8AKHnvDqmc8ofs%3D"'}
		request = FormRequest(response.url,cookies=cookies,callback=self.parse_item3)
		print "-------------------watting3--------3s------------"
		time.sleep(3)
		yield request

	def parse_item3(self, response):
		logging.info("-----login_success_page------="+response.url)
		print "-------------------watting4--------3s------------"
		time.sleep(3)
		for link in response.xpath("//ul[@id='sm-offer-list']/li/div/div[@class='s-widget-offershopwindowtitle sm-offer-title sw-dpl-offer-title']/a/@href").extract():
			logging.info("-----link3="+link)
			redis=RedisConnect()
			redis.setSadd(self.names,link)
