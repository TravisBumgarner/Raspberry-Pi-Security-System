import os

def get_images():
    path = os.path.abspath("./app/static/img/")
    return [image for image in os.listdir(path)]
