'''
Created on Jan 6, 2016

@author: wujz
'''
import traceback,time,os,sys,shutil
from DownloadCount import createCSVFile,INDEX_PACKAGE_URL
from EmailSender import emailSender

def main():     
    cur_month = time.strftime('%b, %Y',time.localtime(time.time()))
    cur_month_digit = time.strftime('%Y%m',time.localtime(time.time()))
    
    root_path = sys.path[0]
    stats_his_folder = os.path.join(root_path,'stats_history')
    if not os.path.isdir(stats_his_folder):
        os.mkdir(stats_his_folder)
        
    modeler_his_folder = os.path.join(root_path,'modeler_history')
    if not os.path.isdir(modeler_his_folder):
        os.mkdir(modeler_his_folder)
    
    # first time run script
    stats_csv_file = 'stats_download_count.csv'
    modeler_csv_file = 'modeler_download_count.csv'
    
    isNotFirstTime = False
    while True:
        month = time.strftime('%b, %Y',time.localtime(time.time()))
        month_digit = time.strftime('%Y%m',time.localtime(time.time()))
        
        if month == cur_month and isNotFirstTime:
            print("Wait for another month!")
            time.sleep(86400)
            continue
        else:    
            try:
                print("New month came. Start to create download count files for last month!")
                createCSVFile(INDEX_PACKAGE_URL['stats'], stats_csv_file, stats_his_folder)
                createCSVFile(INDEX_PACKAGE_URL['modeler'], modeler_csv_file, modeler_his_folder)
                
                mailSender = emailSender([stats_csv_file, modeler_csv_file])    
                MESSAGE = "Report Month: {0}\nMail Server: 9.30.199.60:25\nSee detalied information in the attachment.\n"
                mailSender.sendEmail(MESSAGE.format(cur_month))
                
                cur_stats_csv_file = stats_csv_file[:-4]+str(cur_month_digit)+'.csv'
                cur_modeler_csv_file = modeler_csv_file[:-4]+str(cur_month_digit)+'.csv'
                
                shutil.copyfile(stats_csv_file, os.path.join(stats_his_folder,cur_stats_csv_file))
                shutil.copyfile(stats_csv_file, os.path.join(modeler_his_folder,cur_modeler_csv_file))
                
                cur_month = month 
                cur_month_digit = month_digit
                isNotFirstTime = True 
            except Exception:
                traceback.print_exc()
                exit(1)
        
if __name__=='__main__':
    main()
