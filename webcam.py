from PIL import ImageChops, Image, ImageFile
from picamera import PiCamera
import datetime
import math
import time


class Webcam():
    def __init__(self, images_directory,test_images_directory, offline_thumbnails_directory):
        self.camera = PiCamera()
        self.image = None
        self.images_directory = images_directory
        self.test_images_directory = test_images_directory
        self.offline_thumbnails_directory = offline_thumbnails_directory

    def image_entropy(self,img):
        """Calculate the entropy of an image"""
        histogram = img.histogram()
        histogram_length = sum(histogram)
        samples_probability = [float(h) / histogram_length for h in histogram]
        return -sum([p * math.log(p, 2) for p in samples_probability if p != 0])

    def take_photo(self, filename):
        self.camera.capture(self.images_directory + "/" + filename)

    def wait(self,seconds):
        for i in range(1, seconds + 1):
            time.sleep(1)

    def detect_motion(self):
        """
        Takes two images, checks if motion is detected between the two.
        :param test_images_directory: location where images will be saved
        :return:
        """
        time.sleep(1)
        self.test_image1 = self.test_images_directory + "/" + "img1.jpg"
        self.test_image2 = self.test_images_directory + "/" + "img2.jpg"
        self.camera.capture(self.test_image1)
        time.sleep(1)
        self.camera.capture(self.test_image2)

        img1 = Image.open(self.test_image1)
        img2 = Image.open(self.test_image2)
        diff = ImageChops.difference(img1, img2)
        print(self.image_entropy(diff))
        return True if (self.image_entropy(diff) > 5) else False

    def generate_thumbnail(self, filename):
        im = Image.open(self.images_directory + "/" + filename)
        size = 300, 300
        im.thumbnail(size)
        im.save(self.offline_thumbnails_directory + "/" + filename)
