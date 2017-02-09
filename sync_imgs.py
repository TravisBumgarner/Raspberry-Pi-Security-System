from subprocess import call
dropbox_script = "/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/Desktop/webcam/dropbox/test.jpg test.jpg"
call([dropbox_script], shell = True)
