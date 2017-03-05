import os

def get_images():
    path = os.path.abspath("./app/static/img/")
    print(path)
    return [path+ "\\" + image for image in os.listdir(path)]
