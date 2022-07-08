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


def resource_extraction(elementary_url, directory, name_dir):
    """Downloads local resources of the main page.
       All links are replaced with links pointing to files in the directory."""
    data = extract_data_from_url(elementary_url)
    url_pars = urlparse(elementary_url)
    logger.debug('Starting resource extraction.')
    soup = BeautifulSoup(data, 'html.parser')
    links = defines_working_links(soup, elementary_url)
    progres = IncrementalBar('Downloading: ', max=len(links))
    for dataset, teg in links.items():
        addres = dataset.attrs[teg]
        value = urlparse(addres)
        logger.debug(f'Suitable link: {addres}')
        suffix = os.path.splitext(addres)[1]
        name = changes_the_name(f'{url_pars.netloc}{addres}', suffix)
        logger.debug(f'Resource name: {name}')
        dataset.attrs[teg] = f'{name_dir}/{name}'
        url = f'{url_pars.scheme}://{url_pars.netloc}{value.path}'
        data_url = extract_data_from_url(url)
        path = f'{directory}/{name}'
        writes_data_file(data_url, path)
        progres.next()
    logger.debug('Resource extraction completed.')
    progres.finish()
    return soup.prettify()


def extract_data_from_url(url):
    """Makes a request to the URL and returns its content."""
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


def changes_the_name(addres, suffix='.html'):
    """Generates the changed address of the resource."""
    path_parse = urlparse(addres)
    path = os.path.splitext(path_parse.netloc + path_parse.path)[0]
    result = re.sub(r'\W', '-', path) + suffix
    logger.debug(f'Convert the path {addres} to a name {result}')
    return result


def defines_working_links(data, url):
    """Generates a list of local and working links."""
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
    logger.debug(f'List of working links: {links}')
    return links
