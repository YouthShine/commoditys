# -*- coding: utf-8 -*-
from selenium import webdriver
from scrapy.http import HtmlResponse
from scrapy.conf import settings
import os
import time
import sys
class JavaScriptMiddleware(object):
    def process_request(self, request, spider):
            print "PhantomJS is starting..."
            driver = webdriver.PhantomJS()
            # driver = webdriver.Chrome()
            driver.get(request.url)
            
            #pqs add   
            js="var q=document.documentElement.scrollTop=10000"
            driver.execute_script(js)
            #
            
            time.sleep(3)
            body = driver.page_source
            # driver.close()
            return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)