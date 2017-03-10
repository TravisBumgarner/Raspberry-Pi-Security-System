import os
import datetime


def get_images(start, end, sort_order):
    # Sort order is either "old_to_new" or "new_to_old"
    # By default the files in the folder are sorted in ascending order
    path = os.path.abspath("./app/security_photos")

    if end is None:
        end_datetime = datetime.datetime.now()
    else:
        end_datetime = datetime.datetime(end.year, end.month, end.day)

    if start is None:
        delta = datetime.timedelta(days = 3650)
        #If no start date is defined, get last 3650 days (10 years)
        start_datetime = end_datetime - delta
    else:
        start_datetime = datetime.datetime(start.year, start.month, start.day)

    image_list = []

    for image_file in os.listdir(path):
        image_file_date = datetime.datetime.strptime(image_file[:-4], "%Y-%m-%d-%H-%M-%S")
        if (image_file_date > start_datetime) and (image_file_date < end_datetime):
            image_list.append(image_file)
    if sort_order == "old_to_new":
        return image_list
    elif sort_order == "new_to_old":
        return reversed(image_list)