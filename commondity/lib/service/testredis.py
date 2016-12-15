#! /usr/bin/env python
# -*- coding: utf-8 -*-
#       
from redisconnect import *

if __name__=="__main__":
	name = "spider_ehsy_redis"
        redis=RedisConnect()
        data=redis.getSmembers(name)
	print len(data)
	i=0
	for element in data:
		 i+=1
		 if i%8==0 :
			redis.setSadd("spider_ehsy_redis_0",element)
		 elif i%8==1 :
			redis.setSadd("spider_ehsy_redis_1",element)
		 elif i%8==2 :
			redis.setSadd("spider_ehsy_redis_2",element)
		 elif i%8==3 :
			redis.setSadd("spider_ehsy_redis_3",element)
		 elif i%8==4 :
			redis.setSadd("spider_ehsy_redis_4",element)
		 elif i%8==5 :
			redis.setSadd("spider_ehsy_redis_5",element)
		 elif i%8==6 :
			redis.setSadd("spider_ehsy_redis_6",element)
		 elif i%8==7 :
			redis.setSadd("spider_ehsy_redis_7",element)
