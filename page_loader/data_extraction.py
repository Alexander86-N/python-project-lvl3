import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


TAGS = {'tag': 'img', 'type': 'src'}


def resource_extraction(url, data, directory):
    resource_lst = []
    soup = BeautifulSoup(data, 'html.parser')
    for element in soup.find_all(TAGS['tag']):
        addres = element.attrs.get(TAGS['type'])
        if not addres:
            continue
        addres_pars = urlparse(addres)
        url_pars = urlparse(url)
        if addres_pars.netloc and addres_pars.netloc != url_pars.netloc:
            continue
        else:
            new_url, suffix = highlight_url_and_suffix(addres)
            name = name_formation(new_url, suffix)
            new_url = f'{url_pars.scheme}://{url_pars.netloc}{addres}'
            element.attrs[TAGS['type']] = f'{directory}/{name}'
            resource_lst.append({'addres': new_url,
                                 'name': element.attrs[TAGS['type']]})
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
