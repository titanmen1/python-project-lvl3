import os
import re
from urllib.parse import urlparse


def get_filename(url):
    filename, ext = url_to_slug_and_ext(url)
    return str(filename + ext)


def get_dirname(url):
    filename, _ = url_to_slug_and_ext(url)
    return str(filename + '_files')


def url_to_slug_and_ext(url):
    result_url_parse = urlparse(url)
    path, ext = os.path.splitext(result_url_parse.path)
    return replace_chars(result_url_parse.netloc + path), ext if ext else '.html'


def replace_chars(s):
    return re.sub(re.compile(r'[^0-9a-zA-Z]+'), '-', s)
