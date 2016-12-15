# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaseItem(scrapy.Item):
	productUrl = scrapy.Field()
	productName = scrapy.Field()
	productBrand = scrapy.Field()
	productModel = scrapy.Field()
	productClassification = scrapy.Field()
	productPrice = scrapy.Field()
	productImagePath = scrapy.Field()
	productAddres = scrapy.Field()
	productCompany = scrapy.Field()
	fileName = scrapy.Field()

	#商品详情
	productDetails = scrapy.Field()
	#商品包装参数
	productPack = scrapy.Field()
	#商品简介
	productIntro = scrapy.Field()
	#商品规格参数
	productSpeci = scrapy.Field()