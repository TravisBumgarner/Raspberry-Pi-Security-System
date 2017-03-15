#!/usr/bin/env python3
# The shepang above makes the script executeable
# chmod +x functions_cron_jobs.py
# Add this file to crontab -e
import os
from PIL import Image, ImageFile
import time

def generate_thumbnails():
    # images_path = os.path.abspath('./app/security_photos')
    images_path = os.path.join(os.path.expanduser('~'), 'webapps', 'chs_photo_storage')
    # thumbnails_path = os.path.abspath('./app/security_photos/thumbs')
    thumbnails_path = os.path.join(os.path.expanduser('~'), 'webapps', 'chs_photo_storage','thumbs')

    images_set = set([f for f in os.listdir(images_path) if os.path.isfile(os.path.join(images_path, f))])
    thumbnails_set = set(os.listdir(thumbnails_path))
    new_images = images_set - thumbnails_set

    for image in new_images:
        im = Image.open(os.path.join(images_path, image))
        size = 200, 200
        im.thumbnail(size)
        im.save(os.path.join(thumbnails_path, image))


if __name__ == "__main__":
    #Since cron jobs only run in units of minutes or greater, we'll call this function 6 times, once per 10 seconds. 6*10 = 1 minute.
    # */1 * * * * ~/webapps/chs_web_viewer/web_viewer/app/functions_cron_jobs.py
    for i in range(0,61):
        generate_thumbnails()
        time.sleep(1)
