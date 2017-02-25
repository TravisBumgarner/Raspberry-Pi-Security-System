from picamera import PiCamera
import time
import datetime
from PIL import ImageChops, Image
import math
from subprocess import call
import urllib
from threading import Thread
import dropbox
       
#Settings
filepath = "/home/pi/Desktop/webcam/dropbox/"




#Globals
camera = PiCamera()

def dropbox_upload(file):
    try:
        dropbox_auth_token = open("dropbox_app_info.txt", "r").read()
        client = dropbox.client.DropboxClient(dropbox_auth_token)
        f = open(file, 'rb')
        response = client.put_file('/' + file, f)
        return True
    except:
        return False

dropbox_upload("readme.txt")


def internet_on():
    try:
        urllib.request.urlopen('http://216.58.192.142')
        return True
    except:
        return False

def upload_failed_files():
    while True:
        queue_file_txt = open("queue_file.txt")
        files_to_upload = queue_file_txt.readlines()
        
        queue_file_txt.close()
        if(len(files_to_upload) > 0):
            for index, file_name in enumerate(files_to_upload):
                if(internet_on()): 
                    success = dropbox_upload(file_name[:-1])
                    if(success):
                        print("Failed upload successful: {}".format(file_name[:-1]))
                if(internet_on() and index +1 == len(files_to_upload)):
                    open("queue_file.txt","w").close() #Clear queue_file after all files upload
                elif(internet_on() is False):
                    queue_file_txt = open("queue_file.txt","w")
                    print("\nInternet still down\n")
                    for file in files_to_upload[index:]:
                        queue_file_txt.write(file_name)
                    time.sleep(30) #Sleep for 10 minutes then try again.
                
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
        print("Motion captured, taking photo {} of {}".format(photo_counter,photo_count))
        filename = date_string + '.jpg'
        camera.capture(filepath + filename)
        if(internet_on()):
            dropbox_upload(filename)
            print("Image Uploaded {}".format(filename))
        else:
            print("Internet offline, saving for later.")
            queue_file(filepath + filename)
            #Save filename to list if upload fails.
        time.sleep(1)

def delay_motion_dectection(duration):
    for i in range(1,duration+1):
        print("Sensing motion again in {}".format(duration-i))
        time.sleep(1)

def motion_found():
    time.sleep(1)
    camera.capture("img1.jpg")
    time.sleep(1)
    camera.capture("img2.jpg")

    img1 = Image.open("img1.jpg")
    img2 = Image.open("img2.jpg")
    diff = ImageChops.difference(img1,img2)
    print("image_entropy {}".format(image_entropy(diff)))
    return True if(image_entropy(diff) > 5) else False

def main():        
    while True:
        if(motion_found()):
            take_photos(5)
            delay_motion_dectection(30)    
        else:      
            print("No motion detected")


if __name__ == "__main__":
    Thread(target = main).start()
    Thread(target = upload_failed_files).start()
   
                    


