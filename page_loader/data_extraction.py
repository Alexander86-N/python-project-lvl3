import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from page_loader.loading import loading, name_formation

TAGS = {'tag': 'img', 'url': 'scr'}

def data_extraction(url, file, directory):
    with open(file, 'r') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        for element in soup.find_all(TAGS['tag']):
            addres = TAGS['tag'].attrs.get('src')
            parsed = urlparse(addres)
            if parsed.netoc and pared.netoc != url.netoc:
                continue
            else:
                new_url, suffix = highlight_url_and_suffix(addres)
                file_name = name_formation(new_url, suffix)
                loading(addres, file_name, 'wb')
                TAGS['tag'].attrs.['src'] = urljoin(directory, file_name)



def highlight_url_and_suffix(url):
    if "?" in url:
        position = url.index('?')
        new_url = url[:position]
        return new_url, os.path.splitext(new_url)[1]
    else:
        return url, os.path.splitext(new_url)[1]
