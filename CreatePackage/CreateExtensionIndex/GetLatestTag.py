'''
Created on Dec 24, 2015

@author: wujz
'''
import urllib.request,json

RAW_URL = r'https://api.github.com/repos/ibmpredictiveanalytics/{0}/releases/latest?access_token=b703c046b102d5e28df96901844948c376619ffd'
def getLatestTagNO(ext_name):
    url = RAW_URL.format(ext_name)
    tag_info = json.loads(urllib.request.urlopen(url, data=None, timeout=10).read().decode('utf-8'))
    tag_index = tag_info["tag_name"]
    return tag_index
    