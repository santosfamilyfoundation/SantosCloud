
import auth
import smtplib
import utils

class EmailHelper(object):
    def __init__(self):
        pass

    def send_email(self, to_addr, subject, message):
        text = "From: Traffic Cloud <"+auth.email+">\nTo: "+to_addr+"\nSubject: "+subject+"\n"+message
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(auth.email,auth.password)
        server.sendmail(auth.email, to_addr, text)
        server.quit()
