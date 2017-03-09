import os
import datetime


def get_images(start, end):
    path = os.path.abspath("./app/static/img/")

    start_datetime = datetime.datetime(start.year, start.month, start.day)
    end_datetime = datetime.datetime(end.year, end.month, end.day)

    image_list = []

    for image_file in os.listdir(path):
        image_file_date = datetime.datetime.strptime(image_file[:-4], "%Y-%m-%d-%H-%M-%S")
        if (image_file_date > start_datetime) and (image_file_date < end_datetime):
            image_list.append(image_file)
    return image_list