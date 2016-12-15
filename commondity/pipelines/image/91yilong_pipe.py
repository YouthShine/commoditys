# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import requests
from commondity import settings
import os
import urllib
class BasePipeline(object):
    def process_item(self, item, spider):
        dir_path = '%s\%s'%(settings.IMAGES_STORE,spider.name)#存储路径
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        for image_url in item['image_urls']:
            image_url = "http://www.91yilong.com"+image_url
            list_name = image_url.split('/')
            list_name = list_name[len(list_name)-1]#源文件图片名字http://www.91yilong.com/images/201607/source_img/3990_P_1467350192336.jpg
            image_names = item['url'].split('/')#http://www.91yilong.com/goods-3990.html
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
            os.rename(oldfilename,Newdir)#重命名

        return item
