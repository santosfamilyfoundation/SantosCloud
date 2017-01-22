
import os
import smtplib
import utils

class EmailHelper(object):
	def __init__(self):
		pass

	def send_email(self, to_addr, subject, message):
		email = os.environ.get('TRAFFICCLOUD_EMAIL')
		password = os.environ.get('TRAFFICCLOUD_PASSWORD')

		text = "From: Traffic Cloud <"+email+">\nTo: "+to_addr+"\nSubject: "+subject+"\n"+message
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.starttls()
		server.login(email, password)
		server.sendmail(email, to_addr, text)
		server.quit()
