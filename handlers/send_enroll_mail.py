import os
import smtplib
import threading
from random import randint

# from createProfile import *


class MailSenderThread(threading.Thread):

    error = None
    def __init__(self, link, password, recipient):
        threading.Thread.__init__(self)
        print 'IN MailSender\'s init'
        
        self.link = link
        self.password = password
        self.recipient = recipient
        print self.link
        

            
    def run(self):     
#             "Sends an e-mail to the specified recipient."
            print 'In MailSender\'s run'
            msg = 'Your download link is.'  + str(self.link) + ' and enrollment password is ' + self.password
            body = "<html><head></head><body><pre>" + msg + "</pre></body></html>"
            sender = 'rk12aaa@gmail.com'
            headers = ["From: " + sender,
                       "Subject: " + 'Enrollment',
                       "To: " + self.recipient,
                       "MIME-Version: 1.0",
                       "Content-Type: text/html"]
            headers = "\r\n".join(headers)
        
            # Credentials (if needed)
            username = 'rk12aaa'
            password = 'comedycircus'
 
            # The actual mail send
            try:
                server = smtplib.SMTP('smtp.gmail.com:587')
                server.starttls()
                server.login(username,password)

                server.sendmail(sender, self.recipient, headers + "\r\n\r\n" + body)                
                server.quit()
                print 'Mail Sent Successfully to ' + self.recipient
                self.error = None
            except:
                print 'Some Errors in sending the mail please check the email or the sender\'s configuration'
                self.error = 1


# if __name__ == '__main__':
#     s = MailSenderThread()
