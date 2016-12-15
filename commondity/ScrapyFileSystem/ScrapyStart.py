# -*- coding: utf-8 -*-
from lib.function import *
from lib.Log.logOutput import *
import json
import codecs
import os
import time
import urllib
import hashlib

#MD5 encryption
def md5(addStr):
	m = hashlib.md5()
	m.update(addStr)
	return m.hexdigest()


def DataAnalysis(jsonText):
	logs = LogOutput("commondity/public/logs","ScrapyStart")
	try:
		date=json.loads(jsonText)
		#Add password date str
		addPwdDate=md5(jsonText)
		#Query whether it is duplicate data
		redis=RedisConnect()
		dateId=md5(date["productUrl"]+date["productModel"])
		dateMd5=redis.getKey(dateId)
		if not dateMd5:
			redis.setKey(dateId,addPwdDate)
			writeFile(jsonText)
<<<<<<< HEAD
<<<<<<< HEAD
			print "---------------insert success----------------"
=======
			print "insert success!"
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
			print "insert success!"
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
		else:
			if  dateMd5!=addPwdDate:
				redis.setKey(dateId,addPwdDate)
				writeFile(jsonText)
<<<<<<< HEAD
<<<<<<< HEAD
				print "------------update success!--------------"
			else:
				print "------------your date is don't bian---------------"
=======
				print "update success!"
			else:
				print "your date is don't bian"
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
				print "update success!"
			else:
				print "your date is don't bian"
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
	except Exception,e:
		logs.log("ScrapyStart:"+str(e))
		print e
	

def downloadImage(save_path,image_url,save_name=""):
<<<<<<< HEAD
<<<<<<< HEAD
	url = image_url.encode('utf-8').replace("\"","\'").strip()
=======
	url = image_url
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
	url = image_url
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
	hz=url.split(".")[-1]
	if save_name == "":
		save_name=md5(url)
	path=save_path+"/"+url.split("/")[2]
	if not os.path.exists(path):
		os.makedirs(path)
	path = path+"/"+save_name+"."+hz
	i = 0
	data = 0
	while  i<3 :
		try:			
			data = urllib.urlopen(url).read()
			break
		except IOError,e:
			print "----------->%d<--------------"%(i+1)
			print e
			i+=1
	if not data:
		logs=open("commondity/public/img/download_logs.txt","a+")
		logs.write("image_url:"+image_url+"\n")
		logs.close()
		return 0
	else:
		f = file(path,"wb")
		f.write(data)
		f.close()
		return path

def writeFile(txt):
	date=json.loads(txt)
	timeStamp = int(time.time())
	timeArray = time.localtime(timeStamp)
	otherStyleTime = time.strftime("%Y%m%d:%H",timeArray).split(":")
	#Defualt
	#int
	sales_volume=0
	provider_id=0
	platform_id=0
	category_id_two=0
	brand_id=0
	category_id_one=0
	category_id=0
	commodity_id=0
	private_price=0.0

	#str
	credit=""
	logo_url=""
	is_display="true"
	payment_cycle=""
	is_recommend="flase"
	payment_method=""
	provider_name=""
	category_name_one=""
	category_name_two=""
	category_name=""
	main_pic_url=""
	#Category
	productClassification=date["productClassification"].split("|||")
	if len(productClassification) > 0:
		category_name_one=productClassification[0]
	if len(productClassification) > 1:
		category_name_two=productClassification[1]
	if len(productClassification) > 2:
		category_name=productClassification[2]

	commodity_url=date["productUrl"]
	#Image download
	
<<<<<<< HEAD
<<<<<<< HEAD
	path="commondity/public/img/"+otherStyleTime[0]+"/"+otherStyleTime[1]
=======
	path="commondity/public/img/"+otherStyleTime[0]+"/"+otherStyleTime[1]+"/"
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
	path="commondity/public/img/"+otherStyleTime[0]+"/"+otherStyleTime[1]+"/"
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
	if not os.path.exists(path):
		os.makedirs(path)
	try:
		main_pic_url=downloadImage(path,date["productImagePath"])
	except Exception,e:
		print e
		logs=open("commondity/public/img/download_logs.txt","a+")
		logs.write("commodity_url:"+commodity_url+"\n")
		logs.close()
		print "图片加载失败"
		
	#commodity_attr
	attrkey1=u"型号"
	attrname1=date["productModel"]
	attrkey2=u"单位"
	attrname2=date["productCompany"]

	brand_name=date["productBrand"]
	commodity_name=date["productName"]
	area=date["productAddres"]
	price=date["productPrice"]

	#新加字段
	details=json.dumps(date["productDetails"]).decode("unicode_escape")
	pack=json.dumps(date["productPack"]).decode("unicode_escape")
	intro=json.dumps(date["productIntro"]).decode("unicode_escape")
	speci=json.dumps(date["productSpeci"]).decode("unicode_escape")


	if price == "":
		price=0.0
	else:
		price=float(price)
	
	#write str temple
	PreservationTxt='"sales_volume":0,"provider_id":0,"platform_id":0,"category_id_two":0,"brand_id":0,"category_id_one":0,"category_id":0,"commodity_id":0,"private_price":[],'
	PreservationTxt=PreservationTxt+'"credit":"","logo_url":"","is_display":true,"payment_cycle":"","is_recommend":false,"payment_method":"","provider_name":"",'
	PreservationTxt=PreservationTxt+'"category_name_one":"%s","category_name_two":"%s","category_name":"%s","main_pic_url":"%s","commodity_attr":[{"attrkey":"%s","attrname":"%s"},{"attrkey":"%s","attrname":"%s"}],"brand_name":"%s","commodity_name":"%s","area":"%s","price":%.2f,"commodity_url":"%s"'%(category_name_one,category_name_two,category_name,main_pic_url,attrkey1,attrname1,attrkey2,attrname2,brand_name,commodity_name,area,price,commodity_url)
	PreservationTxt=PreservationTxt+',"details":%s,"pack":%s,"intro":%s,"speci":%s'%(details,pack,intro,speci)
	PreservationTxt="{"+PreservationTxt+"}"

	fileName=date["productUrl"].split("/")[2].split(".")[1]
	path="commondity/public/json/"+otherStyleTime[0]+"/"+otherStyleTime[1]+"/"

	if not os.path.exists(path):
		os.makedirs(path)
	fileName=path+"/"+fileName+".json"
	file=codecs.open(fileName,"a+",encoding="utf-8")   
	file.write(PreservationTxt + '\n')
	file.close()

	

"""
if __name__ == "__main__":
	#DataAnalysis(strd)
	strd='{"productImagePath": "", "productPrice": "44880.0", "productPack": [{"attrkey": "长度(mm)", "keyname": "200"}, {"attrkey": "宽度(mm)", "keyname": "65"}, {"attrkey": "高度(mm)", "keyname": "90"}, {"attrkey": "重量(kg)", "keyname": "0.20"}], "productModel": "", "productSpeci": [{"attrkey": "类别", "keyname": "手持式放大镜"}, {"attrkey": "放大倍数", "keyname": "30×"}, {"attrkey": "尺寸(mm)", "keyname": "Φ43×65×184"}, {"attrkey": "有效直径(mm)", "keyname": "7"}, {"attrkey": "重量(g)", "keyname": "40"}], "productName": "放大镜，必佳 手持式带灯放大镜30×，1996-L", "productClassification": "实验室产品|||光学检测仪器|||放大镜", "productUrl": "http://www.ehsy.com/product-LAE421", "productDetails": [], "productBrand": "", "productIntro": [], "productAddres": "", "fileName": "spider_ehsy_redis.json", "productCompany": ""}'
	writeFile(strd)
"""
