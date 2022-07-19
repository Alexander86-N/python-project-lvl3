import os
import logging
from page_loader.work_with_html_page import resource_extraction
from page_loader.work_with_file_system import writes_data_file
from page_loader.work_with_file_system import creating_directory
from page_loader.working_with_url import extract_data_from_url
from page_loader.working_with_url import changes_the_name
logger = logging.getLogger(__name__)


def download(url, filepath=os.getcwd()):
    """Downloads the page from the network to the specified directory.
       Returns the full path to the downloaded file."""
    change_url = changes_the_name(url)
    filename = os.path.join(filepath, change_url)
    data = extract_data_from_url(url)
    name_dir = changes_the_name(url, '_files')
    dirname = os.path.join(filepath, name_dir)
    creating_directory(dirname)
    logger.info(f'requested url: {url}')
    logger.info(f'output path: {os.path.abspath(filepath)}')
    logger.info(f'write html file: {os.path.abspath(filename)}')
    text_html = resource_extraction(url, data, dirname, name_dir)
    writes_data_file(text_html, filename)
    return os.path.abspath(filename)
