'''
Created on Dec 24, 2015

@author: wujz
'''
import urllib.request,json

TOKEN = '4a6db936e057d1832399a91a98a86eddf9a2ed6e'
RAW_URL = r'https://api.github.com/repos/ibmpredictiveanalytics/{0}/releases/latest?access_token={1}'
def getLatestTagNO(ext_name):
    url = RAW_URL.format(ext_name,TOKEN)
	
    try:
        tag_info = json.loads(urllib.request.urlopen(url, data=None, timeout=10).read().decode('utf-8'))
        tag_index = tag_info["tag_name"]
    except urllib.error.HTTPError as e:
	    raise e
    return tag_index
    
