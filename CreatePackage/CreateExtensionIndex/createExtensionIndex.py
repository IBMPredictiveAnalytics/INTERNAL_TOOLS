'''
Created on Oct 22, 2015

@author: wujz
'''
# -*- coding: utf-8 -*-  
from CreateExtensionIndex.GithubApiInfoObj import GithubApiInfoObj
from CreateExtensionIndex.InfoJSONObj import InfoJSONObj
from CreateExtensionIndex.MetaObj import MetaObj
from common.Logger import Logger

import socket,urllib.request,zipfile,os,time,shutil

#"https://github.com/IBMPredictiveAnalytics/repos_name/blob/master/repos_name.spe?raw=true"
EXT_CONTENT_URL = "https://github.com/IBMPredictiveAnalytics/{0}/raw/master/{1}"
#SPE_DOWNLOAD_URL = "https://github.com/IBMPredictiveAnalytics/repos_name/raw/master/repos_name.spe"
IMG_DOWNLOAD_URL = "https://raw.githubusercontent.com/IBMPredictiveAnalytics/{0}/master/default.png"
FILE_NAME= "MANIFEST.MF"
RAW_INDEX_FILE = 'extension_info_index.json'
INDENT = '\t'
LOG_INFO = "createExtensionIndex.log"
META_DIR = 'META-INF' 
TIMEOUT = 600     
LOG_DIR_NAME = 'log'
START_WORD = 'extension_index'

def createExtensionIndex(*args):
    socket.setdefaulttimeout(TIMEOUT)
    indexdir = args[0]
    product = args[1]
    
    if product=='stats':
        tail = '.spe'
    else: 
        tail = '.mpe'  
         
    cur_time = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))  
    root_content_dir = os.path.join(indexdir,tail+cur_time) 
    root_log_dir = os.path.join(indexdir, LOG_DIR_NAME)   
    
    if not os.path.exists(root_log_dir):
        os.mkdir(root_log_dir)
       
    try:
        os.mkdir(root_content_dir)            
        extLogger = Logger(os.path.join(root_log_dir,LOG_INFO),'extLogger')
        extLogger.info("CreateExtensionIndex script start ...")
    except IOError as e:  
        raise IOError("IOError: Need permission to write in "+indexdir+ " or this folder does not exist")
    
    index_for_extension = "{\n\""+START_WORD+"\":[\n"
    whole_product_name = getWholeProductName(product) 
    extLogger.info("start to get repo data from github ...")
    ext_output_path = os.path.join(indexdir, RAW_INDEX_FILE)
    
    i=0
    ok_repo_num = 0
    try:        
        githubApiInfo_obj = GithubApiInfoObj()
        for item in githubApiInfo_obj.item_list:
            i+=1
            
            index_for_extension_item = INDENT+"{\n"
            index_for_extension_item += generateJSONStr(item)
            
            repo_name = item[githubApiInfo_obj.__class__.REPOSITORY].val
            extLogger.info(str(i)+" repo: "+repo_name)

            try:
                info_json = InfoJSONObj(repo_name)
            except ValueError as e:
                raise e
            except Exception as e:
                extLogger.warning(str(e))
                continue
                
            index_for_extension_item += generateJSONStr(info_json.item_list)
            repo_software = info_json.item_list[info_json.__class__.SOFTWARE].val
                      
            content_name = repo_name+tail  
            repo_content_url = EXT_CONTENT_URL.format(repo_name,content_name)
            repo_img_url = IMG_DOWNLOAD_URL.format(repo_name)
                    
            index_for_extension_item += INDENT*2 + "\"download_link\":" +"\"" + repo_content_url +"\",\n"
            index_for_extension_item += INDENT*2 + "\"image_link\":" +"\"" + repo_img_url +"\",\n"
            
            if repo_software != whole_product_name:
                extLogger.info("This is not a " + whole_product_name + " repo. Switch to next repo.")
                continue
            
            content_saving_path = os.path.join(root_content_dir,repo_name)
            os.mkdir(content_saving_path)
            
            try:
                urllib.request.urlretrieve(repo_content_url, os.path.join(content_saving_path,content_name))
            except:
                extLogger.warning("This repo '"+repo_name+" does not have "+tail+" package. Please check! Switch to next repo.")
                continue
            
            srcZip = zipfile.ZipFile(os.path.join(content_saving_path,content_name), "r", zipfile.ZIP_DEFLATED)
            for file in srcZip.namelist():
                if not os.path.isdir(content_saving_path):     
                    os.mkdir(content_saving_path)
                if FILE_NAME in file:
                    srcZip.extract(file, content_saving_path)
            srcZip.close()
            
            meta_path = os.path.join(content_saving_path, META_DIR, FILE_NAME)
            metaObj = MetaObj(meta_path)
            index_for_extension_item += metaObj.generateExtensionJSON()
            index_for_extension_item += INDENT + "},\n" 
            index_for_extension += index_for_extension_item
            ok_repo_num += 1
            extLogger.info("Successfully get data!")

        index_for_extension = index_for_extension[0:-2]
        index_for_extension += '\n]\n}'
        index_for_extension_fp = open(ext_output_path,'w', encoding='utf-8')
        index_for_extension_fp.write(index_for_extension)  
        index_for_extension_fp.close()   
        extLogger.info("CreateIndexForDownloadExtensiosn action succeeded!") 
        extLogger.info("Extension index file has been saved in "+ext_output_path)
    except Exception as e:        
        extLogger.error(str(e), e)
        extLogger.info("CreateIndexForDownloadExtensiosn action failed!")
        raise e
    finally:
        extLogger.info("Totally get "+str(ok_repo_num)+" repo data.")
        clear(root_content_dir)

    if not os.path.exists(ext_output_path):
        raise Exception("Fail to create extension index file! Please contact github administrator!")   
    
    return ext_output_path
            
            
def getWholeProductName(product_name):
    if(product_name.lower() == "stats"):
        return "SPSS Statistics"
    else:
        return "SPSS Modeler"

def generateJSONStr(json_obj_list):
    json_item_str =''
    for item in json_obj_list:            
        json_item_str += INDENT*2 + item.getJSONStr() 
    return json_item_str

def clear(contentdir):
    if os.path.isdir(contentdir):
        os.system(r"C:\Windows\System32\attrib -r "+ contentdir+"\*.* " + " /s /d")
        shutil.rmtree(contentdir, ignore_errors = True) 
    