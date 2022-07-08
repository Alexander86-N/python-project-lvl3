import os
from page_loader.data_extraction import resource_extraction, changes_the_name
from page_loader.data_extraction import writes_data_file, extract_data_from_url
from page_loader.init_logger import logger


def download(url, filepath):
    """Downloads the page from the network to the specified directory.
       Returns the full path to the downloaded file."""
    change_url = changes_the_name(url)
    filename = os.path.join(filepath, change_url)
    data = extract_data_from_url(url)
    name_dir = changes_the_name(url, '_file')
    dirname = os.path.join(filepath, name_dir)
    try:
        os.mkdir(dirname)
    except FileExistsError:
        logger.error('Folder already exists.')
        raise FileExistsError('Folder already exists.')

    logger.info(f'requested url: {url}')
    logger.info(f'output path: {os.path.abspath(filepath)}')
    logger.info(f'write html file: {os.path.abspath(filename)}')
    text_html = resource_extraction(url, data, dirname, name_dir)
    writes_data_file(text_html, filename)
    return os.path.abspath(filename)
