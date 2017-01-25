
import os
import smtplib
import utils

class EmailHelper(object):
    def __init__(self):
        pass

<<<<<<< HEAD
    def send_email(self, to_addr, subject, message):
        text = "From: Traffic Cloud <"+auth.email+">\nTo: "+to_addr+"\nSubject: "+subject+"\n"+message
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(auth.email,auth.password)
        server.sendmail(auth.email, to_addr, text)
        server.quit()
=======
	def send_email(self, to_addr, subject, message):
		email = os.environ.get('TRAFFICCLOUD_EMAIL')
		password = os.environ.get('TRAFFICCLOUD_EMAIL_PASSWORD')

    	if email == '' or password == '' or email == None or password == None:
    		print("WARNING: No email provided, failed to email user.")
    		return

		text = "From: Traffic Cloud <"+email+">\nTo: "+to_addr+"\nSubject: "+subject+"\n"+message
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.starttls()
		server.login(email, password)
		server.sendmail(email, to_addr, text)
		server.quit()
>>>>>>> master
