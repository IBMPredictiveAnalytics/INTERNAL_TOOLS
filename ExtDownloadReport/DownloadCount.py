'''
Created on Jan 6, 2016

@author: wujz
'''
import os,sys,urllib.request,zipfile,json,csv,traceback,time
from EmailSender import emailSender

INDEX_PACKAGE_URL = {'stats':r'https://github.com/IBMPredictiveAnalytics/IBMPredictiveAnalytics.github.io/blob/master/resbundles/statisitcs/extension_index_resbundles.zip?raw=true',
                     'modeler': 'https://github.com/IBMPredictiveAnalytics/IBMPredictiveAnalytics.github.io/blob/master/resbundles/modeler/extension_index_resbundles.zip?raw=true'}
PACKAGE_NAME = 'extension_index_resbundles.zip'
INDEX_FILE = 'extension_info_index.json'
RELEASE_INFO_URL = r'https://api.github.com/repos/{0}/{1}/releases'

def sendRequest(url, method='GET', data=None, headers={}):  
    TOKEN = 'YOUR_TOKEN'
    try:
        if data!=None:
            data = data.encode('utf-8')
        request = urllib.request.Request(url, data)
        request.method = method
        request.add_header("Authorization", "token "+TOKEN)
        for key in headers.keys():
            request.add_header(key, headers[key])
        
        try:    
            print(url)
            response = urllib.request.urlopen(request,timeout=50)
        except Exception as e:
            raise e
        
        feedback_info = None 
        if str.upper(method)=='GET':
            if 200 <= response.status < 300:
                print("GET info successfully!")
                feedback_info = response.read().decode('utf-8')
            else:
                raise Exception("Cannot get release information from api.github.com!")
        elif str.upper(method)=='POST':
            if 200 <= response.status < 300:
                print(response.status)
                print("POST info successfully!")
            else:
                raise Exception("Cannot get post data to api.github.com!")  
        elif str.upper(method) == 'DELETE': 
            if 200 <= response.status < 300: 
                print("request is done!")
                print(response.status)
            else:
                raise Exception("request to api.github.com failed!")  
        else:
            print("Wrong method!")
    except Exception as e:
        raise e
    return feedback_info

def unzip_file(zipfilename, unziptodir):
    if not os.path.exists(unziptodir): os.mkdir(unziptodir)
    zfobj = zipfile.ZipFile(zipfilename)
    for name in zfobj.namelist():
        name = name.replace('\\','/')
        
        if name.endswith('/'):
            continue
        else:            
            if INDEX_FILE in name:
                ext_filename = os.path.join(unziptodir, name)
                outfile = open(ext_filename, 'wb')
                outfile.write(zfobj.read(name))
                outfile.close()
                break
    zfobj.close()

def getExtNameList(index_file_path):
    ext_name_list = list()
    if os.path.isfile(index_file_path):
        fp = open(index_file_path, 'r', encoding='utf8')
        ext_list = json.loads(fp.read())
        ext_list = ext_list["extension_index"]
        fp.close()
        for item in ext_list:
            ext_name_list.append(item["repository"])
    else:
        raise Exception('Cannot find index file')
    return ext_name_list

def getExtList(url, product):
    path = sys.path[0]
    print(path)
    package_file = os.path.join(path, PACKAGE_NAME)
    
    if os.path.isfile(package_file):
        os.remove(package_file)
    
    try:
        urllib.request.urlretrieve(url, package_file) 
    
        if os.path.isfile(package_file):
            unzip_file(package_file, path)
            ext_name_list = getExtNameList(INDEX_FILE)
            
            csvfile = open('{0}_exts_download_count.csv'.format(product), 'w', newline='')   
            fieldnames = ['Extension', 'Download Count'] 
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            tot_count = 0
            for ext in ext_name_list:
                url = RELEASE_INFO_URL.format('ibmpredictiveanalytics',ext)
                try:
                    content = json.loads(sendRequest(url, method='GET'))
                except Exception as e:
                    raise e
                print(ext)
                count = 0
                for release in content:
                    assets = release['assets']
                    for asset in assets:
                        if ext in asset['name']:
                            count += int(asset['download_count'])
                            tot_count += count
                            print(count)
                            break
                writer.writerow({'Extension': ext, 'Download Count': str(count)})
            writer.writerow({'Extension': 'totoal download count', 'Download Count': str(tot_count)})
            csvfile.close()
            
            if os.path.isfile(INDEX_FILE):
                os.remove(INDEX_FILE)
            if os.path.isfile(package_file):
                os.remove(package_file)
    except Exception as e:
        raise e
        
if __name__ == '__main__':
    try:
        getExtList(INDEX_PACKAGE_URL['stats'])
    except Exception as e:
        traceback.print_exc()
    mailSender = emailSender(['stats_download_count.csv'])
    month = time.strftime('%b, %Y',time.localtime(time.time()))
    print(month)
    MESSAGE = "Report Month: {0}\nMail Server: 9.30.199.60:25\nSee detalied information in the attachment.\n"
    mailSender.sendEmail(MESSAGE.format(month))
            