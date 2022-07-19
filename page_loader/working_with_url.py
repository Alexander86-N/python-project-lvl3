import re
import os
import requests
import logging
from urllib.parse import urlparse
logger = logging.getLogger(__name__)


def extract_data_from_url(url):
    """Makes a request to the URL and returns its content."""
    try:
        response = requests.get(url)
        logger.debug(f'File {url} received.')
    except requests.exceptions.ConnectionError as err:
        logger.error(f'Connection failed: {err}')
        raise ConnectionError('Connection failed')
    except requests.exceptions.MissingSchema:
        logger.error('Invalid URL '': No scheme supplied.')
        raise ConnectionError('Invalid URL '': No scheme supplied.')
    if response.status_code != requests.codes.ok:
        logger.error(f'Invalid request code: {response.status_code}')
        raise Warning(f'Status_code is {response.status_code}')
    return response.content


def changes_the_name(addres, suffix='.html'):
    """Generates the changed address of the resource."""
    path_parse = urlparse(addres)
    path = os.path.splitext(path_parse.netloc + path_parse.path)[0]
    result = re.sub(r'\W', '-', path) + suffix
    logger.debug(f'Convert the path {addres} to a name {result}')
    return result
