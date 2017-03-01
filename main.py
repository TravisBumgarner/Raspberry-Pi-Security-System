import time
import datetime

from subprocess import call
import socket
from threading import Thread
import dropbox
from dropbox import MaxRetryError
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
    except MaxRetryError:
        print("FAILURE!")
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
    Tries to upload each file in queue
    """
    while True:
        print("size: {}".format(file_manager.size))
        print("is_connected: {}".format(is_connected()))
        if file_manager.size > 0 and is_connected():
            success = dropbox_upload(file_manager.get_next())
            print("success: {}".format(success))
            if success:
                print_log("{} -- File upload success: {}".format(datetime.datetime.now(),file_manager.get_next()))
                file_manager.dequeue()
        time.sleep(1)
                


def capture_photos():
    """
    If motion is detected, take photo(s) and then wait until next motion
    detection.
    """
    while True:
        if webcam.detect_motion() is True:
            print_log("{} -- Motion detected".format(datetime.datetime.now()))
            for i in range(0,config["qty_of_photos"]):
                filename = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".jpg"
                webcam.take_photo(filename)
                file_manager.enqueue(filename)
                time.sleep(config["interval"])
            webcam.wait(config["delay_time"])
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


def setup_dirs(*pathes):
    for path in pathes:
        if not os.path.exists(path):
            os.makedirs(path)
    

if __name__ == "__main__":
    
    
    offline_dir = config["offline_images_directory"]
    online_dir = config["online_images_directory"]
    test_dir = config["test_images_directory"]
    purge_age = config["purge_age"]
    setup_dirs(offline_dir,online_dir,test_dir)
        
    file_manager = File_Manager(offline_dir, online_dir)
    webcam = Webcam(offline_dir,test_dir)
    
    Thread(target = capture_photos).start()
    Thread(target = upload_files).start()
    Thread(target = purge_old_files, args = (offline_dir,purge_age)).start()


   
                    


