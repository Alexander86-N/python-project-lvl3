import os
import re
import requests
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse
logger = logging.getLogger('page_loader.data_extraction')


TAGS = [{'tag': 'img', 'type': 'src'},
        {'tag': 'link', 'type': 'href'},
        {'tag': 'script', 'type': 'src'}]


def resource_extraction(first_url, directory, name_dir):
    data = extraction_data(first_url)
    logger.debug('Starting resource extraction.')
    soup = BeautifulSoup(data, 'html.parser')
    for tag in TAGS:
        for element in soup.find_all(tag['tag']):
            addres = element.attrs.get(tag['type'])
            if not addres:
                continue
            resours = urlparse(addres)
            url_pars = urlparse(first_url)
            if resours.netloc and resours.netloc != url_pars.netloc:
                logger.debug('Link to another domain.')
                continue
            else:
                logger.debug(f'Suitable link: {addres}')
                suffix = os.path.splitext(addres)[1]
                name = name_formation(f'{url_pars.netloc}{addres}', suffix)
                logger.debug(f'Resource name: {name}')
                element.attrs[tag['type']] = f'{name_dir}/{name}'
                url = f'{url_pars.scheme}://{url_pars.netloc}{resours.path}'
                data_url = extraction_data(url)
                path = f'{directory}/{name}'
                saving_data(data_url, path)
    logger.debug('Resource extraction completed.')
    return soup.prettify()


def extraction_data(url):
    try:
        response = requests.get(url)
        logger.debug(f'File {url} received.')
    except requests.RequestException as err:
        logger.error(f'Connection failed: {err}')
        raise ConnectionError('Connection failed')
    if response.headers['Content-Type'] == 'text/html':
        response.encoding = 'utf-8'
        return response.text
    else:
        return response.content


def saving_data(data, file_name):
    try:
        if isinstance(data, str):
            with open(file_name, 'w') as fp:
                fp.write(data)
        else:
            with open(file_name, 'wb') as fp:
                fp.write(data)
    except FileNotFoundError as err:
        logger.error(f'File {file_name} not saved: {err}')
        raise FileNotFoundError('File not saved')
    logger.debug(f'File {file_name} saved.')


def name_formation(addres, suffix='.html'):
    path_parse = urlparse(addres)
    path = os.path.splitext(path_parse.netloc + path_parse.path)[0]
#    result = ''.join([sing if sing.isalnum() else sing.replace(sing, '-')
#                      for sing in path]) + suffix
    result = re.sub(r'\W', '-', path) + suffix
    logger.debug(f'Convert the path {addres} to a name {result}')
    return result
