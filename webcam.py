#from picamera import PiCamera
import time
import datetime
from PIL import ImageChops, Image
import math
from subprocess import call
import socket
from threading import Thread
import dropbox
from config import wc_config #Contains all settings



#Used to work with images directory
import os


# Settings
filepath = "/home/pi/Desktop/webcam/dropbox/"

# Globals
# camera = PiCamera()

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
        dropbox_auth_token = open("dropbox_app_info.txt", "r").read()
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


def upload_failed_files(file_name_txt):
    """
    Takes files that failed to upload due to internet being down
    and tries to upload them.
    """
    while True:
        queue_file_txt = open("queue_file.txt")
        files_to_upload = queue_file_txt.readlines()
        
        queue_file_txt.close()
        if len(files_to_upload) > 0:
            for index, file_name in enumerate(files_to_upload):
                if is_connected():
                    success = dropbox_upload(file_name[:-1])
                    if success:
                        print_log("Failed upload successful: {}".format(file_name[:-1]))
                if is_connected() and index +1 == len(files_to_upload):
                    open("queue_file.txt","w").close() # Clear queue_file after all files upload
                elif is_connected() is False:
                    queue_file_txt = open("queue_file.txt","w")
                    print_log("\nInternet still down\n")
                    for file in files_to_upload[index:]:
                        queue_file_txt.write(file_name)
                    time.sleep(30) # Sleep for 10 minutes then try again.


def image_entropy(img):
    """Calculate the entropy of an image"""
    histogram = img.histogram()
    histogram_length = sum(histogram)
    samples_probability = [float(h) / histogram_length for h in histogram]
    return -sum([p * math.log(p,2) for p in samples_probability if p != 0])


def queue_file(file_name):
    queue_file_txt = open("queue_file.txt","a")
    queue_file_txt.write(file_name + "\n")
    queue_file_txt.close()


def take_photos(photo_count):
    for photo_counter in range(1,photo_count + 1):
        date_string = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        print_log("Motion captured, taking photo {} of {}".format(photo_counter,photo_count))
        filename = date_string + '.jpg'
        camera.capture(filepath + filename)
        if is_connected():
            dropbox_upload(filename)
            print_log("Image Uploaded {}".format(filename))
        else:
            print_log("Internet offline, saving for later.")
            queue_file(filepath + filename)
            # Save filename to list if upload fails.
        time.sleep(1)


def delay_motion_detection(duration):
    for i in range(1,duration+1):
        print_log("Sensing motion again in {}".format(duration-i))
        time.sleep(1)


def motion_found(test_images_directory):
    """
    Takes two images, checks if motion is detected between the two.
    :param test_images_directory: location where images will be saved
    :return:
    """
    time.sleep(1)
    camera.capture("img1.jpg")
    time.sleep(1)
    camera.capture("img2.jpg")

    img1 = Image.open("img1.jpg")
    img2 = Image.open("img2.jpg")
    diff = ImageChops.difference(img1, img2)
    print_log("image_entropy {}".format(image_entropy(diff)))
    return True if(image_entropy(diff) > 5) else False


def webcam():
    while True:
        if motion_found():
            take_photos(5)
            delay_motion_detection(30)
        else:      
            print_log("No motion detected")


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

"""
if __name__ == "__main__":
    Thread(target = webcam).start()
    Thread(target = upload_failed_files).start()
    Thread(target = purge_old_files).start()
"""

   
                    


