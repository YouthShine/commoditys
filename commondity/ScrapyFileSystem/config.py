# -*- coding: utf-8 -*-
# This is the configuration file for the entire file system.
# It can initialize the initial information of Log, Redis, Mongondb.
# You can also choose not to write the configuration file, you can also call the time to manually initialize their own.
#Write the corresponding configuration in the corresponding position


def config(cfgName):
	Log={"filePath":"commondity/public/logs","fileNamekey":"default"}
<<<<<<< HEAD
<<<<<<< HEAD
	Redis={"host":"192.168.1.230","port":6379,"db":0,"pwd":""}
=======
	Redis={"host":"192.168.200.116","port":6379,"db":5,"pwd":"mypasshahayou"}
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
	Redis={"host":"192.168.200.116","port":6379,"db":5,"pwd":"mypasshahayou"}
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
	Mongodb={"host":"119.29.195.206","port":27017,"db":"scrapy","table":"scrapy","user":"scrapy","pwd":"12345678"}
	if cfgName=="Log":
		return Log
	if cfgName=="Redis":
		return Redis
	if cfgName=="Mongodb":
		return Mongodb
