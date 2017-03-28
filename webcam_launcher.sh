#!/bin/sh
# launcher.sh
# navigate to home, then to this dir, then execute script, then home, launch vncserver

cd /
vncserver
cd home/pi/Desktop/webcam
sudo python3 main.py
cd /
