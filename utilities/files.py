import os
import re
from settings import config


def get_files_by_size(path):
    images_files = []

    fun = lambda x: os.path.isfile(os.path.join(path, x))
    files_list = filter(fun, os.listdir(path))

    """Create a list of files in directory along with the size"""
    size_of_file = [(f, os.stat(os.path.join(path, f)).st_size) for f in files_list]

    for file in size_of_file:
        if re.search(r"\.(gif|jpg|jpeg|png)$", file[0], re.IGNORECASE):
            images_files.append(file[0])

    return images_files


def get_name_girl(image):
    return image[: image.find("_")]


def delete_images_tweeted(images_to_delete):
    for image in images_to_delete:
        image_url = f"${config.ROUTE}/${image}"
        os.remove(image_url)
