import time
import datetime

from subprocess import call

from threading import Thread
import dropbox
import os

# Classes used for security camera
from file_manager import File_Manager
from webcam import Webcam
from uploader import Uploader

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


def upload_files():
    """
    Tries to upload each file in queue
    """
    while True:
        if uploader.is_connected_to_ssh() is False:
            uploader.connect_to_ssh()
            print("uploader is connected: {}".format(uploader.is_connected_to_ssh()))

        if file_manager.size > 0 and uploader.is_connected_to_internet():
            file_origin = config["offline_images_directory"] + "/" + file_manager.get_next()
            file_destination = file_manager.get_next()

            success = uploader.upload_to_ssh(file_origin, file_destination)
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
    uploader = Uploader(config["ssh_host"],
                        config["ssh_username"],
                        config["ssh_password"])
    
    Thread(target = capture_photos).start()
    Thread(target = upload_files).start()
    Thread(target = purge_old_files, args = (offline_dir,purge_age)).start()


   
                    


