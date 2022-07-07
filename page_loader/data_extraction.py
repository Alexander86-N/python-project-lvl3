import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from progress.bar import IncrementalBar
from page_loader.init_logger import logger


TAGS = [{'tag': 'img', 'type': 'src'},
        {'tag': 'link', 'type': 'href'},
        {'tag': 'script', 'type': 'src'}]


def resource_extraction(first_url, directory, name_dir):
    data = extraction_data(first_url)
    url_pars = urlparse(first_url)
    logger.debug('Starting resource extraction.')
    soup = BeautifulSoup(data, 'html.parser')
    links = defines_working_links(soup, first_url)
    logger.debug(links)
    progres = IncrementalBar('Downloading: ', max=len(links))
    for dataset, teg in links.items():
        addres = dataset.attrs[teg]
        value = urlparse(addres)
        logger.debug(f'Suitable link: {addres}')
        suffix = os.path.splitext(addres)[1]
        name = name_formation(f'{url_pars.netloc}{addres}', suffix)
        logger.debug(f'Resource name: {name}')
        dataset.attrs[teg] = f'{name_dir}/{name}'
        url = f'{url_pars.scheme}://{url_pars.netloc}{value.path}'
        data_url = extraction_data(url)
        path = f'{directory}/{name}'
        saving_data(data_url, path)
        progres.next()
    logger.debug('Resource extraction completed.')
    progres.finish()
    return soup.prettify()


def extraction_data(url):
    try:
        response = requests.get(url)
        logger.debug(f'File {url} received.')
    except requests.RequestException as err:
        logger.error(f'Connection failed: {err}')
        raise ConnectionError('Connection failed')
    if response.status_code != requests.codes.ok:
        logger.error(f'Invalid request code: {response.status_code}')
        raise Warning(f'Status_code is {response.status_code}')
    if response.headers['Content-Type'] == 'text/html':
        response.encoding = 'utf-8'
        return response.text
    else:
        return response.content


def saving_data(data, file_name):
    mode = 'w' if isinstance(data, str) else 'wb'
    try:
        with open(file_name, mode) as fp:
            fp.write(data)
    except FileNotFoundError as err:
        logger.error(f'File {file_name} not saved: {err}')
        raise FileNotFoundError('File not saved')
    logger.debug(f'File {file_name} saved.')


def name_formation(addres, suffix='.html'):
    path_parse = urlparse(addres)
    path = os.path.splitext(path_parse.netloc + path_parse.path)[0]
    result = re.sub(r'\W', '-', path) + suffix
    logger.debug(f'Convert the path {addres} to a name {result}')
    return result


def defines_working_links(data, url):
    url_pars = urlparse(url)
    links = {}
    for tag in TAGS:
        for element in data.find_all(tag['tag']):
            addres = element.attrs.get(tag['type'])
            value = urlparse(addres)
            if not addres or value.netloc and value.netloc != url_pars.netloc:
                logger.debug('There is no link to another domain or link.')
                continue
            else:
                links[element] = tag['type']
    return links
