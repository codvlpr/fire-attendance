#!/usr/bin/env python
# -*- coding: utf8 -*-
from Read import Read
from Attendance import Attendance
from Email import Email
import sys


if len(sys.argv) > 1:
	PASSED_ARG = sys.argv[1]
	MODE = None

	if PASSED_ARG == "--register":
		MODE = 0
		Read(MODE).start()
	elif PASSED_ARG == "--read":
		MODE = 1
		Read(MODE).start()
	elif PASSED_ARG == "--offline":
		Attendance().markOfflineAttendance()
	elif PASSED_ARG == "--email":
		Email().send()
	elif PASSED_ARG == "--help":
		print open("manual.txt", "r").read() 
	else:
		print "app: invalid option -- " + PASSED_ARG
		print "Try python app.py --help for more information."
else:
	print "Try python app.py --help for more information."

