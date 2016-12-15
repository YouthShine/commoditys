from commondity.lib.service.redisconnect import *

class GetUrls:
    def getUrls(self,key):
        redis=RedisConnect()
        return redis.getSmembers(key)
