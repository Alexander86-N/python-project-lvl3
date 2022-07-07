import os
from page_loader.data_extraction import resource_extraction
from page_loader.data_extraction import saving_data, name_formation
from page_loader.init_logger import logger


def download(url, filepath):
    change_url = name_formation(url)
    filename = os.path.join(filepath, change_url)

    name_dir = name_formation(url, '_file')
    dirname = os.path.join(filepath, name_dir)
    if not os.path.exists(dirname):
        try:
            os.mkdir(dirname)
        except FileExistsError:
            logger.error('Folder already exists.')
            raise FileExistsError('Folder already exists.')

    logger.info(f'requested url: {url}')
    logger.info(f'output path: {os.path.abspath(filepath)}')
    logger.info(f'write html file: {os.path.abspath(filename)}')
    text_html = resource_extraction(url, dirname, name_dir)
    saving_data(text_html, filename)
    return os.path.abspath(filename)
