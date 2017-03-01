Setup

Python Requirements
    1. Python > 3.4
    2. dropbox - File Uploader package
    3. pillow - Image Processor package

Hardware Requirements
    1. Raspberry Pi camera

Raspberry Pi Setup
    1. Place webcam_launcher.sh in /usr/local/bin
    Optional - Disable vncserver line if vnc is not 

Dropbox Setup
    1. Create new app https://www.dropbox.com/developers/apps
    2. Scroll down and click "generate key"
    3. Open config.py and paste key in on line for "dropbox_key"
    4. Save and close.

Issues
    1. If main.py is run from webcam_launcher.sh, it is not possible to run it a second time and
       an error will result. (Failed to enable connection: Out of resources)


