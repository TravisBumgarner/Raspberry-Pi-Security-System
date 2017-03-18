import os
import datetime

def get_images(start, end):
    photos_root_dir =  os.path.join(os.path.expanduser('~'), 'webapps', 'chs_photo_storage')
    #photos_root_dir = os.path.abspath("./security_photos")

    if end is None:
        end_datetime = datetime.datetime.now()
    else:
        end_datetime = datetime.datetime(end.year, end.month, end.day)

    if start is None:
        delta = datetime.timedelta(days = 3650)
        start_datetime = end_datetime - delta
    else:
        start_datetime = datetime.datetime(start.year, start.month, start.day)

    image_request = {}
    for dirName, subdir, fileList in os.walk(photos_root_dir):
        for fname in fileList:
            image_file_date = datetime.datetime.strptime(fname[:-4], "%Y-%m-%d-%H-%M-%S")
            if (image_file_date > start_datetime) and (image_file_date < end_datetime):
                _, hour = os.path.split(dirName)
                _, date = os.path.split(_)
                rel_path = fname          
                
                if date not in image_request:
                    image_request[date] = {hour: [rel_path]}
                elif date in image_request and hour not in image_request[date]:
                    image_request[date][hour] = [rel_path]
                else:
                    image_request[date][hour].append(rel_path)
    """
    for date in sorted(image_request.keys(), reverse=reverse_order):
        for hour in sorted(image_request[date], reverse=reverse_order):
            for image in sorted(image_request[date][hour], reverse=reverse_order):
                print("{} -- {} -- {}".format(date, hour, image))
    """
    return image_request

