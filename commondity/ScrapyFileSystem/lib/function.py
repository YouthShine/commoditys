import shutil
shutil.copy("commondity/ScrapyFileSystem/config.py","commondity/ScrapyFileSystem/lib/tempConfig.py")
from Log.logOutput import *
from Redis.redisConnect import *
from Mongodb.mongodbConnect import *
import hashlib

#MD5 encryption
def md5(addStr):
	m = hashlib.md5()
	m.update(addStr)
	return m.hexdigest()


