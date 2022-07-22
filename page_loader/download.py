import os
import logging
import requests
from progress.bar import ShadyBar
from page_loader.html import resource_extraction
from page_loader.storage import save, mkdir
from page_loader.url import changes_the_name
logger = logging.getLogger(__name__)


def download(url, filepath=os.getcwd()):
    """Downloads the page from the network to the specified directory.
       Returns the full path to the downloaded file."""
    change_url = changes_the_name(url)
    filename = os.path.join(filepath, change_url)
    data = extract_data_from_url(url)
    name_dir = changes_the_name(url, '_files')
    dirname = os.path.join(filepath, name_dir)
    mkdir(dirname)
    logger.info(f'requested url: {url}')
    logger.info(f'output path: {os.path.abspath(filepath)}')
    logger.info(f'write html file: {os.path.abspath(filename)}')
    resources, text_html = resource_extraction(url, data, dirname, name_dir)
    save(text_html, filename)
    download_content(resources)
    return os.path.abspath(filename)


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


def download_content(resources):
    progres = ShadyBar('Downloading: ', max=len(resources))
    for resource in resources:
        data = extract_data_from_url(resource['url'])
        save(data, resource['path'])
        progres.next()
    progres.finish()
