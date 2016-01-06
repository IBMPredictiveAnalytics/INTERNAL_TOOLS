'''
Created on Jan 6, 2016

@author: wujz
'''
import smtplib,traceback,os,mimetypes,time
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText 
from email.mime.audio import MIMEAudio
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from email.encoders import encode_base64
            
class emailSender(object):     
    def __init__(self, file_name):       
        # mail server 
        self.server = None
        self.mail_host="9.30.199.60"
        self.mail_port=25
        
        # mail sener info
        self.mail_user="report"
        self.mail_postfix="extdownload"
        self.mailto_list = ['gfilla@us.ibm.com','fanyey@cn.ibm.com','dstauber@us.ibm.com',
                            'wujz@cn.ibm.com','dunworth@uk.ibm.com','rjcohen@us.ibm.com'] 
        
        # attachment name
        self.file_name = file_name
        
        try:
            self.server = smtplib.SMTP()
            self.server.connect(self.mail_host,self.mail_port)
        except Exception:
            traceback.print_exc()
    
    def close(self):
        if self.server != None:
            self.server.close()     
            self.server = None 
    
    def sendEmail(self, message):
        try:
            # mail headers
            sender = "<"+self.mail_user+'@'+self.mail_postfix+">"
            msg = MIMEMultipart() 
            msg['Subject'] = "Extensions Download Count Monthly Report "
            msg['From'] = sender
            msg['To'] = ";".join(self.mailto_list)
            msg['Date'] = formatdate()
            
            body_msg = MIMEText(message, _subtype='plain')
            msg.attach(body_msg)
            
            for file_name in self.file_name:
                if not os.path.isfile(file_name):
                    raise Exception("Cannot find "+file_name)
                      
                ctype, encoding = mimetypes.guess_type(file_name) 
                if ctype is None or encoding is not None:
                    # No guess could be made, or the file is encoded (compressed), so
                    # use a generic bag-of-bits type.
                    ctype = 'application/octet-stream'
                    
                maintype, subtype = ctype.split('/', 1)
                if maintype == 'text':
                    with open(file_name) as fp:
                        # Note: we should handle calculating the charset
                        file_msg = MIMEText(fp.read(), _subtype=subtype)
                elif maintype == 'image':
                    with open(file_name, 'rb') as fp:
                        file_msg = MIMEImage(fp.read(), _subtype=subtype)
                elif maintype == 'audio':
                    with open(file_name, 'rb') as fp:
                        file_msg = MIMEAudio(fp.read(), _subtype=subtype)
                else:
                    with open(file_name, 'rb') as fp:
                        file_msg = MIMEBase(maintype, subtype)
                        file_msg.set_payload(fp.read())
                    # Encode the payload using Base64
                    file_msg.add_header('Content-Disposition','attachment', filename = file_name) 
                    encode_base64(file_msg)
                fp.close()
                msg.attach(file_msg)  
                
            content = msg.as_string()
            self.server.sendmail(sender,self.mailto_list,content)
        except Exception as e:
            raise e
        finally:
            self.close()

if __name__=='__main__':
    month = time.strftime('%b, %Y',time.localtime(time.time()))
    print(month)
    eSender = emailSender(r'C:\Users\wujz\Desktop\format.csv')
    MESSAGE = "Report Month: {0}\n"+"MailServer: 9.30.199.60:25\n" +"Top 10 Extensions: \nSee detalied information in the attachment."
    eSender.sendEmail(MESSAGE.format(month))