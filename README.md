Fire Attendance
==============

A small project to interface with the NFC reader Module MFRC522 on the Raspberry Pi. This project is based on the working of https://github.com/mxgxw/MFRC522-python. 

##Purpose
This project will register an employee and will mark the time in and time out of that particular employee even if its not connected to the internet. This project requires you to have a Google Firebase account becuase the data for employee and attendance will store on Firebase database
https://firebase.google.com/docs/database/

This is a Python port of the example code for the NFC module MF522-AN.

##Requirements
1. This project requires you to have SPI-Py installed from the following repository:
https://github.com/lthiery/SPI-Py

2. This project requires you to have Pyrebase installed from the following repository:
https://github.com/thisbejim/Pyrebase

## Pins
You can use [this](http://i.imgur.com/y7Fnvhq.png) image for reference.

| Name | Pin # | Pin name   |
|------|-------|------------|
| SDA  | 24    | GPIO8      |
| SCK  | 23    | GPIO11     |
| MOSI | 19    | GPIO10     |
| MISO | 21    | GPIO9      |
| IRQ  | None  | None       |
| GND  | Any   | Any Ground |
| RST  | 22    | GPIO25     |
| 3.3V | 1     | 3V3        |

##Usage
1. Set your Firebase credentials in config.json

2. Import Firebase Admin SDK from Firebase console

3. In order to run this module on Raspberry PI's startup open up */etc/rc.local* and add the below line before *exit 0*
	sh /path/to/fire-attendance/launcher.sh &

4. In order to pull the offline data in your Firebase you need to set up a cronjob that'll do that for you. Open crontab as root and add the below job
	m h dom mon dow python /path/to/fire-attendance/app.py --offline

5. In order to receive attendance report of the day passed in email set the configuration in ´email.config.json´ and then run the below command to get the email. You can add this script in your crontab to get the report on daily basis.
	python /path/to/fire-attendance/app.py --email

6. python /path/to/fire-attendance/app.py --help
