"""

Created on Jan 6, 2016

@author: wujz

"""
import os
import sys
import urllib.request
import zipfile
import json
import csv
import datetime
import re
from DnCountObj import DnCountObj
from HistCSVParser import HistCSVParser

INDEX_PACKAGE_URL = \
    {
        'stats':
        r'https://github.com/IBMPredictiveAnalytics/IBMPredictiveAnalytics.github.io/'
        r'blob/master/resbundles/statisitcs/extension_index_resbundles.zip?raw=true',

        'modeler':
        r'https://github.com/IBMPredictiveAnalytics/IBMPredictiveAnalytics.github.io/'
        r'blob/master/resbundles/modeler/extension_index_resbundles.zip?raw=true'
    }

PACKAGE_NAME = r'extension_index_resbundles.zip'
INDEX_FILE = r'extension_info_index.json'
RELEASE_INFO_URL = r'https://api.github.com/repos/{0}/{1}/releases'
HIST_EXT_CSV_COL = ['Extension', 'Current Month Download Count']
HIST_R_ESSENTIALS_CSV_COL = ['R Essentials', 'Current Month Download Count']


def send_request(url, method='GET', data=None, headers={}):
    token = ''
    try:
        if data is not None:
            data = data.encode('utf-8')
        request = urllib.request.Request(url, data)
        request.method = method
        request.add_header("Authorization", "token "+token)
        for key in headers.keys():
            request.add_header(key, headers[key])
        
        try:    
            response = urllib.request.urlopen(request, timeout=50)
        except Exception as e:
            raise e
        
        feedback_info = None 
        if str.upper(method) == 'GET':
            if 200 <= response.status < 300:
                feedback_info = response.read().decode('utf-8')
            else:
                raise Exception("Cannot get release information from api.github.com!")
        elif str.upper(method) == 'POST':
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


def unzip_file(zip_filename, unzip_to_dir):
    if not os.path.exists(unzip_to_dir):
        os.mkdir(unzip_to_dir)
        
    zf_obj = zipfile.ZipFile(zip_filename)
    for name in zf_obj.namelist():
        name = name.replace('\\','/')
        
        if name.endswith('/'):
            continue
        else:            
            if INDEX_FILE in name:
                ext_filename = os.path.join(unzip_to_dir, name)
                outfile = open(ext_filename, 'wb')
                outfile.write(zf_obj.read(name))
                outfile.close()
                break
    zf_obj.close()


def get_ext_name_list(index_file_path):
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


def get_time(file):
    pat = re.compile(r'(\d{6})')
    time_int = pat.search(file)
    
    if time_int:
        return int(time_int.group())
    else:
        return 0


def set_dn_count_info(hist_dn_count_obj, hist_folder):
    # list history download count files
    file_list = os.listdir(hist_folder)

    for item in file_list:
        hist_csv_parser = HistCSVParser(os.path.join(hist_folder, item))

        for row in hist_csv_parser.get_data_list():
            hist_dn_count_obj.add_dn_count(row[0], row[1], get_time(item))


def get_datetime_list(hist_folder):
    filename_list = list()
    
    for item in os.listdir(hist_folder):
        filename_list.append(get_time(item))

    return filename_list


def create_hist_csv_file(hist_csv_filename, hist_folder, cur_dn_info):
    csv_file = open(os.path.join(hist_folder, hist_csv_filename), 'w', newline='')
    writer = csv.DictWriter(csv_file, fieldnames=HIST_EXT_CSV_COL)
    writer.writeheader()
    
    cur_dn_info.sort()
    for item in cur_dn_info:
        writer.writerow({HIST_EXT_CSV_COL[0]: item[0], HIST_EXT_CSV_COL[1]: item[1]})
    csv_file.close()


def create_r_essentials_dn_count_file(output_filename, hist_folder, r_essential_list, main_logger):
    ext_hist_dn_count_obj = DnCountObj()
    set_dn_count_info(ext_hist_dn_count_obj, hist_folder)

    # get lats month string
    des_month_digit = ''.join(str(datetime.date.today() - datetime.timedelta(days=1)).split('-'))[:-2]
    main_logger.info(str(des_month_digit) + " R essential Download Count Report execution started ...")

    cur_dn_info = list()
    for item in r_essential_list.keys():
        count = get_release_tot_dn_count(RELEASE_INFO_URL.format('ibmpredictiveanalytics', item), r_essential_list[item])
        cur_count = count - ext_hist_dn_count_obj.get_tot_dn_count(item)
        cur_dn_info.append((item, str(cur_count)))
        ext_hist_dn_count_obj.add_dn_count(item, cur_count, des_month_digit)

    main_logger.info("start output general " + output_filename)
    ext_hist_dn_count_obj.output_csv_file(output_filename)

    main_logger.info("start output history " + output_filename)
    create_hist_csv_file(os.path.basename(output_filename).split('.')[0] + str(des_month_digit) + '.csv',
                         hist_folder, cur_dn_info)


"""

@param url: get index package url
@param output_file_name: csv file name
@param hist_folder: folder store history download count

"""


def create_csv_file(url, output_filename, hist_folder, main_logger):
    path = sys.path[0]
    package_file = os.path.join(path, PACKAGE_NAME)
    
    if os.path.isfile(package_file):
        os.remove(package_file)
    
    ext_hist_dn_count_obj = DnCountObj()
    set_dn_count_info(ext_hist_dn_count_obj, hist_folder)

    # get lats month string
    des_month_digit = ''.join(str(datetime.date.today() - datetime.timedelta(days=1)).split('-'))[:-2]

    main_logger.info(str(des_month_digit) + " Download Count Report execution started ...")
    try:
        urllib.request.urlretrieve(url, package_file) 
        
        if os.path.isfile(package_file):
            unzip_file(package_file, path)
            ext_name_list = get_ext_name_list(INDEX_FILE)
            cur_dn_info = list()

            for ext in ext_name_list:
                count = get_release_tot_dn_count(RELEASE_INFO_URL.format('ibmpredictiveanalytics', ext), ext)
                        
                cur_count = count - ext_hist_dn_count_obj.get_tot_dn_count(ext)
                cur_dn_info.append((ext, str(cur_count)))
                ext_hist_dn_count_obj.add_dn_count(ext, cur_count, des_month_digit)
            
            main_logger.info("start output general " + output_filename)
            ext_hist_dn_count_obj.output_csv_file(output_filename)

            main_logger.info("start output history " + output_filename)
            create_hist_csv_file(os.path.basename(output_filename).split('.')[0] + str(des_month_digit) + '.csv',
                                 hist_folder, cur_dn_info)

            if os.path.isfile(INDEX_FILE):
                os.remove(INDEX_FILE)
            if os.path.isfile(package_file):
                os.remove(package_file)
    except Exception as e:
        raise e


def get_release_tot_dn_count(release_url, repo_name):
    try:
        content = json.loads(send_request(release_url, method='GET'))
    except Exception as e:
        raise e

    count = 0
    for release in content:
        assets = release['assets']
        for asset in assets:
            if repo_name in asset['name']:
                count += int(asset['download_count'])
                continue
    return count

if __name__ == '__main__':
    create_r_essentials_dn_count_file()
