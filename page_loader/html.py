import os
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from page_loader.url import changes_the_name
logger = logging.getLogger(__name__)


TAGS = {'img': 'src',
        'link': 'href',
        'script': 'src'}


def resource_extraction(elementary_url, data, directory, name_dir):
    """Collects local resources of the main page in the list.
       All links are replaced with links pointing to files in the directory."""
    resours = []
    url_pars = urlparse(elementary_url)
    logger.debug('Starting resource extraction.')
    soup = BeautifulSoup(data, 'html.parser')
    links = defines_working_links(soup, elementary_url)
    for dataset, teg in links.items():
        addres = dataset.attrs[teg]
        value = urlparse(addres)
        logger.debug(f'Suitable link: {addres}')
        suffix = os.path.splitext(addres)[1]
        logger.debug(f'Suffix: {suffix}')
        if not suffix:
            name = changes_the_name(f'{url_pars.netloc}{addres}')
        else:
            name = changes_the_name(f'{url_pars.netloc}{addres}', suffix)
        logger.debug(f'Resource name: {name}')
        dataset.attrs[teg] = f'{name_dir}/{name}'
        url = f'{url_pars.scheme}://{url_pars.netloc}{value.path}'
        path = f'{directory}/{name}'
        resours.append({'url': url,
                        'path': path})
    logger.debug('Resource extraction completed.')
    return resours, soup.prettify()


def defines_working_links(data, url):
    """Generates a list of local and working links."""
    url_pars = urlparse(url)
    links = {}
    for tag, attribute in TAGS.items():
        for element in data.find_all(tag):
            addres = element.attrs.get(attribute)
            value = urlparse(addres)
            if not addres or value.netloc and value.netloc != url_pars.netloc:
                logger.debug('There is no link to another domain or link.')
                continue
            else:
                links[element] = attribute
    logger.debug(f'List of working links: {links}')
    return links
