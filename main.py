import time
import datetime
from subprocess import call
from threading import Thread
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
        try:
            if uploader.is_connected_to_ssh() is False:
                errorMsg = uploader.connect_to_ssh()
                if errorMsg is not None: print_log("{} -- Script Error: {}".format(datetime.datetime.now(),errorMsg))
                print_log("{} -- Internet Status: {}".format(datetime.datetime.now(),uploader.is_connected_to_ssh()))
                time.sleep(60)
                continue
                
            if file_manager.size > 0 and uploader.is_connected_to_internet():
                full_file_origin = config["offline_images_directory"] + "/" + file_manager.get_next()
                full_file_destination = ""

                thumb_file_origin = config["offline_thumbnails_directory"] + "/" + file_manager.get_next()
                thumb_file_destination = "thumbs/"
                
                if config["ssh_or_dropbox"] == "ssh":
                    success1 = uploader.upload_to_ssh(full_file_origin, full_file_destination)
                    success2 = uploader.upload_to_ssh(thumb_file_origin, thumb_file_destination)
                    success = success1 and success2
                elif config["ssh_or_dropbox"] == "dropbox":
                    success = uploader.upload_to_dropbox(full_file_origin)
                else:
                    raise ValueError('Select either "ssh" or "dropbox" from config.py setting "ssh_or_dropbox"')
                if success:
                    print_log("{} -- File upload success: {}".format(datetime.datetime.now(),file_manager.get_next()))
                    file_manager.dequeue()
            time.sleep(1)
        except Exception as e:
            print_log("{} -- Script Error: {}".format(datetime.datetime.now(),e))


def capture_photos():
    """
    If motion is detected, take photo(s) and then wait until next motion
    detection.
    """
    while True:
        try:
            if webcam.detect_motion() is True:
                print_log("{} -- Motion detected".format(datetime.datetime.now()))
                for i in range(0,config["qty_of_photos"]):
                    filename = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".jpg"
                    webcam.take_photo(filename)
                    webcam.generate_thumbnail(filename)
                    file_manager.enqueue(filename)
                    time.sleep(config["interval"])
                webcam.wait(config["delay_time"])

        except Exception as e:
            print_log("{} -- Script Error: {}".format(datetime.datetime.now(),e))


def setup_dirs(*pathes):
    for path in pathes:
        if type(path) is not str:
            raise TypeError("{} is not a valid folder path, check config.py.".format(path))
        if not os.path.exists(path):
            os.makedirs(path)
    

if __name__ == "__main__":
    offline_dir = config["offline_images_directory"]
    offline_thumbnails_dir = config["offline_thumbnails_directory"]

    test_dir = config["test_images_directory"]
                                          
    purge_age = config["purge_age"]
    setup_dirs(offline_dir,
               test_dir,
               offline_thumbnails_dir
               )
        
    file_manager = File_Manager(offline_dir)
    webcam = Webcam(offline_dir,test_dir, offline_thumbnails_dir)
    uploader = Uploader(config["ssh_host"],
                        config["ssh_username"],
                        config["ssh_password"],
                        config["dropbox_key"])

    Thread(target = capture_photos).start()
    Thread(target = upload_files).start()

    

   
                    


