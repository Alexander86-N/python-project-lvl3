import os
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from progress.bar import ShadyBar
from page_loader.working_with_url import extract_data_from_url, changes_the_name
from page_loader.work_with_file_system import writes_data_file
logger = logging.getLogger(__name__)


TAGS = {'img': 'src',
        'link': 'href',
        'script': 'src'}


def resource_extraction(elementary_url, data, directory, name_dir):
    """Downloads local resources of the main page.
       All links are replaced with links pointing to files in the directory."""
    url_pars = urlparse(elementary_url)
    logger.debug('Starting resource extraction.')
    soup = BeautifulSoup(data, 'html.parser')
    links = defines_working_links(soup, elementary_url)
    progres = ShadyBar('Downloading: ', max=len(links))
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
        data_url = extract_data_from_url(url)
        path = f'{directory}/{name}'
        writes_data_file(data_url, path)
        progres.next()
    logger.debug('Resource extraction completed.')
    progres.finish()
    return soup.prettify()


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
