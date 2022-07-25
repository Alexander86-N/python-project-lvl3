import os
import logging
import requests
from progress.bar import ShadyBar
from page_loader.html import get_resources
from page_loader.storage import save, mkdir
from page_loader.url import to_filename, to_directory
logger = logging.getLogger(__name__)


def download(url, filepath=os.getcwd()):
    """Downloads the page from the network to the specified directory.
       Returns the full path to the downloaded file."""
    filename = os.path.join(filepath, to_filename(url))
    data = get_data(url)
    name_dir = to_directory(url)
    dirname = os.path.join(filepath, name_dir)
    mkdir(dirname)
    logger.info(f'requested url: {url}')
    logger.info(f'output path: {os.path.abspath(filepath)}')
    logger.info(f'write html file: {os.path.abspath(filename)}')
    resources, text_html = get_resources(url, data, name_dir)
    save(text_html, filename)
    download_resources(resources, dirname)
    return os.path.abspath(filename)


def get_data(url):
    """Makes a request to the URL and returns its content."""
    try:
        response = requests.get(url)
        logger.debug(f'File {url} received.')
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        logger.error(f'Connection failed: {err}')
        raise ConnectionError('Connection failed')
    return response.content


def download_resources(resources, directory):
    """Loads and writes local resources of a given page."""
    progres = ShadyBar('Downloading: ', max=len(resources))
    for resource in resources:
        try:
            data = get_data(resource['url'])
        except requests.exceptions.RequestException as err:
            logger.error(err)
        path = os.path.join(directory, resource['name'])
        save(data, path)
        progres.next()
    progres.finish()
