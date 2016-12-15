import hashlib
import json
import os
#MD5 encryption
def md5(addStr):
	m = hashlib.md5()
	m.update(addStr)
	return m.hexdigest()

#JSON to string string
def jsonToStr(scStr,key):
	strs=json.loads(scStr)[key]
	return strs

#Output fail in file
def outPutFaileToFile(info,fileName="outPutFaileToFile.txt",filePath="./"):
	if not os.path.exists(filePath+fileName):
		f=open(filePath+fileName,"w")
		f.close()
	f=open(filePath+fileName,"a+")
	f.write(info+"\n")
	f.close()