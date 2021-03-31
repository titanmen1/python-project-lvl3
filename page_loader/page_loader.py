import logging
import os

import requests

from page_loader.download_assets import download_assets
from page_loader.url_parse import get_filename, get_dirname


def download(url, path=''):
    logging.info('requested url: %s', url)
    # url = 'https://ru.hexlet.io/courses'

    data = requests.get(url)
    # path = '/home/artem/projects/python-project-lvl3/download/'

    filename = get_filename(url)
    dirname = get_dirname(url)

    full_path = os.path.join(os.getcwd() + path)
    file_path = os.path.join(full_path, filename)
    logging.info('output path: %s', full_path)
    assets_path = os.path.join(full_path, dirname)

    result = download_assets(data.text, url, dirname, assets_path)

    with open(file_path, 'w') as file:
        file.write(result)
    return file_path
