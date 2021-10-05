import logging
import os
import requests
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar
from urllib.parse import urlparse, urljoin
import page_loader.url


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

        file_name = page_loader.url.to_file_name(full_asset_url)
        assets.append((full_asset_url, file_name))
        tag[attr_name] = os.path.join(assets_dir_name, file_name)

    return (page.prettify(), assets)


def download_assets(assets_path, assets):
    bar_width = len(assets)

    with IncrementalBar("Downloading:", max=bar_width) as bar:
        bar.suffix = "%(percent).1f%% (eta: %(eta)s)"

        for url, file_name in assets:
            asset_content = requests.get(url, stream=True).content
            with open(os.path.join(assets_path, file_name), 'wb') as file:
                file.write(asset_content)
            bar.next()


#  Альтернативное решение с использованием чанков
#  def download_assets(assets_path, assets):
#      for url, file_name in assets:
#          response = requests.get(url, stream=True)

#          with open(
#              os.path.join(assets_path, file_name), 'wb',
#          ) as output_file:
#              content_length = int(response.headers.get('content-length', '0'))
#              chunk_size = 128
#              quantity_of_chunks = (content_length / chunk_size) + 1
#              with Bar(file_name, max=quantity_of_chunks) as progress_bar:
#                  for chunk in response.iter_content(chunk_size=chunk_size):
#                      output_file.write(chunk)
#                      progress_bar.next()


def download(url, output_path=''):
    logging.info('requested url: %s', url)

    full_output_path = os.path.join(os.getcwd(), output_path)
    html_file_name = page_loader.url.to_file_name(url)
    html_file_path = os.path.join(full_output_path, html_file_name)
    assets_dir_name = page_loader.url.to_dir_name(url)
    assets_path = os.path.join(full_output_path, assets_dir_name)

    logging.info('output path: %s', full_output_path)

    response = requests.get(url)
    # print(response.text)
    response.raise_for_status()

    html, assets = prepare_assets(response.text, url, assets_dir_name)
    print(html)

    with open(html_file_path, 'w') as html_file:
        logging.info('write html file: %s', html_file_path)
        html_file.write(html)

    if assets:
        if not os.path.exists(assets_path):
            logging.info('create directory for assets: %s', assets_path)
            os.mkdir(assets_path)

        download_assets(assets_path, assets)

    return html_file_path
