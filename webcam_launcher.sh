#!/bin/sh
# launcher.sh
# navigate to home, then to this dir, then execute script, then home, launch vncserver

vncserver
cd /
cd home/pi/Desktop/webcam
sudo python main.py
cd /
