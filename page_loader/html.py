import logging
from os import path
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from page_loader.url import to_filename
logger = logging.getLogger(__name__)


TAGS = {'img': 'src',
        'link': 'href',
        'script': 'src'}


def get_resources(root_url, data, name_dir):
    """Collects local resources of the main page in the list.
       All links are replaced with links pointing to files in the directory."""
    resours = []
    logger.debug('Starting resource extraction.')
    soup = BeautifulSoup(data, 'html.parser')
    links = get_links(soup, root_url)
    for dataset, teg in links.items():
        addres = dataset.attrs[teg]
        logger.debug(f'Suitable link: {addres}')
        name = to_filename(f'{urlparse(root_url).netloc}{addres}')
        dataset.attrs[teg] = path.join(name_dir, name)
        url = urljoin(root_url, urlparse(addres).path)
        resours.append({'url': url,
                        'name': name})
    logger.debug('Resource extraction completed.')
    return resours, soup.prettify()


def get_links(data, url):
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
