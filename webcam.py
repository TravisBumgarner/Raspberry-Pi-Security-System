#from picamera import PiCamera
import time
import datetime

from subprocess import call
import socket
from threading import Thread
import dropbox
import os

from file_manager import File_Manager
from webcam2 import Webcam
# Settings
filepath = "/home/pi/Desktop/webcam/dropbox/"

# Globals
#

def print_log(text_to_log):
    """
    Print text to log.txt file and command line
    """
    print_log(text_to_log)
    f = open("log.txt", "a")
    f.write(text_to_log + "\n")
    f.close()


def dropbox_upload(file):
    """
    Try to upload file to dropbox, return true if successful, otherwise false
    """
    try:
        dropbox_auth_token = open("dropbox_auth.txt", "r").read()
        client = dropbox.client.DropboxClient(dropbox_auth_token)
        f = open(file, 'rb')
        response = client.put_file('/' + file, f)
        return True
    except:
        return False


def is_connected():
    """
    Check if there is an internet connection
    """
    try:
        host = socket.gethostbyname("www.google.com")
        s = socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False


def upload_files():
    """
    Takes files that failed to upload due to internet being down
    and tries to upload them.
    """
    while file_manager.size > 0:
        if is_connected():
            success = dropbox_upload(file_manager.get_next())
            if success:
                file_manager.dequeue()
                print_log("Upload Success: {}".format(file_manager.last_pop))


def capture_photos():
    while True:
        if Webcam.detect_motion() is True:
            delay_time = 30
            Webcam.take_photos(5)
            print_log("Motion detected: {}".format(datetime.datetime.now()))
            Webcam.wait(delay_time)
        else:      
            print_log("No motion detected: {}".format(datetime.datetime.now()))


def purge_old_files(images_folder, purge_age):
    """
    Any file older than (now - purge_age) will be deleted
    :param images_folder: Directory of files to be checked
    :param purge_age: Measured in days
    :return:
    """
    now = datetime.datetime.now()
    delta = datetime.timedelta(days = purge_age)
    cutoff_date = now - delta

    list_of_image_files = [f for f in os.listdir(images_folder) if os.path.isfile(os.path.join(images_folder, f))]
    for image_file in list_of_image_files:
        image_file_date = datetime.datetime.strptime(image_file[:-4], "%Y-%m-%d-%H-%M-%S")
        if cutoff_date > image_file_date:
            print_log("Deleting {}".format(image_file))
            os.remove(images_folder + "/" + image_file)
        else:
            print_log("Not deleting {} because {}".format(image_file, cutoff_date))

    time.sleep(60*60*24)


if __name__ == "__main__":
    file_manager = File_Manager("./offline_images", "./online_images")
    webcam = Webcam("./offline_images","./test_images")
    # Thread(target = capture_photos).start()
    Thread(target = upload_files).start()
    # Thread(target = purge_old_files).start()


   
                    


