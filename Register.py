import time
import datetime
from Firebase import Firebase
from Attendance import Attendance

class Register:

	CURRENT_TIME = None
	TODAY = None
	FIREBASE = None
	EMPLOYEE_NODE = None

	def __init__(self):
		self.CURRENT_TIME = int(time.time())
		self.TODAY = datetime.datetime.today().strftime('%Y-%m-%d')
		self.FIREBASE = Firebase().connect()
		self.EMPLOYEE_NODE = Firebase().EMPLOYEE_NODE
		pass

	def new(self, rfid):
		# check the duplication of RFID
		if self.FIREBASE.child(self.EMPLOYEE_NODE).get().each() is not None:
			matching_rfid = [o for o in self.FIREBASE.child(self.EMPLOYEE_NODE).get().each() if o.val()['rfid'] == rfid]
			if matching_rfid:
				print 'Duplicate RFID'
				return False

		employee_name = raw_input('Enter employee\'s name: ')
		
		# add employee in the database
		validate_employee_name = self.FIREBASE.child(self.EMPLOYEE_NODE).child(employee_name).get()
		if validate_employee_name.val() is not None:
			print 'Employee name must be unique'
			self.new(rfid)
		employee_data = {"rfid": rfid, "created_at":self.CURRENT_TIME, "updated_at":self.CURRENT_TIME}
		self.FIREBASE.child(self.EMPLOYEE_NODE).child(employee_name).set(employee_data)

		# mark the attendance of that employee
		attendance = Attendance()
		attendance.markAttendance(rfid)
		print 'Registered'
		return True