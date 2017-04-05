#!/bin/sh
sleep 60
sudo python /home/pi/fire-attendance/app.py --read > /dev/null &
