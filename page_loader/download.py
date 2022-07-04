import os
import logging
from page_loader.data_extraction import resource_extraction
from page_loader.data_extraction import saving_data, name_formation
logger = logging.getLogger('page_loader.download')


def download(url, filepath):
    change_url = name_formation(url)
    filename = os.path.join(filepath, change_url)

    name_dir = name_formation(url, '_file')
    dirname = os.path.join(filepath, name_dir)
    if not os.path.exists(dirname):
        try:
            os.mkdir(dirname)
        except OSError:
            logger.error('The dictory was not created.')
            raise FileNotFoundError('The dictory was not created.')

    logger.info(f'requested url: {url}')
    text_html = resource_extraction(url, dirname, name_dir)
    logger.info(f'output path: {os.path.abspath(filepath)}')
    logger.info(f'write html file: {os.path.abspath(filename)}')
    saving_data(text_html, filename)
    return os.path.abspath(filename)
