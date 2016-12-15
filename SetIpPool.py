#! /usr/bin/env python
# -*- coding: utf-8 -*-

import redis
import urllib2
import time
class RedisConnect:
	#class member
	__redisId=""
	__host=""
	__port=""
	__db=""
	__pwd=""

	#Constructor, class member
	def __init__(self,host="",port="",db=0,pwd=""):
		self.__host=host
		self.__port=port
		self.__db=db
		self.__pwd=pwd
		self.__connect()

	#Link redis database
	def __connect(self):
		self.__redisId=redis.Redis(host=self.__host,port=self.__port,db=self.__db,password=self.__pwd)
	#Set the connection redis Road
	def setConnectPath(self,host,port,db,pwd):
		self.__host=host
		self.__port=port
		self.__db=db
		self.__pwd=pwd
		self.__connect()

	#Add an element to the collection
	def setSadd(self,key,value):
		try:
			return self.__redisId.sadd(key,value)
		except Exception,e:
			print e

	#Delete an element in a collection.
	def srem(self,key,member):
		try:
			return self.__redisId.srem(key,member)
		except Exception,e:
			print e

	#Get the total number of elements in the collection
	def getScard(self,key):
		try:
			return self.__redisId.scard(key)
		except Exception,e:
			print e

	#Get some member
	def getSrandmember(self,key,count):
		try:
			return self.__redisId.srandmember(key,count)
		except Exception,e:
			print e


	#To determine whether the set in the member
	def getSismember(self,key,member):
		try:
			return self.__redisId.sismember(key,member)
		except Exception,e:
			print e

	#Delete all keys	
	def delAllKey(self):
		try:
			return self.__redisId.flushdb()
		except Exception,e:
			print e

def getIp(count):
	url = "http://xvre.daili666api.com/ip/?tid=559436287116377&num=%d"%(count)
	req = urllib2.Request(url)
	res_data = urllib2.urlopen(req)
	res = res_data.read().split("\r\n")
	return res

def main():
	try:
<<<<<<< HEAD
<<<<<<< HEAD
		redis=RedisConnect("192.168.1.100",6379,0,"")
=======
		redis=RedisConnect("192.168.200.116",6379,4,"mypasshahayou")
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
		redis=RedisConnect("192.168.200.116",6379,4,"mypasshahayou")
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
		count=redis.getScard("ipPool")
		while True:
			if  not count:
				Ips=getIp(10000)
				for i in Ips:
					print "------Is insert ip :%s---------"%i
					redis.setSadd("ipPool",i)
					if redis.getScard("ipPool")>=1000:
						break 
			else:
				ipList=redis.getSrandmember("ipPool",500)
				for i in ipList:
					print "xxxxxxxxxxIs delete ip :%sxxxxxxxxxxx"%i
					redis.srem("ipPool",i)
				Ipss=getIp(10000)
				m=0
				while  redis.getScard("ipPool") <1000:
					print  redis.getScard("ipPool") 
					print "------Is update ip :%s---------"%Ipss[m]
					redis.setSadd("ipPool",Ipss[m])
					m+=1
			print "--------------------------Update Ip Success----------------------------"
			print "---------------------------Wait for the update, the next update will be in 60 seconds after the----------------------------------------------"
			time.sleep(60)

	except Exception,e:
<<<<<<< HEAD
<<<<<<< HEAD
		redis=RedisConnect("192.168.1.100",6379,0,"")
=======
		redis=RedisConnect("192.168.200.116",6379,4,"mypasshahayou")
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
		redis=RedisConnect("192.168.200.116",6379,4,"mypasshahayou")
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
		count=redis.getScard("ipPool")
		print e
		#Delete some ip

if __name__  == "__main__":
	main()
