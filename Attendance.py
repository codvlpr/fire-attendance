import time
import datetime
from Firebase import Firebase

class Attendance:
	"""docstring for Attendance"""
	CURRENT_TIME = None
	TODAY = None
	EMPLOYEE_NODE = None
	ATTENDANCE_NODE = None
	FIREBASE = None
	TIME_SPAN = 3

	def __init__(self):
		self.CURRENT_TIME = int(time.time())
		self.TODAY = datetime.datetime.today().strftime('%Y-%m-%d')
		self.FIREBASE = Firebase().connect()
		self.EMPLOYEE_NODE = Firebase().EMPLOYEE_NODE
		self.ATTENDANCE_NODE = Firebase().ATTENDANCE_NODE
	
	def __processAttendance(self, employee_name):
		# get today's data of the employee
		record = self.FIREBASE.child(self.ATTENDANCE_NODE).child(self.TODAY).child(employee_name).get()
		
		if record.val() is None: # Mark time in
			attendance_data={"time_in": self.CURRENT_TIME, "time_out": ""}
			self.FIREBASE.child(self.ATTENDANCE_NODE).child(self.TODAY).child(employee_name).set(attendance_data)
			return True
		elif not record.val()['time_out']: # Mark time out
			time_in = record.val()['time_in']
			time_span = (time_in + (self.TIME_SPAN * 60))
			if self.CURRENT_TIME > time_span: # current time is greater than 3 minutes
				attendance_data={"time_in": time_in, "time_out": self.CURRENT_TIME}
				self.FIREBASE.child(self.ATTENDANCE_NODE).child(self.TODAY).child(employee_name).update(attendance_data)
				return True
		return False
		pass

	def markAttendance(self, rfid):
		employees = self.FIREBASE.child(self.EMPLOYEE_NODE).get().each()
		if employees is not None: # check if initial employees node exists in the database
			matching_rfid = [o for o in employees if o.val()['rfid'] == rfid]
			if matching_rfid:
			    employee_name = matching_rfid[0].key()
			    print 'Marked'
			    return self.__processAttendance(employee_name)
		pass