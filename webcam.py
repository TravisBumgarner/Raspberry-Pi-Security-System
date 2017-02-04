import picamera
import time
import datetime
from PIL import ImageChops, Image
import math

camera = picamera.PiCamera()

sleep_time = 30 #How many seconds camera should sleep after taking batch of photos of motion
photo_count = 5 #How many photos to take if motion is detected

def image_entropy(img):
    """Calculate the entropy of an image"""
    histogram = img.histogram()
    histogram_length = sum(histogram)
    samples_probability = [float(h) / histogram_length for h in histogram]
    return -sum([p * math.log(p,2) for p in samples_probability if p != 0])

while True:
    print("Capturing img1")
    camera.capture("img1.jpg")
    time.sleep(1)
    print("Capturing img2")
    camera.capture("img2.jpg")
    img1 = Image.open("img1.jpg")
    img2 = Image.open("img2.jpg")
    print("Comparing images")
    diff = ImageChops.difference(img1,img2)
    if(image_entropy(diff) > 5):
        print("image_entropy {}".format(image_entropy(diff)))
        for photo_counter in range(1,photo_count + 1):
            date_string = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            print("Motion captured, taking photo {} of {}".format(photo_counter,photo_count))
            camera.capture("dropbox/" + date_string + '.jpg')
            time.sleep(1)
        for i in range(1,sleep_time+1):
            print("Sensing motion again in {}".format(sleep_time-i))
            time.sleep(1)
    else:      
        print("No motion detected")
