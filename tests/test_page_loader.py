import os
import pytest
import requests
import tempfile
from urllib.parse import urljoin

from page_loader import download

BASE_URL = 'https://site.com/'
HTML_FILE_NAME = 'site-com-blog-about.html'
ASSETS_DIR_NAME = 'site-com-blog-about_files'
PAGE_PATH = '/blog/about'
PAGE_URL = urljoin(BASE_URL, PAGE_PATH)
ASSETS = [
    {
        'format': 'css',
        'url_path': '/blog/about/assets/styles.css',
        'file_name': 'site-com-blog-about-assets-styles.css',
    },
    {
        'format': 'svg',
        'url_path': '/photos/me.jpg',
        'file_name': 'site-com-photos-me.jpg',
    },
    {
        'format': 'js',
        'url_path': '/assets/scripts.js',
        'file_name': 'site-com-assets-scripts.js',
    },
    {
        'format': 'html',
        'url_path': '/blog/about',
        'file_name': 'site-com-blog-about.html',
    },
]


def get_fixture_path(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'fixtures', file_name)


def read(file_path, mode='r'):
    with open(file_path, mode) as f:
        result = f.read()
    return result


def get_fixture_data(file_name):
    return read(get_fixture_path(file_name))


# проверка ошибок сети
def test_connection_error(requests_mock):
    invalid_url = 'https://badsite.com'
    requests_mock.get(invalid_url, exc=requests.exceptions.ConnectionError)

    with tempfile.TemporaryDirectory() as tmpdirname:
        assert not os.listdir(tmpdirname)

        with pytest.raises(Exception):
            assert download(invalid_url, tmpdirname)

        assert not os.listdir(tmpdirname)


# проверка ошибок с сайта
@pytest.mark.parametrize('code', [404, 500])
def test_response_with_error(requests_mock, code):
    url = urljoin(BASE_URL, str(code))
    requests_mock.get(url, status_code=code)

    with tempfile.TemporaryDirectory() as tmpdirname:
        with pytest.raises(Exception):
            assert download(url, tmpdirname)


# проверка ошибок файловой системы
def test_storage_errors(requests_mock):
    requests_mock.get(PAGE_URL)

    root_dir_path = '/sys'
    with pytest.raises(Exception):
        assert download(PAGE_URL, root_dir_path)

    file_path = get_fixture_path(HTML_FILE_NAME)
    with pytest.raises(Exception):
        assert download(PAGE_URL, file_path)

    not_exists_path = get_fixture_path('notExistsPath')
    with pytest.raises(Exception):
        assert download(PAGE_URL, not_exists_path)


def test_page_load(requests_mock):
    content = get_fixture_data(HTML_FILE_NAME)
    requests_mock.get(PAGE_URL, text=content)
    expected_html_file_path = get_fixture_path(
        os.path.join('expected', HTML_FILE_NAME),
    )
    expected_html_content = read(expected_html_file_path)

    for asset in ASSETS:
        asset_url = urljoin(BASE_URL, asset['url_path'])
        expected_asset_path = get_fixture_path(
            os.path.join('expected', ASSETS_DIR_NAME, asset['file_name']),
        )
        expected_asset_content = read(expected_asset_path, 'rb')
        asset['content'] = expected_asset_content
        requests_mock.get(asset_url, content=expected_asset_content)

    with tempfile.TemporaryDirectory() as tmpdirname:
        assert not os.listdir(tmpdirname)

        output_file_path = download(PAGE_URL, tmpdirname)
        assert len(os.listdir(tmpdirname)) == 2
        assert len(os.listdir(os.path.join(tmpdirname, ASSETS_DIR_NAME))) == 4

        html_file_path = os.path.join(tmpdirname, HTML_FILE_NAME)
        assert output_file_path == html_file_path

        html_content = read(html_file_path)
        assert html_content == expected_html_content

        for asset in ASSETS:
            asset_path = os.path.join(
                tmpdirname,
                ASSETS_DIR_NAME,
                asset['file_name'],
            )
            asset_content = read(asset_path, 'rb')
            expected_asset_content = asset['content']
            assert asset_content == expected_asset_content
