import argparse as ap

data = {
    "dropbox_key" : "abc",
    "failed_uploads_list" : "/local_images/failed_uploads.txt",
    "local_images_directory": "/local_images",
    "test_images_directory": "/test_images"
}

wc_config = ap.Namespace(**data)
