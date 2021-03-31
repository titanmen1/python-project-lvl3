import os

import requests

from page_loader.url_parse import get_filename, get_dirname


def download(url, path=''):

    # url = 'https://ru.hexlet.io/courses'
    data = requests.get(url)
    # path = '/home/artem/projects/python-project-lvl3/download/'

    filename = get_filename(url)
    dirname = get_dirname(url)

    full_path = os.path.join(os.getcwd() + path)
    file_path = os.path.join(full_path, filename)

    with open(file_path, 'w') as file:
        file.write(data.text)
    return file_path
