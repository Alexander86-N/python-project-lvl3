from os import path
import re
import logging
from urllib.parse import urlparse
logger = logging.getLogger(__name__)


def url_parsing(url):
    """Divides the url into a path and a format."""
    path_parse = urlparse(url)
    addres, suffix = path.splitext(path_parse.netloc + path_parse.path)
    return change_text(addres), suffix


def change_text(text):
    """Сharacters other than letters and numbers are replaced with '-'."""
    result = re.sub(r'\W', '-', text)
    logger.debug(f'Convert the path {text} to a name {result}')
    return result


def to_directory(url):
    """Forms the name of the directory."""
    result, suffix = url_parsing(url)
    return f'{result}_files'


def to_filename(url):
    """Forms the name of the file."""
    result, suffix = url_parsing(url)
    if suffix:
        return f'{result}{suffix}'
    return f'{result}.html'
