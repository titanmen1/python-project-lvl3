import os
import re
from urllib.parse import urlparse


def get_filename(url):
    filename, ext = url_to_string(url)
    return str(filename + ext)


def get_dirname(url):
    filename, _ = url_to_string(url)
    return str(filename + '_files')


def url_to_string(url):
    result = []
    result_url_parse = urlparse(url)
    path, ext = os.path.splitext(result_url_parse.path)
    if result_url_parse.netloc:
        result.append(result_url_parse.netloc)
    if result_url_parse.path:
        result.append(path)

    return replace_chars(''.join(result)), ext if ext else '.html'


def replace_chars(s):
    return re.sub(re.compile(r'[^0-9a-zA-Z]+'), '-', s)
