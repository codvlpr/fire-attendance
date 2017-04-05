import time
import datetime
import json
import os
import calendar
from Firebase import Firebase

class Attendance:
	"""docstring for Attendance"""
	CURRENT_TIME = None
	TODAY = None
	EMPLOYEE_NODE = None
	ATTENDANCE_NODE = None
	FIREBASE = None
	TIME_SPAN = 3
	BASE=os.path.dirname(os.path.realpath(__file__))
	OFFLINE_DATA=BASE+'/offline/data.json'

	def __init__(self):
		self.TODAY = datetime.datetime.today().strftime('%Y-%m-%d')
		# self.CURRENT_TIME = self.__convertTime(datetime.datetime.today().strftime('%H:%M:%S %p'), self.TODAY)
		self.CURRENT_TIME = int(time.time())
		self.FIREBASE = Firebase().connect()
		self.EMPLOYEE_NODE = Firebase().EMPLOYEE_NODE
		self.ATTENDANCE_NODE = Firebase().ATTENDANCE_NODE

	def __dumpJson(self, data):
		with open(self.OFFLINE_DATA, 'w') as DATA_FILE:
			json.dump(data, DATA_FILE)
	
	def __processAttendance(self, employee_name):	
		# get today's data of the employee
		record = self.FIREBASE.child(self.ATTENDANCE_NODE).child(self.TODAY).child(employee_name).get()
		
		if record.val() is None: # Mark time in
			attendance_data={"time_in": self.__convertTime(self.CURRENT_TIME), "time_out": ""}
			self.FIREBASE.child(self.ATTENDANCE_NODE).child(self.TODAY).child(employee_name).set(attendance_data)
			return True
		elif not record.val()['time_out']: # Mark time out
			time_in = self.__convertTime(record.val()['time_in'], self.TODAY)
			time_span = (time_in + (self.TIME_SPAN * 60))
			if self.CURRENT_TIME > time_span: # current time is greater than 3 minutes
				attendance_data={"time_in": self.__convertTime(time_in), "time_out": self.__convertTime(self.CURRENT_TIME)}
				self.FIREBASE.child(self.ATTENDANCE_NODE).child(self.TODAY).child(employee_name).update(attendance_data)
				return True
		return False
		pass

	def __convertTime(self,thisTime,thisDate=None):
		try:
			return datetime.datetime.fromtimestamp(
		        int(thisTime)
		    ).strftime('%H:%M:%S %p')
		except Exception as e:
			# return calendar.timegm(datetime.datetime.strptime(thisDate + ' ' + thisTime, '%Y-%m-%d %H:%M:%S %p').timetuple())
			return time.mktime(datetime.datetime.strptime(thisDate + ' ' + thisTime, "%Y-%m-%d %H:%M:%S %p").timetuple())

	def __saveAttendance(self, rfid):
		try:
			data = json.loads(open(self.OFFLINE_DATA).read())
			node = self.TODAY + "." + rfid
			if node not in data: # Mark time in
				DATA={node: {"time_in": self.CURRENT_TIME, "time_out": ""}}
				data.update(DATA)
				self.__dumpJson(data)
				return True
			elif not data[node]['time_out']: # mark time out
				time_in = data[node]['time_in']
				time_span = (time_in + (self.TIME_SPAN * 60))
				if self.CURRENT_TIME > time_span: # current time is greater than 3 minutes
					DATA={"time_out": self.CURRENT_TIME}
					data[node].update(DATA)
					self.__dumpJson(data)
					return True
				return False
		except Exception as e:
			# fresh data
			node = self.TODAY + "." + rfid
			DATA={node: {"time_in": self.CURRENT_TIME, "time_out": ""}}
			self.__dumpJson(DATA)
			return True
			
		

	def markAttendance(self, rfid):
		try:
			employees = self.FIREBASE.child(self.EMPLOYEE_NODE).get().each()
			if employees is not None: # check if initial employees node exists in the database
				matching_rfid = [o for o in employees if o.val()['rfid'] == rfid]
				if matching_rfid:
				    employee_name = matching_rfid[0].key()
				    return self.__processAttendance(employee_name)
			pass
		except Exception as e:
			# dump the record in offline/data.json
			return self.__saveAttendance(rfid)


	def markOfflineAttendance(self):
		try:
			if os.path.exists(self.OFFLINE_DATA):
				employees = self.FIREBASE.child(self.EMPLOYEE_NODE).get().each()
				if employees is not None: # check if initial employees node exists in the database
					json_data = json.loads(open(self.OFFLINE_DATA).read())
					for data in json_data:
						offline_employee_node = data.split(".")
						rfid = offline_employee_node[1]
						today = offline_employee_node[0]
						matching_rfid = [o for o in employees if o.val()['rfid'] == rfid]
						if matching_rfid:
							employee_name = matching_rfid[0].key()
							record = self.FIREBASE.child(self.ATTENDANCE_NODE).child(today).child(employee_name).get()
							if record.val() is None: # no record on firebase
								if json_data[data]['time_out']:
									attendance_data={"time_in": self.__convertTime(json_data[data]['time_in']), "time_out": self.__convertTime(json_data[data]['time_out'])}
								else:
									attendance_data={"time_in": self.__convertTime(json_data[data]['time_in']), "time_out": ""}
								self.FIREBASE.child(self.ATTENDANCE_NODE).child(today).child(employee_name).set(attendance_data)
							elif not record.val()['time_out']: # no time out on firebase
								if json_data[data]['time_out']:
									attendance_data={"time_in": record.val()['time_in'], "time_out": self.__convertTime(json_data[data]['time_out'])}
								else:
									attendance_data={"time_in": record.val()['time_in'], "time_out": self.__convertTime(json_data[data]['time_in'])}
								self.FIREBASE.child(self.ATTENDANCE_NODE).child(today).child(employee_name).update(attendance_data)
				os.unlink(self.OFFLINE_DATA)
		except Exception as e:
			return False
		pass
		

































