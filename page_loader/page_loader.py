import logging
import os
import requests
from page_loader.download_assets import modification_page, save_file
from page_loader.url_parse import get_filename, get_dirname


def download(url, path=''):
    data = requests.get(url)
    data.raise_for_status()
    logging.info('requested url: {0}'.format(url))

    filename = get_filename(url)
    dirname = get_dirname(url)
    full_path = os.path.join(os.getcwd(), path)
    file_path = os.path.join(full_path, filename)
    assets_path = os.path.join(full_path, dirname)
    logging.info('output path: {0}'.format(full_path))

    if not os.path.exists(assets_path):
        logging.info('create directory for assets: {0}'.format(assets_path))
        os.mkdir(assets_path)

    updated_html = modification_page(data.text, url, dirname, assets_path)
    with open(file_path, 'w') as file:
        file.write(updated_html)
    return file_path
