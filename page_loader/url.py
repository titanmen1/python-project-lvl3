import os
import re
from urllib.parse import urlparse


ALPHANUM = re.compile(r'[^0-9a-zA-Z]+')


def to_file_name(url):
    parsed_url = urlparse(url)
    (path, ext) = os.path.splitext(parsed_url.path)
    slug = re.sub(ALPHANUM, '-', parsed_url.netloc + path)
    format = ext if ext else '.html'

    return re.sub(r'^-', '', slug) + format


def to_dir_name(url):
    parsed_url = urlparse(url)
    (path, _) = os.path.splitext(parsed_url.path)
    slug = re.sub(ALPHANUM, '-', parsed_url.netloc + path)

    return slug + '_files'
