import tempfile

import pytest
import os

from page_loader.download_assets import download_assets
from page_loader.url_parse import get_filename, get_dirname, \
    url_to_string, replace_chars

from page_loader import download


URL = 'https://notepadonline.ru/'
URL_ASSET = 'https://notepadonline.ru/banners/strap.gif'
file_and_dir_name = 'notepadonline-ru-'
css_filename = 'notepadonline-ru-css-style.css'


def test_create_name_file():
    assert get_filename(URL) == file_and_dir_name + '.html'


def test_create_name_dir():
    assert get_dirname(URL) == file_and_dir_name + '_files'


def test_url_to_string_and_ext():
    filename_without_ext, ext = url_to_string(URL)
    assert filename_without_ext == file_and_dir_name
    assert ext == '.html'


def test_replace_chars():
    assert replace_chars('notepadonline.ru/') == file_and_dir_name


def test_download_assets():
    with tempfile.TemporaryDirectory() as temp_dir:
        os.mkdir(os.path.join(temp_dir,
                              file_and_dir_name + '_files'))
        file_path = os.path.join(temp_dir,
                                 file_and_dir_name + '_files',
                                 'notepadonline-ru-banners-strap.gif')
        download_assets(URL_ASSET, file_path)
        assert open(file_path, 'rb').read() == open('./tests/fixture/'
                                                    + file_and_dir_name
                                                    + '_files/'
                                                    + 'notepadonline-ru-'
                                                    + 'banners-strap.gif',
                                                    'rb').read()


def test_download():
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = download(URL, temp_dir)
        test_path = os.path.join(temp_dir, file_and_dir_name + '.html')
        assert file_path == test_path
        with open(file_path, 'r') as download_page:
            with open('./tests/fixture/notepadonline-ru-.html',
                      'r') as test_page:
                assert download_page.read() == test_page.read()

        with open(os.path.join(temp_dir,
                               file_and_dir_name + '_files',
                               css_filename), 'r') as download_css_file:
            with open('./tests/fixture/notepadonline-ru-_files/' +
                      css_filename, 'r') as test_css_file:
                assert download_css_file.read() == test_css_file.read()


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
