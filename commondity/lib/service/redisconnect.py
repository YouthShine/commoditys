#! /usr/bin/env python
# -*- coding: utf-8 -*-
# 	

import redis
class RedisConnect:
	#class member
	__redisId=""
	__host=""
	__port=""
	__db=""
	__pwd=""


	#Constructor, class member
	
<<<<<<< HEAD
<<<<<<< HEAD
	def __init__(self,host="192.168.1.230",port="6379",db=0,pwd=""):
=======
	def __init__(self,host="192.168.200.116",port="6379",db=4,pwd="mypasshahayou"):
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
	def __init__(self,host="192.168.200.116",port="6379",db=4,pwd="mypasshahayou"):
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
		#def __init__(self,host="192.168.1.100",port="6379",db=0,pwd=""):
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

	#print redis info
	def print_info(self):
		try:
			return self.__redisId.info()
		except Exception,e:
			print e

	#Type of query keywords
	def getType(self,key=""):
		try:
			if  key=="":
				return ""
			else:
				return self.__redisId.type(key)
		except Exception,e:
			print e	

	#Get all the keys
	def getKeys(self,keyLike=""):
		try:
			if  keyLike=="":
				return self.__redisId.keys()
			else:
				return self.__redisId.keys(keyLike)
		except Exception,e:
			print e

	#Sets the value of the keyword
	def setKey(self,key,value):
		try:
			return self.__redisId.set(key,value)
		except Exception,e:
			print e
	def lPush(self,key,value):
		try:
			return self.__redisId.lpush(key,value)
		except Exception,e:
			print e
	def lPop(self,key):
		try:
			return self.__redisId.lpop(key)
		except Exception,e:
			print e
	def lRange(self,key,start,end):
		try:
			return self.__redisId.lrange(key,start,end)
		except Exception,e:
			print e
	def lLen(self,key):
		try:
			return self.__redisId.llen(key)
		except Exception,e:
			print e
	#Gets the value of the keyword
	def getKey(self,key):
		try:
			return self.__redisId.get(key)
		except Exception,e:
			print e

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

	#Get the difference between Set1 and set2
	def getSdiff(self,key1,key2):
		try:
			return self.__redisId.sdiff(key1,key2)
		except Exception,e:
			self.__log.log("Redis:"+str(e))
			print e

	#The difference between Set1 and set2 is stored in set3.
	def getSdiffStore(self,key1,key2,key3):
		try:
			return self.__redisId.sdiffstore(key3,key1,key2)
		except Exception,e:
			self.__log.log("Redis:"+str(e))
			print e

	#Get the intersection of set2 and Set1
	def getSinter(self,key1,key2):
		try:
			return self.__redisId.sinter(key1,key2)
		except Exception,e:
			print e

	#The intersection of Set1 and set3 in set2
	def getSinterStore(self,key1,key2,key3):
		try:
			return self.__redisId.sinterstore(key3,key1,key2)
		except Exception,e:
			print e

	#Gets all the elements in the collection
	def getSmembers(self,key):
		try:
			return self.__redisId.smembers(key)
		except Exception,e:
			print e

	#To determine whether the set in the member
	def getSismember(self,key,member):
		try:
			return self.__redisId.sismember(key,member)
		except Exception,e:
			print e

	#We get Set1 and set2
	def getSunion(self,key1,key2):
		try:
			return self.__redisId.sunion(key1,key2)
		except Exception,e:
			print e

	#The union of Set1 and set2 stored in set3
	def getSunionStore(self,key1,key2,key3):
		try:
			return self.__redisId.sunionstore(key3,key1,key2)
		except Exception,e:
			print e

	#Delete all keys	
	def delAllKey(self):
		try:
			return self.__redisId.flushdb()
		except Exception,e:
			print e


			
