import os
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from progress.bar import Bar
from page_loader.url_parse import get_filename


def download_assets(html, page_url, assets_dir_name, assets_path):
    soup = BeautifulSoup(html, 'html.parser')
    tag_list = soup.find_all(['link', 'script', 'img'])
    bar = Bar('Processing', max=len(tag_list))

    for source_tag in tag_list:
        attribute_name = choose_attribute(source_tag.name)
        short_asset_url = source_tag.get(attribute_name)

        if not short_asset_url:
            bar.next()
            continue

        full_asset_url = urljoin(page_url + '/', short_asset_url)

        if urlparse(full_asset_url).netloc == urlparse(page_url).netloc:
            filename = get_filename(full_asset_url)
            # -------------------
            full_asset_path = os.path.join(assets_path, filename)
            download_asset(full_asset_url, full_asset_path)
            # -------------------
            source_tag[attribute_name] = os.path.join(
                assets_dir_name,
                filename
            )
        bar.next()

    bar.finish()
    return soup.prettify(formatter="html5")


def choose_attribute(tag):
    if tag == 'link':
        return 'href'
    if tag == 'script':
        return 'src'
    if tag == 'img':
        return 'src'


def download_asset(url, full_asset_path):
    print(url)
    response = requests.get(url, stream=True)
    save_file(response.content, full_asset_path)


def save_file(data, path):
    with open(path, 'wb') as output_file:
        output_file.write(data)
