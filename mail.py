#Automation of sending email through console with attachment
#sendemail(from_addr = 'swetha.ravishankar92@gmail.com',
#	to_addr_list = ['swetha.ravishankar92@gmail.com'],
#	cc_addr_list = [],
#	subject = "Test Mail",
#	message = 'Hi,\r\n\nSending Email with attachment\r\n\nRegards,\r\nR Swetha Shankar')

import os
import smtplib
from getpass import getpass
from validate_email import validate_email
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email.MIMEAudio import MIMEAudio
from email.MIMEImage import MIMEImage
from email.mime.application import MIMEApplication
from email import encoders

os.chdir('C:\\Users\\Swetha\\Desktop')

#Create Message
def sendemail(from_addr,to_addr_list,cc_addr_list,subject,message,files,smtpserver = 'smtp.gmail.com:587'):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From']=from_addr
    msg['To'] = to_addr_list
    msg['Cc']= cc_addr_list
    text = message
    msg.attach(MIMEText(text))

    #Mail with attachment
    ctype = "application/octet-stream"
    maintype , subtype = ctype.split('/' , 1)
    if maintype == 'image':
        fp=open(files,'rb')
        part = MIMEImage(fp.read())
        fp.close()
        encoders.encode_base64(part)
        part.add_header('Content-Disposition','attachment',filename = files)
        msg.attach(part)
    elif maintype == 'audio':
        fp = open(files,'rb')
        part = MIMEAudio(fp.read())
        fp.close()
        encoders.encode_base64(part)
        part.add_header('Content-Disposition','attachment',filename = files)
        msg.attach(part)
    else:
        fp = open(files,'rb')
        part = MIMEApplication(maintype,subtype)
        part.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(part)
        part.add_header('Content-Disposition','attachment', filename = files)
        msg.attach(part)
    
    #Login Credentials
    username = from_addr
    password = getpass('Enter Password:')

    #Email Validation
    is_from_valid = validate_email(from_addr,verify=True)
    is_from_mx = validate_email(from_addr,check_mx=True)
    if is_from_valid == True and is_from_mx == True:
        try:
            #Sending Email
            s = smtplib.SMTP(smtpserver)
            s.starttls()
            s.login(username,password)
            s.sendmail(from_addr,to_addr_list,msg.as_string())
            print("Email Sent Successfully..!!")
        finally:
            s.quit()
    else:
        print 'Email Address not Valid'
