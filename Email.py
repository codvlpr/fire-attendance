import json
import smtplib
import datetime
import os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from Firebase import Firebase

class Email():

	ATTENDANCE_NODE = None
	FIREBASE = None
	DATE = None
	CONFIG = None
	BASE=os.path.dirname(os.path.realpath(__file__))
	CONFIG_FILE_LOCATION=BASE+'/email.config.json'

	def __init__(self):
		self.ATTENDANCE_NODE = Firebase().ATTENDANCE_NODE
		self.FIREBASE = Firebase().connect()
		self.DATE = datetime.datetime.now() - datetime.timedelta(days = 1)
		config_data = open(Email.CONFIG_FILE_LOCATION).read()
		self.CONFIG = json.loads(config_data)
		pass

	def __prepareMsg(self):
		attendance = self.FIREBASE.child(self.ATTENDANCE_NODE).child(self.DATE.strftime("%Y-%m-%d")).get().each()
		if attendance is not None:
			msg = "Check the below details\n\n"
			for data in attendance:
				msg += "Employee Name: " + data.key() + "\n" + "Time In: " + data.val()['time_in'] + "\n" + "Time Out: " + data.val()['time_out'] + "\n\n"
			attendance = msg
			pass
		return attendance
		pass

	def send(self):
		body = self.__prepareMsg()
		if body is None:
			return False
		else:
			msg = MIMEMultipart()
			msg['From'] = self.CONFIG['email']
			msg['To'] = ', '.join(self.CONFIG['recipient'])
			msg['Subject'] = "Attendance - " + self.DATE.strftime("%A, %Y-%m-%d")
			
			if self.CONFIG['bcc']:
				msg['Bcc'] = self.CONFIG['bcc']
				pass

			if self.CONFIG['cc']:
				msg['Cc'] = self.CONFIG['cc']
				pass
			
			msg.attach(MIMEText(body, 'plain'))
			 
			server = smtplib.SMTP(self.CONFIG['host'], int(self.CONFIG['port']))
			server.starttls()
			server.login(self.CONFIG['email'], self.CONFIG['password'])
			text = msg.as_string()
			server.sendmail(self.CONFIG['email'], self.CONFIG['recipient'], text)
			server.quit()
			return True
		pass




		
		