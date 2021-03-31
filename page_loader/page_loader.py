# import logging
# import os
#
# import requests
#
# from page_loader.download_assets import download_assets
# from page_loader.url_parse import get_filename, get_dirname
#
#
# def download(url, path=''):
#     logging.info('requested url: %s', url)
#     # url = 'https://ru.hexlet.io/courses'
#
#     data = requests.get(url)
#     # path = '/home/artem/projects/python-project-lvl3/download/'
#
#     filename = get_filename(url)
#     dirname = get_dirname(url)
#
#     full_path = os.getcwd() + path
#     file_path = os.path.join(full_path, filename)
#     logging.info('output path: %s', full_path)
#     assets_path = os.path.join(full_path, dirname)
#     if not os.path.exists(assets_path):
#         os.mkdir(assets_path)
#     result = download_assets(data.text, url, dirname, assets_path)
#
#     with open(file_path, 'w') as file:
#         file.write(result)
#     return file_path

import logging
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

from page_loader.url_parse import get_filename, get_dirname

attribute_mapping = {
    'link': 'href',
    'script': 'src',
    'img': 'src'
}


def prepare_assets(html, url, assets_dir_name):
    page = BeautifulSoup(html, 'html.parser')

    tags = [*page('script'), *page('link'), *page('img')]

    assets = []
    for tag in tags:
        attr_name = attribute_mapping[tag.name]
        asset_url = tag.get(attr_name)

        if not asset_url:
            continue

        full_asset_url = urljoin(url + '/', asset_url)

        if urlparse(full_asset_url).netloc != urlparse(url).netloc:
            continue

        file_name = get_filename(full_asset_url)
        assets.append((full_asset_url, file_name))
        tag[attr_name] = os.path.join(assets_dir_name, file_name)

    return (page.prettify(formatter='html5'), assets)


def download_assets(assets_path, assets):
    for url, file_name in assets:
        response = requests.get(url, stream=True)

        with open(
            os.path.join(assets_path, file_name), 'wb',
        ) as output_file:
            chunk_size = 128
            for chunk in response.iter_content(chunk_size=chunk_size):
                output_file.write(chunk)


def download(url, output_path=''):
    logging.info('requested url: %s', url)

    full_output_path = os.path.join(os.getcwd(), output_path)
    html_file_name = get_filename(url)
    html_file_path = os.path.join(full_output_path, html_file_name)
    assets_dir_name = get_dirname(url)
    assets_path = os.path.join(full_output_path, assets_dir_name)

    logging.info('output path: %s', full_output_path)

    response = requests.get(url)
    response.raise_for_status()

    html, assets = prepare_assets(response.text, url, assets_dir_name)

    with open(html_file_path, 'w') as html_file:
        logging.info('write html file: %s', html_file_path)
        html_file.write(html)

    if assets:
        if not os.path.exists(assets_path):
            logging.info('create directory for assets: %s', assets_path)
            os.mkdir(assets_path)

        download_assets(assets_path, assets)

    return html_file_path
