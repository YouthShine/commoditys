# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import requests
from commondity import settings
import os
import urllib
from commondity.ScrapyFileSystem.ScrapyStart import *

import json
class BasePipeline(object):
<<<<<<< HEAD
<<<<<<< HEAD
	def process_item(self, item, spider):
		#self.file=codecs.open("./CrawlerTools/public/json/"+fileName,"a+",encoding="utf-8")
		line = json.dumps(dict(item))
		DataAnalysis(line)
		#writeFile(line)
		"""
		dir_path = '%s/%s'%(settings.IMAGES_STORE,spider.name)#存储路径
		
		if not os.path.exists(dir_path):
			os.makedirs(dir_path)
		for image_url in item['productImagePath']:
			list_name = image_url.split('/')
			list_name = list_name[len(list_name)-1]#源文件图片名字
			image_names = item['productUrl'].split('/')
			image_name = image_names[len(image_names)-1]
			image_namess = image_name.split('.')#image_name字符串变列表image_namess
			image_namesss = image_namess[len(image_namess)-2]#image_namess列表变字符串image_namesss
			file_path = '%s/%s'%(dir_path,list_name)
				# print 'file_path',file_path
			if os.path.exists(list_name):
				continue
			with open(file_path,'wb') as file_writer:
				conn = urllib.urlopen(image_url)#下载图片
				file_writer.write(conn.read()) 
			file_writer.close()
			#model重命名图片名字
			filetype = os.path.splitext(list_name)[1]
			chdir(os.path.dirname(dir_path))#进入目录
			oldfilename = os.path.join(dir_path,list_name)	 
			Newdir = os.path.join(dir_path,image_namesss+filetype)
			#print Newdir+"------"
			#print oldfilename+"------"
			os.rename(oldfilename,Newdir)

		return item
		"""
=======
=======
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
    def process_item(self, item, spider):
        #self.file=codecs.open("./CrawlerTools/public/json/"+fileName,"a+",encoding="utf-8")
        line = json.dumps(dict(item))
        DataAnalysis(line)
        #writeFile(line)
        """
        dir_path = '%s/%s'%(settings.IMAGES_STORE,spider.name)#存储路径
        
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        for image_url in item['productImagePath']:
            list_name = image_url.split('/')
            list_name = list_name[len(list_name)-1]#源文件图片名字
            image_names = item['productUrl'].split('/')
            image_name = image_names[len(image_names)-1]
            image_namess = image_name.split('.')#image_name字符串变列表image_namess
            image_namesss = image_namess[len(image_namess)-2]#image_namess列表变字符串image_namesss
            file_path = '%s/%s'%(dir_path,list_name)
                # print 'file_path',file_path
            if os.path.exists(list_name):
                continue
            with open(file_path,'wb') as file_writer:
                conn = urllib.urlopen(image_url)#下载图片
                file_writer.write(conn.read()) 
            file_writer.close()
            #model重命名图片名字
            filetype = os.path.splitext(list_name)[1]
            chdir(os.path.dirname(dir_path))#进入目录
            oldfilename = os.path.join(dir_path,list_name)     
            Newdir = os.path.join(dir_path,image_namesss+filetype)
            #print Newdir+"------"
            #print oldfilename+"------"
            os.rename(oldfilename,Newdir)

        return item
        """
<<<<<<< HEAD
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
