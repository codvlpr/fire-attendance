import pyrebase
import json
import os
class Firebase:
	"""docstring for Firebase"""
	BASE=os.path.dirname(os.path.realpath(__file__))
	CONFIG_FILE_LOCATION=BASE+'/config.json'
	EMPLOYEE_NODE = 'employees'
	ATTENDANCE_NODE = 'attendance'
	
	def __init__(self):
		pass

	def connect(self):
		# Connecting to Firebase - pyrebase
		config_data = open(Firebase.CONFIG_FILE_LOCATION).read()
		config = json.loads(config_data)
		firebase = pyrebase.initialize_app(config)
		return firebase.database()
	
	