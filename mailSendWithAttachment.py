import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from time import strftime, localtime
import os
from glob import glob
from threading import Event, Timer

base_dir = os.path.dirname(os.path.realpath(__file__))

plcList={'192.168.1.202':{'pass':'aNk@574725','path':['/usr/local/plc/plc.log']},'192.168.1.203':{'pass':'aNk@574725','path':['/usr/local/plc/plc.log']},
	 '192.168.1.204':{'pass':'raspberry','path':['/usr/local/plc/plc.log']},'192.168.1.205':{'pass':'aNk@574725','path':['/usr/local/plc/plc.log']},
	 '192.168.1.206':{'pass':'aNk@574725','path':['/usr/local/plc/plc.log']},'192.168.1.207':{'pass':'aNk@574725','path':['/usr/local/plc/app/plc.log','/usr/local/plc/app/plcSys.log']},
	 '192.168.1.208':{'pass':'aNk@574725','path':['/usr/local/plc/plc.log']},'192.168.1.209':{'pass':'aNk@574725','path':['/usr/local/plc/plc.log']},
	 '192.168.1.210':{'pass':'aNk@574725','path':['/usr/local/plc/plc.log']},'192.168.1.211':{'pass':'aNk@574725','path':['/usr/local/plc/plc.log']},
	 '192.168.1.212':{'pass':'raspberry','path':['/usr/local/plc/app/plc.log','/usr/local/plc/app/plcSys.log']},
	 '192.168.1.213':{'pass':'raspberry','path':['/usr/local/plc/app/plc.log','/usr/local/plc/app/plcSys.log']},
	 '192.168.1.214':{'pass':'raspberry','path':['/usr/local/plc/plc.log']},'192.168.1.215':{'pass':'raspberry','path':['/usr/local/plc/plc.log']},
	 '192.168.1.216':{'pass':'raspberry','path':['/usr/local/plc/plc.log']},'192.168.1.217':{'pass':'raspberry','path':['/usr/local/plc/plc.log']},
	 '192.168.1.218':{'pass':'raspberry','path':['/usr/local/plc/app/plc.log','/usr/local/plc/app/plcSys.log']},'192.168.1.219':{'pass':'raspberry','path':['/usr/local/plc/plc.log']},
	 '192.168.1.220':{'pass':'raspberry','path':['/usr/local/plc/plc.log']},'192.168.1.221':{'pass':'raspberry','path':['/usr/local/plc/plc.log']},
	 '192.168.1.222':{'pass':'raspberry','path':['/usr/local/plc/plc.log']},'192.168.1.223':{'pass':'raspberry','path':['/usr/local/plc/plc.log']},
	 '192.168.1.224':{'pass':'raspberry','path':['/usr/local/plc/plc.log']}}

notConnected=[]

gunEvent=Event()
gunEvent.clear()

fromaddr = "nisradestek@gmail.com"
toaddr = "nisradestek@gmail.com"
format='%Y/%m/%d %H:%M:%S'

def gunTemizle():
	global gunEvent
	gunEvent.set()

while True:
	try:
		timer=Timer(86400,gunTemizle)
		timer.start()
		gunEvent.clear()
		os.system("cp /usr/local/plc/app/server.log %s/loglar/201server.log")
		os.system("truncate -s 0 /usr/local/plc/app/server.log")
		os.system("cp /usr/local/plc/app/serverSys.log %s/loglar/201serverSys.log")
		os.system("truncate -s 0 /usr/local/plc/app/serverSys.log")
		for i in plcList:
			for j in plcList[i]['path']:
				response=os.system("sshpass -p '{1}' scp root@{0}:{2} ./loglar/{3}".format(i,plcList[i]['pass'],j,(i.split('.')[-1]+j.split('/')[-1])))
				if not response:
					if not i in notConnected:
						notConnected.append(i)
					continue
				os.system("sshpass -p '{1}' ssh root@{0} truncate -s 0 {2}".format(i,plcList[i]['pass'],j))
		msg = MIMEMultipart()
		msg['From'] = fromaddr
		msg['To'] = toaddr
		msg['Subject'] = strftime(format,localtime())
		body = strftime(format,localtime())+" log dosyaları."
		msg.attach(MIMEText(body, 'plain'))
		
		loglar=glob(base_dir+"/loglar/*.log")
		for i in loglar
			filename = i.split('/')[-1]
			attachment = open(i, "rb")
			p = MIMEBase('application', 'octet-stream')
			p.set_payload((attachment).read())
			encoders.encode_base64(p)
			p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
			msg.attach(p)
		
		s = smtplib.SMTP('smtp.gmail.com', 587)
		s.starttls()
		s.login(fromaddr, "123456789nisra")
		text = msg.as_string()
		s.sendmail(fromaddr, toaddr, text)
		s.quit()
		
		while not gunEvent.isSet() and len(notConnected):
			for i in notConnected:
				for j in plcList[i]['path']:
					response=os.system("sshpass -p '{1}' scp root@{0}:{2} {4}/{3}").format(i,plcList[i]['pass'],j,(i.split('.')[-1]+j.split('/')[-1]),(base_dir+"/loglar"))
					if not response:
						continue
					os.system("sshpass -p '{1}' ssh root@{0} truncate -s 0 {2}").format(i,plcList[i]['pass'],j)
					notConnected.remove(i)
					msg = MIMEMultipart()
					msg['From'] = fromaddr
					msg['To'] = toaddr
					msg['Subject'] = strftime(format,localtime())
					body = strftime(format,localtime())+" log dosyaları."
					msg.attach(MIMEText(body, 'plain'))

					filename = i.split('.')[-1]+j.split('/')[-1]
					attachment = open(base_dir+'/loglar/'+j.split('/')[-1], "rb")
					p = MIMEBase('application', 'octet-stream')
					p.set_payload((attachment).read())
					encoders.encode_base64(p)
					p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
					msg.attach(p)
					
					s = smtplib.SMTP('smtp.gmail.com', 587)
					s.starttls()
					s.login(fromaddr, "123456789nisra")
					text = msg.as_string()
					s.sendmail(fromaddr, toaddr, text)
					s.quit()
		if not gunEvent.isSet():
			gunEvent.wait(86400)
	except:
		pass





	