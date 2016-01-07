'''
Created on Jan 6, 2016

@author: wujz
'''
import os,sys,urllib.request,zipfile,json,csv,traceback,time,re,shutil
from EmailSender import emailSender

INDEX_PACKAGE_URL = {'stats':r'https://github.com/IBMPredictiveAnalytics/IBMPredictiveAnalytics.github.io/blob/master/resbundles/statisitcs/extension_index_resbundles.zip?raw=true',
                     'modeler': 'https://github.com/IBMPredictiveAnalytics/IBMPredictiveAnalytics.github.io/blob/master/resbundles/modeler/extension_index_resbundles.zip?raw=true'}
PACKAGE_NAME = 'extension_index_resbundles.zip'
INDEX_FILE = 'extension_info_index.json'
RELEASE_INFO_URL = r'https://api.github.com/repos/{0}/{1}/releases'

def sendRequest(url, method='GET', data=None, headers={}):  
    TOKEN = '86453c61dd94ef247e293cde22934d0758bb2b6d'
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

def getTime(file):
    pat = re.compile(r'(\d{6})')
    time_int = pat.search(file)
    
    if time_int:
        return int(time_int.group())
    else:
        return 0

def getLastFile(hist_folder):
    file_list = os.listdir(hist_folder)
    
    if file_list==None or len(file_list)==0:
        return None
    
    latest = getTime(file_list[0])
    latest_file = file_list[0]
    for item in file_list:
        tmp = getTime(item)
        if tmp > latest:
            latest = tmp
            latest_file = item
    if latest==0:
        return None
    else:
        return latest_file
    
def getLastMonthTotDnCount(hist_folder):
    latest_file = getLastFile(hist_folder)
    
    if latest_file==None:
        return None
    csvfile = open(os.path.join(hist_folder,latest_file), 'r', newline='')
    spamreader = csv.reader(csvfile,delimiter=',', quotechar='|')
    
    tot_dn_list = dict()
    for row in spamreader:
        tot_dn_list[row[0]] = row[2]
    return tot_dn_list

def createCSVFile(url, output_filename, hist_folder):
    path = sys.path[0]
    package_file = os.path.join(path, PACKAGE_NAME)
    
    if os.path.isfile(package_file):
        os.remove(package_file)
    
    last_count_list = getLastMonthTotDnCount(hist_folder)
    try:
        urllib.request.urlretrieve(url, package_file) 
    
        if os.path.isfile(package_file):
            unzip_file(package_file, path)
            ext_name_list = getExtNameList(INDEX_FILE)
            
            csvfile = open(output_filename, 'w', newline='')   
            fieldnames = ['Extension', 'Current Month Download Count', 'Total Download Count'] 
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
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
                            print(count)
                            break
                # first time create csv
                if last_count_list==None:
                    writer.writerow({fieldnames[0]: ext, fieldnames[1]: str(count), fieldnames[2]: str(count)})
                else:
                    last_tot_count = int(last_count_list[ext])
                    month_num = count - last_tot_count
                    writer.writerow({fieldnames[0]: ext, fieldnames[1]: str(month_num), fieldnames[2]: str(count)})
            csvfile.close()
            
            if os.path.isfile(INDEX_FILE):
                os.remove(INDEX_FILE)
            if os.path.isfile(package_file):
                os.remove(package_file)
    except Exception as e:
        raise e

            