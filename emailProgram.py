#Author: Jared Noble 04/18/2018
#Intention of this project is to create an email spoofing program that takes the input of what I want to spoof as, and specify a target address.

import smtplib
import getpass
import smtpServer_m #broken, needs attention
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

username = input('Enter your email address: ')
password = getpass.getpass('Enter your password: ')
targetEmail = input('Enter the target email address: ')
subjectLine = input('Enter the subject: ')
bodyEmail = input('What woud you like to tell ' + targetEmail + '? ' )

################Server Selection Section#############################
#wanting to add functionality to select between gmail/yahoo/etc. email servers
#Check for input from username and automatically assign smpt server

if "gmail" in username.lower():
	print("found 'gmail' in your input..")
	serverLoc = 'smtp.gmail.com'
	serverPort = 587
elif "outlook" in username.lower():
	print("found 'outlook' in your input..")
	serverLoc = 'smtp.live.com'
	serverPort = 587
elif "office" in username.lower():
	print("found 'office' in your input..")
	serverLoc = 'smtp.office365.com'
	serverPort = 587
elif "yahoo" in username.lower():
	print("found 'yahoo' in your input..")
	serverLoc = 'smtp.mail.yahoo.com'
	serverPort = 465
elif "aol" in username.lower():
	print("found 'aol' in your input..")
	serverLoc = 'smtp.aol.com'
	serverPort = 587
elif "att" in username.lower():
	print("found 'att' in your input..")
	serverLoc = 'smtp.att.yahoo.com'
	serverPort = 587
elif "hotmail" in username.lower():
	print("found 'hotmail' in your input..")
	serverLoc = 'smtp.live.com'
	serverPort = 465
elif "verizon" in username.lower():
	print("found 'verizon' in your input..")
	serverLoc = 'outgoing.verizon.net'
	serverPort = 465
elif "mail" in username.lower():
	print("found 'mail' in your input..")
	serverLoc = 'smtp.mail.com'
	serverPort = 587
else:
	print("did not find 'valid smtp server'")
#####################################################################

msg = MIMEMultipart()
msg['From'] = username
msg['To'] = targetEmail
msg['Subject'] = subjectLine
message = bodyEmail
msg.attach(MIMEText(message))

#587 is the tls port used w/SMTP. To adjust the server service, change the gmail part
#Pulled from 
mailserver = smtplib.SMTP(serverLoc, serverPort)

# identify ourselves to smtp gmail client w/extended hello
mailserver.ehlo()

# secure our email with tls encryption
mailserver.starttls()

# re-identify ourselves as an encrypted connection. haven't decided if this matters
#mailserver.ehlo()

#user/pass arguments
mailserver.login(username, password)

#ready to send the email
mailserver.sendmail(username,targetEmail,msg.as_string())


#kill connection
mailserver.quit()
