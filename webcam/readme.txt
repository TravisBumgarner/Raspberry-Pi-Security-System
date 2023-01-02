Setup

Python Requirements
    1. Python > 3.4
    2. For Image Uploading, either:
	2.1. paramiko (for SSH)
    	2.2. dropbox
    3. pillow - Image Processor package

Hardware Requirements
    1. Raspberry Pi (Written for Raspberry Pi 3B)
    1. Raspberry Pi camera

Raspberry Pi Setup
    1. Add webcam_launcher.sh to crontab so that the script runs on reboot.
    	(Optional - Disable vncserver line if vnc is not used) 
    2. Review settings in config.py (See Dropbox setup and Paramiko setup below)
    3. Run "sudo raspi-config" -> Interfacing Options -> Camera -> Enable.
    4. Restart

Dropbox Setup
    1. Create new app https://www.dropbox.com/developers/apps
    2. Scroll down and click "generate key"
    3. Open config.py and paste key on line for "dropbox_key"
    4. Save and close.

Paramiko Setup (for SSH)
    1. Paste server host, username, in password in config.py

Issues
    1. If main.py is run from webcam_launcher.sh, it is not possible to run it a second time and
       an error will result. (Failed to enable connection: Out of resources)


