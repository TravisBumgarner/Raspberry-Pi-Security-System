import argparse as ap

data = {
    "dropbox_key" : "abc",
    "failed_uploads_list" : "/online_images/failed_uploads.txt",
    "local_images_directory": "/online_images",
    "test_images_directory": "/test_images",
    "purge_age": 30 # How many days old should photos be before they are removed from the Rasberry Pi
}

wc_config = ap.Namespace(**data)
