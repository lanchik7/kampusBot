import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config


def send_email(to_addr, subject, text):
    msg = MIMEMultipart()
    msg['From'] = config.login
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg.attach(MIMEText(text, 'plain'))

    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.ehlo(config.login)
    server.login(config.login, config.password)
    server.auth_plain()
    server.send_message(msg)
    server.quit()



# import necessary packages

# from email.mime.multipart import MIMEMultipart
#
# from email.mime.text import MIMEText
#
# import smtplib
#
# # create message object instance
#
# msg = MIMEMultipart()
#
# message = "Thank you"
#
# # setup the parameters of the message
#
# password = "your_password"
#
# msg['From'] = "your_address"
#
# msg['To'] = "to_address"
#
# msg['Subject'] = "Subscription"
#
# # add in the message body
#
# msg.attach(MIMEText(message, 'plain'))
#
# #create server
#
# server = smtplib.SMTP('smtp.gmail.com: 587')
#
# server.starttls()
#
# # Login Credentials for sending the mail
#
# server.login(msg['From'], password)
#
# # send the message via the server.
#
# server.sendmail(msg['From'], msg['To'], msg.as_string())
#
# server.quit()
#
# print "successfully sent email to %s:" % (msg['To'])
