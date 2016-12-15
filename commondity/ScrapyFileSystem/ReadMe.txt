class RedisConnect:
	#Set the connection redis Road
	def setConnectPath(self,host,port,db,pwd):

	#print redis info
	def print_info(self):

	#Type of query keywords
	def getType(self,key=""):

	#Get all the keys
	def getKeys(self,keyLike=""):

	#Sets the value of the keyword
	def setKey(self,key,value):

	#Gets the value of the keyword
	def getKey(self,key):

	#Add an element to the collection
	def setSadd(self,key,value):

	#Delete an element in a collection.
	def srem(self,key,member):

	#Get the total number of elements in the collection
	def getScard(self,key):

	#Get the difference between Set1 and set2
	def getSdiff(self,key1,key2):

	#The difference between Set1 and set2 is stored in set3.
	def getSdiffStore(self,key1,key2,key3):

	#Get the intersection of set2 and Set1
	def getSinter(self,key1,key2):

	#The intersection of Set1 and set3 in set2
	def getSinterStore(self,key1,key2,key3):

	#Gets all the elements in the collection
	def getSmembers(self,key):

	#To determine whether the set in the member
	def getSismember(self,key,member):

	#We get Set1 and set2
	def getSunion(self,key1,key2):

	#The union of Set1 and set2 stored in set3
	def getSunionStore(self,key1,key2,key3):

	#Delete all keys	
	def delAllKey(self):


class MongodbConnect:
	#Set connection properties
	def setConnectPath(self,host="",port=0,db="",table="test",user="",pwd=""):

	#Insert data
	def insert(self,jsonTxt="{}"):

	#Find data
	def find(self,jsonTxt=""):

	#Delete data
	def remove(self,jsonTxt=""):

	#Delete data sheet
	def drop(self):