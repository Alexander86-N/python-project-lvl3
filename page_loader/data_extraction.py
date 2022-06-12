import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


TAGS = [{'tag': 'img', 'type': 'src'},
        {'tag': 'link', 'type': 'href'},
        {'tag': 'script', 'type': 'src'}]


def resource_extraction(url, data, directory):
    resource_lst = []
    soup = BeautifulSoup(data, 'html.parser')
    for tag in TAGS:
        for element in soup.find_all(tag['tag']):
            addres = element.attrs.get(tag['type'])
            if not addres:
                continue
            resours = urlparse(addres)
            url_pars = urlparse(url)
            if resours.netloc and resours.netloc != url_pars.netloc:
                continue
            else:
                new_url, suffix = highlight_url_and_suffix(addres)
                name = name_formation(f'{url_pars.netloc}{new_url}', suffix)
                url = f'{url_pars.scheme}://{url_pars.netloc}{resours.path}'
                element.attrs[tag['type']] = f'{directory}/{name}'
                resource_lst.append({'addres': url,
                                     'name': element.attrs[tag['type']]})
    return resource_lst, soup.prettify()


def extraction_data(url):
    response = requests.get(url)
    if response.headers['Content-Type'] == 'text/html':
        response.encoding = 'utf-8'
        return response.text
    else:
        return response.content


def highlight_url_and_suffix(url):
    if "?" in url:
        position = url.index('?')
        new_url = url[:position]
        return new_url, os.path.splitext(new_url)[1]
    else:
        return url, os.path.splitext(url)[1]


def name_formation(addres, suffix='.html'):
    path_parse = urlparse(addres)
    path = os.path.splitext(path_parse.netloc + path_parse.path)[0]
    result = ''.join([sing if sing.isalnum() else sing.replace(sing, '-')
                      for sing in path]) + suffix
    return result
