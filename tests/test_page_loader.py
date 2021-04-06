import tempfile
from urllib.parse import urljoin

import pytest
import os

from page_loader.url_parse import get_filename, get_dirname, \
    url_to_slug_and_ext, replace_chars

from page_loader import download


URL = 'http://site.com/blog/about.html'
BASE_URL = 'http://site.com/'
file_and_dir_name = 'site-com-blog-about'

ASSETS = [
    {
        'url_path': '/blog/about/assets/styles.css',
        'file_name': 'site-com-blog-about-assets-styles.css',
    },
    {
        'url_path': '/photos/me.jpg',
        'file_name': 'site-com-photos-me.jpg',
    },
    {
        'url_path': '/assets/scripts.js',
        'file_name': 'site-com-assets-scripts.js',
    },
    {
        'url_path': '/blog/about',
        'file_name': 'site-com-blog-about.html',
    },
]


def get_path(filename):
    return os.path.join(os.getcwd(), 'tests', 'fixture', filename)


def test_create_name_file():
    assert get_filename(URL) == file_and_dir_name + '.html'


def test_create_name_dir():
    assert get_dirname(URL) == file_and_dir_name + '_files'


def test_url_to_string_and_ext():
    filename_without_ext, ext = url_to_slug_and_ext(URL)
    assert filename_without_ext == file_and_dir_name
    assert ext == '.html'


def test_replace_chars():
    assert replace_chars('site.com/blog/about') == file_and_dir_name


def test_download(requests_mock):
    for asset in ASSETS:
        asset_url = urljoin(BASE_URL, asset['url_path'])
        asset_path = os.path.join(os.getcwd(),
                                  'tests',
                                  'fixture',
                                  'site-com-blog-about_files',
                                  asset['file_name'],
                                  )
        with open(asset_path, 'rb') as file:
            asset_content = file.read()
        requests_mock.get(asset_url, content=asset_content)

    with tempfile.TemporaryDirectory() as temp_dir:
        with open(get_path('init-site-com-blog-about.html'),
                  'r') as test_page:
            test_page_contend = test_page.read()
        requests_mock.get(URL, text=test_page_contend)
        file_path = download(URL, temp_dir)
        test_path = os.path.join(temp_dir, file_and_dir_name + '.html')
        assert file_path == test_path
        with open(file_path, 'r') as download_page:
            with open(get_path('site-com-blog-about.html'),
                      'r') as file_for_test:
                assert download_page.read() == file_for_test.read()

        for asset in ASSETS:
            asset_path = os.path.join(
                temp_dir,
                file_and_dir_name + '_files',
                asset['file_name'],
            )
            with open(asset_path, 'rb') as asset_file:
                asset_content = asset_file.read()
                with open(os.path.join(os.getcwd(),
                                       'tests',
                                       'fixture',
                                       'site-com-blog-about_files',
                                       asset['file_name']), 'rb') as test_file:
                    test_asset_file = test_file.read()
                    assert asset_content == test_asset_file


@pytest.mark.parametrize('code', [403, 404, 500, 501, 502])
def test_errors_response(requests_mock, code):
    url = 'http://testsite.test/' + str(code)
    requests_mock.get(url, status_code=code)
    with tempfile.TemporaryDirectory() as temp_dir:
        with pytest.raises(Exception):
            assert download(url, temp_dir)


def test_error_dirname():
    with pytest.raises(Exception):
        assert download(URL, '/download')
