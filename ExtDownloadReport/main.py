'''
Created on Jan 6, 2016

@author: wujz
'''
import traceback,time
from DownloadCount import getExtList,INDEX_PACKAGE_URL
from EmailSender import emailSender

def main():
    cur_month = time.strftime('%b, %Y',time.localtime(time.time()))
    while True:
        month = time.strftime('%b, %Y',time.localtime(time.time()))
        
        if month == cur_month:
            time.sleep(86400)
            continue
        else:
            cur_month = month      
            try:
                getExtList(INDEX_PACKAGE_URL['stats'])
                getExtList(INDEX_PACKAGE_URL['modeler'])
                
                mailSender = emailSender(['stats_download_count.csv', 'modeler_download_count.csv'])    
                MESSAGE = "Report Month: {0}\nMailServer: 9.30.199.60:25\nSee detalied information in the attachment.\n"
                mailSender.sendEmail(MESSAGE.format(cur_month))
            except Exception:
                traceback.print_exc()
                exit(1)

def test():
    try:
        getExtList(INDEX_PACKAGE_URL['modeler'], 'modeler')
        getExtList(INDEX_PACKAGE_URL['stats'], 'stats')
        
        cur_month = time.strftime('%b, %Y',time.localtime(time.time()))
        mailSender = emailSender(['stats_download_count.csv', 'modeler_download_count.csv'])    
        MESSAGE = "Report Month: {0}\nMailServer: 9.30.199.60:25\nSee detalied information in the attachment.\n"
        mailSender.sendEmail(MESSAGE.format(cur_month))
    except Exception:
        traceback.print_exc()
        exit(1)
        
if __name__=='__main__':
    test()
    #main()
