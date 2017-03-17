import os
import datetime
from PIL import Image, ImageFile
import time
ImageFile.LOAD_TRUNCATED_IMAGES = True

def get_images(photos_root_dir, start, end, sort_order):
    # Sort order is either "old_to_new" or "new_to_old"
    # By default the files in the folder are sorted in ascending order
    #photos_dir =  os.path.join(os.path.expanduser('~'), 'webapps', 'chs_photo_storage')
    root_dir = os.path.abspath(photos_root_dir)
    print("XXXXXXXXXXXXXXXXXXXXXXXXxx: {}".format(root_dir))
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

    all_images_list = []

    # Gets all direct children directories of images folder not including thumbs
    photos_by_date_dirs = [name for name in os.listdir(photos_root_dir) if os.path.isdir(os.path.join(photos_root_dir, name)) and name != "thumbs"]
    print("dates: {}".format(photos_by_date_dirs))
    for current_dir in photos_by_date_dirs:
        for root, _, files in os.walk(os.path.abspath(os.path.join(root_dir, current_dir))):
            for file in files:
                all_images_list.append(os.path.join(root, file))

    image_list_in_range = []
    for image_file in all_images_list:
        image_file_dir, image_file_name = os.path.split(image_file)
        image_file_date = datetime.datetime.strptime(image_file_name[:-4], "%Y-%m-%d-%H-%M-%S")
        if (image_file_date > start_datetime) and (image_file_date < end_datetime):
            image_list_in_range.append(image_file)
    print("images: {}".format(image_list_in_range))
    if sort_order == 'old_to_new':
        return image_list_in_range
    elif sort_order == 'new_to_old':
        return reversed(image_list_in_range)

