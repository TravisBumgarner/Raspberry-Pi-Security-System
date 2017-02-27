class Webcam():
    def __init__(self, images_directory,test_images_directory):
        self.camera = PiCamera()
        self.image = None
        self.images_directory = images_directory
        self.test_images_directory = test_images_directory

    def image_entropy(img):
        """Calculate the entropy of an image"""
        histogram = img.histogram()
        histogram_length = sum(histogram)
        samples_probability = [float(h) / histogram_length for h in histogram]
        return -sum([p * math.log(p, 2) for p in samples_probability if p != 0])

    def take_photo(self):
        date_string = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        filename = date_string + '.jpg'
        self.camera.capture(self.images_directory + "/" + filename)

    def wait(self,seconds):
        for i in range(1, seconds + 1):
            print_log("Sensing motion again in {}".format(duration - i))
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
        camera.capture(self.test_image1)
        time.sleep(1)
        camera.capture(self.test_image2)

        img1 = Image.open(self.test_image1)
        img2 = Image.open(self.test_image2)
        diff = ImageChops.difference(img1, img2)
        print_log("image_entropy {}".format(image_entropy(diff)))
        return True if (image_entropy(diff) > 5) else False
