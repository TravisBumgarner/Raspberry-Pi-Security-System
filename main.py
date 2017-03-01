import time
import datetime

from subprocess import call
import socket
from threading import Thread
import dropbox
import os

# Classes used for security camera
from file_manager import File_Manager
from webcam import Webcam

#Config data
from config import config

def print_log(text_to_log):
    """
    Print text to log.txt file and command line
    """
    print(text_to_log)
    f = open("log.txt", "a")
    f.write(text_to_log + "\n")
    f.close()


def dropbox_upload(file):
    """
    Try to upload file to dropbox, return true if successful, otherwise false
    """
    try:
        dropbox_auth_token = config["dropbox_key"]
        client = dropbox.client.DropboxClient(dropbox_auth_token)
        f = open(config["offline_images_directory"] + "/" + file, 'rb')
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
                print_log("{} -- File upload success: {}".format(datetime.datetime.now(),file_manager.get_next()))
                file_manager.dequeue()
                


def capture_photos():
    while True:
        if webcam.detect_motion() is True:
            delay_time = 30
            webcam.take_photos(5)
            print_log("{} -- Motion detected".format(datetime.datetime.now()))
            webcam.wait(delay_time)
        else:      
            print_log("{} -- No motion detected".format(datetime.datetime.now()))


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
            print_log("{} -- Deleting {}".format(datetime.datetime.now(),image_file))
            os.remove(images_folder + "/" + image_file)
    time.sleep(60*60*24)


if __name__ == "__main__":
    offline_dir = config["offline_images_directory"]
    online_dir = config["online_images_directory"]
    test_dir = config["test_images_directory"]
    purge_age = config["purge_age"]
        
    file_manager = File_Manager(offline_dir, online_dir)
    webcam = Webcam(offline_dir,test_dir)
    Thread(target = capture_photos).start()
    Thread(target = upload_files).start()
    Thread(target = purge_old_files, args = (offline_dir,purge_age)).start()


   
                    


