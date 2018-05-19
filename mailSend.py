#!/usr/bin/env python
#-*- coding:utf-8 -*-
import encript
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from time import strftime, localtime
import os
from threading import Event, Timer
import xml.etree.cElementTree as ET

base_dir = os.path.dirname(os.path.realpath(__file__))

#try:
xmlServer = ET.parse(base_dir + '/serverConf.xml')
xmlMail = ET.parse(base_dir + '/sendingMail.xml')
server = xmlServer.getroot()
email = xmlMail.getroot()
for i in range(0,len(server)):
	fromaddr = server[0].find('from').text
	print 'from', fromaddr
	toaddr = email.find('to').text.split(',')
	print 'to', toaddr
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = ", ".join(toaddr)
	msg['Subject'] = email.find('konu').text
	body = email.find('text').text
	print 'body', body
	msg.attach(MIMEText(body, 'plain', 'UTF-8'))
	print 'smtp', server[0].find('SMTPAddr').text, int(server[0].find('SMTPPort').text)
	s = smtplib.SMTP_SSL(server[0].find('SMTPAddr').text, int(server[0].find('SMTPPort').text))
	print 'smtp tamam'
	s.login(fromaddr, encript.decode(server[0].find('fromPass').text))
	print 'pass', encript.decode(server[0].find('fromPass').text)
	s.sendmail(fromaddr, toaddr, msg.as_string())
	print 'sending tamam'
	s.quit()
	
#except:
#	pass
