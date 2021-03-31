import logging
import os

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

from page_loader.url_parse import get_filename

attribute_mapping = {
    'link': 'href',
    'script': 'src',
    'img': 'src'
}




def download_assets(html, page_url, assets_dir_name, assets_path):
    soup = BeautifulSoup(html, 'html.parser')
    logging.info('write html file: %s', "тест")
    tag_list = soup.find_all(['link', 'script', 'img'])
    for source_tag in tag_list:
        # src_or_href = choose_src_or_href_attribute(source_tag)
        attr_name = attribute_mapping[source_tag.name]
        asset_url = source_tag.get(attr_name)

        if not asset_url:
            continue

        full_asset_url = urljoin(page_url + '/', asset_url)

        if urlparse(full_asset_url).netloc != urlparse(page_url).netloc:
            continue

        file_name = get_filename(full_asset_url)

        # -------------------
        response = requests.get(full_asset_url, stream=True)
        if not os.path.exists(assets_path):
            os.mkdir(assets_path)

        with open(os.path.join(assets_path, file_name), 'wb',) as output_file:
            chunk_size = 128
            for chunk in response.iter_content(chunk_size=chunk_size):
                output_file.write(chunk)
        # -------------------

        source_tag[asset_url] = os.path.join(assets_dir_name, file_name)

    html_with_local_links = soup.prettify(formatter="html5")
    return html_with_local_links


def choose_src_or_href_attribute(tag):
    if tag.get('src'):
        return 'src'
    if tag.get('href'):
        return 'href'
    else:
        return False

