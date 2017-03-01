import argparse as ap

config = {
    "dropbox_key" : "wvZ8VBwBLH0AAAAAAAAMM4tjx4Ql2yn8OR2_p-w2Ya9Plbh7UXYkMYqa_Ym2G3N8",
    "failed_uploads_list" : "./online_images/failed_uploads.txt",
    "online_images_directory": "./online_images",
    "offline_images_directory": "./offline_images",
    "test_images_directory": "./test_images",
    "purge_age": 30, # How many days old should photos be before they are removed from the Rasberry Pi
    "delay_time": 30, # How long in seconds to delay after motion is detected until sensing begins again. 
    "qty_of_photos": 5, # How many photos to take if motion is detected.
    "interval": 1 # Time between each photo in seconds
}
wc_config = ap.Namespace(**config)
