# -*- coding: utf-8 -*-
import os
import time
import datetime
import getpass
from ..tempConfig import *

class LogOutput:
	#Output file Name key
	__fileNameKey=""

	#Output file Name
	__fileName=""

	#System time
	__localTime=""

	#Output file path
	__filePath=""

	def __init__(self,filePath="./",fileNamekey="default"):
		cfg=config("Log")
		if filePath=="":
			filePath=cfg["filePath"]
		if fileNamekey==0:
			fileNamekey=cfg["fileNamekey"]
		self.__fileNameKey=fileNamekey
		self.__filePath=filePath
		self.__localTime=self.getDayTime()
		self.__fileName=str(self.dateToTimestamp(self.getDayDate()))+"_"+self.__fileNameKey+".log"

	#Set file name
	def setLogFileName(self,fileName):
		self.__fileNameKey=fileName
		self.__fileName=str(self.dateToTimestamp(self.getDayDate()))+"_"+self.__fileNameKey

	#Set file path
	def setLogFilePath(self,filePath):
		self.__filePath=filePath
		
	#Get the day time stamp	
	def getDayTime(self):
		timeStamp = int(time.time())
		timeArray = time.localtime(timeStamp)
		otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
		return otherStyleTime

	#Get the date of the day
	def getDayDate(self):
		date=self.getDayTime().split(" ")[0]
		return date
	
	#Date turning time
	def dateToTimestamp(self,date):
		date=date.strip()
		dates=date.split(" ")
		timeStamp=""
		if len(dates) == 1:
			timeArray = time.strptime(date, "%Y-%m-%d")
			timeStamp = int(time.mktime(timeArray))
		else:
			timeArray = time.strptime(date, "%Y-%m-%d %H:%M:%S")
			timeStamp = int(time.mktime(timeArray))
		return timeStamp

	#Write file
	def writeFile(self,txt):
		filePath=self.__filePath+"/"+self.__fileName
		print filePath
		if not os.path.exists(filePath):
			if os.path.exists("lib/Log/logTips.log"):
				print filePath
				f=open(filePath,"w")
				for i in open("lib/Log/logTips.log","r"):
					f.write(i+"\n")
				f.close()
		f = open(filePath,"a+")
		f.write(txt+"\n\n")
		f.close()


	#Assembly information
	def assemblyTxt(self,info,iCnt=0):
		info=str(info)
		systemUser= getpass.getuser()
		if iCnt==0:
			tips="[ERROR]"
		else:
			tips="[PRINT]"
		txt=systemUser+tips+": "+self.getDayTime()+":\n["
		txt=txt+info+"]"
		return txt

	#Write error log
	def log(self,txt):
		tempTxt=self.assemblyTxt(txt)
		self.writeFile(tempTxt)

	#Write people log
	def log_print(self,txt):
		tempTxt=self.assemblyTxt(txt,1)
		self.writeFile(tempTxt)