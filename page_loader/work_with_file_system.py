import os
import logging
logger = logging.getLogger(__name__)


def writes_data_file(data, file_name):
    """Performs secure data writing to a file."""
    mode = 'w' if isinstance(data, str) else 'wb'
    try:
        with open(file_name, mode) as fp:
            fp.write(data)
    except FileNotFoundError as err:
        logger.error(f'File {file_name} not saved: {err}')
        raise FileNotFoundError('File not saved')
    logger.debug(f'File {file_name} saved.')


def creating_directory(name):
    """Creates a directory if it does not exist."""
    try:
        os.mkdir(name)
        logger.debug(f'A directory has been created: {name}')
    except FileExistsError:
        logger.error('Folder already exists.')
        raise FileExistsError('Folder already exists.')
