import random
import urllib2
import redis
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
from commondity.ScrapyFileSystem.config import *
class RotateUserAgentMiddleware(UserAgentMiddleware):
	
	def __inti__(self,user_agent=""):
		self.user_agent=user_agent

	def process_request(self,request,spider):
		user_agent_list=["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "  
					"(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",  
					"Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "  
					"(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",  
					"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "  
					"(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",  
					"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "  
					"(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",  
					"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "  
					"(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",  
					"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "  
					"(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",  
					"Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "  
					"(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",  
					"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "  
					"(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",  
					"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "  
					"(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
					"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "  
					"(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",  
					"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "  
					"(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",  
					"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "  
					"(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",  
					"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "  
					"(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",  
					"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "  
					"(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",  
					"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "  
					"(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",  
					"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "  
					"(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",  
					"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "  
					"(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",  
					"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "  
					"(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"  ]
		ua=random.choice(user_agent_list)
		if ua:
			request.headers.setdefault("User-Agent",ua)

		#Get  ip
<<<<<<< HEAD
<<<<<<< HEAD
		#url = "http://xvre.daili666api.com/ip/?tid=559436287116377&num=1&foreign=only&operator=1"
		#req = urllib2.Request(url)
		#res_data = urllib2.urlopen(req)
		#res = res_data.read().split("\r\n")
		#print res[0],"-----------ip------------"
		#urls=res[0].split(":")
		#cfg=config("Redis")
                #redisId=redis.Redis(cfg["host"],cfg["port"],4,cfg["pwd"])
                #res=redisId.srandmember("ipPool",1)[0].strip()
                #urls=res.split(":")
		#request.meta['proxy'] ="http://"+str(urls[0])+":"+str(urls[1])
		request.meta['proxy'] ="http://124.88.67.20:80"
		#print request.meta['proxy'] 
=======
=======
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
		cfg=config("Redis")
		redisId=redis.Redis(cfg["host"],cfg["port"],3,cfg["pwd"])
		res=redisId.srandmember("ipPool",1)[0].strip()
		urls=res.split(":")
		request.meta['proxy'] ="http://"+str(urls[0])+":"+str(urls[1])
		print request.meta['proxy'] 
<<<<<<< HEAD
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
=======
>>>>>>> 7235bd3b1c4452496ce81c35a74b003805fe6394
		# Use the following lines if your proxy requires authentication





		
