# -*- coding: utf-8 -*-
# Note: the database operation method parameters are string type JSON, 
# 		the function will automatically call json.loads()
# 
 

import pymongo
from ..Log.logOutput import *
from ..tempConfig import *
import json


class MongodbConnect:
	#Port address
	__host=""

	#Port number
	__port=27017

	#Data base
	__db=""

	#Table name
	__table=""

	#User name  
	__user=""

	#User password
	__pwd=""

	#Database identifier
	__dbIdentifier=""

	#table collection
	__collection=""

	#logs id
	__log=""

	#Constructor
	def __init__(self,host="",port=0,db="",table="",user="",pwd=""):
		cfg=config("Mongodb")
		if host=="":
			host=cfg["host"]
		if port==0:
			port=cfg["port"]
		if db=="":
			db=cfg["db"]
		if table=="":
			table=cfg["table"]
		if user=="":
			user=cfg["user"]
		if pwd=="":
			pwd=cfg["pwd"]
		self.setConnectPath(host,port,db,table,user,pwd)	
		self.__log=LogOutput("commondity/public/logs","Mongodb")

	#Database connection
	def sqlConnect(self):
		try:
			connect=pymongo.MongoClient(self.__host,self.__port)
			exec("rdb=connect."+self.__db)
			rdb.authenticate(self.__user,self.__pwd)
			self.__dbIdentifier = rdb
			self.selectTable("scrapy")
		except Exception,e:
			print e
			self.__log.log("Mongodb:"+str(e))
		

	#selective listing  
	def selectTable(self,tableName):
		self.__collection=self.__dbIdentifier[tableName]

	#Set connection properties
	def setConnectPath(self,host="",port=0,db="",table="test",user="",pwd=""):
		self.__host=host
		self.__port=port
		self.__db=db
		self.__table=table
		self.__user=user
		self.__pwd=pwd

	#Insert data
	def insert(self,jsonTxt="{}"):
		try:
			return self.__collection.insert(json.loads(jsonTxt))
		except Exception,e:
			self.__log.log("Mongodb:"+str(e))
			print e

	#Find data
	def find(self,jsonTxt=""):
		try:
			if jsonTxt=="":
				return self.__collection.find()
			else:
				return self.__collection.find(json.loads(jsonTxt))
		except Exception,e:
			self.__log.log("Mongodb:"+str(e))
			print e

	#Delete data
	def remove(self,jsonTxt=""):
		try:
			if jsonTxt=="":
				return self.__collection.remove(json.loads("{}"))
			else:
				return self.__collection.remove(json.loads(jsonTxt))
		except Exception,e:
			self.__log.log("Mongodb:"+str(e))
			print e

	#Delete data sheet
	def drop(self):
		try:
			self.__collection.drop()
		except Exception,e:
			self.__log.log("Mongodb:"+str(e))
			print e


