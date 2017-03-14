import os
import datetime
from PIL import Image
import time

def get_images(start, end, sort_order):
    # Sort order is either "old_to_new" or "new_to_old"
    # By default the files in the folder are sorted in ascending order

    path =  os.path.join(os.path.expanduser('~'), 'webapps', 'chs_photo_storage')
    #path = os.path.abspath('./app/security_photos')

    if end is None:
        end_datetime = datetime.datetime.now()
    else:
        end_datetime = datetime.datetime(end.year, end.month, end.day)

    if start is None:
        delta = datetime.timedelta(days = 3650)
        # If no start date is defined, get last 3650 days (10 years)
        start_datetime = end_datetime - delta
    else:
        start_datetime = datetime.datetime(start.year, start.month, start.day)

    image_list = []

    for image_file in os.listdir(path):
        image_file_date = datetime.datetime.strptime(image_file[:-4], "%Y-%m-%d-%H-%M-%S")
        if (image_file_date > start_datetime) and (image_file_date < end_datetime):
            image_list.append(image_file)
    if sort_order == 'old_to_new':
        return image_list
    elif sort_order == 'new_to_old':
        return reversed(image_list)


def generate_thumbnails():
    # images_path = os.path.abspath('./app/security_photos')
    images_path = os.path.join(os.path.expanduser('~'), 'webapps', 'chs_photo_storage')
    # thumbnails_path = os.path.abspath('./app/security_photos/thumbs')
    thumbnails_path = os.path.join(os.path.expanduser('~'), 'webapps', 'chs_photo_storage','thumbs')
    while True:
        images_set = set([f for f in os.listdir(images_path) if os.path.isfile(os.path.join(images_path, f))])
        thumbnails_set = set(os.listdir(thumbnails_path))
        new_images = images_set - thumbnails_set

        for image in new_images:
            im = Image.open(os.path.join(images_path, image))
            size = 200, 200
            im.thumbnail(size)
            im.save(os.path.join(thumbnails_path, image))
        time.sleep(10)