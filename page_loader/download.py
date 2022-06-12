import os
from urllib.parse import urlparse
from page_loader.data_extraction import resource_extraction, extraction_data


def download(url, filepath):
    title = name_formation(url)
    filename = os.path.join(filepath, title)
    data = extraction_data(url)

    name_dir = name_formation(url, '_file')
    new_dir = os.path.join(filepath, name_dir)
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)

    urls, text_html = resource_extraction(url, data, new_dir)
    saving_data(text_html, filename)
    for url in urls:
        data_url = extraction_data(url['addres'])
        saving_data(data_url, url['name'])
    return os.path.abspath(filename)


def saving_data(data, file_name):
    if isinstance(data, str):
        with open(file_name, 'w') as fp:
            fp.write(data)
    else:
        with open(file_name, 'wb') as fp:
            fp.write(data)


def name_formation(addres, suffix='.html'):
    path_parse = urlparse(addres)
    path = os.path.splitext(path_parse.netloc + path_parse.path)[0]
    result = ''.join([sing if sing.isalnum() else sing.replace(sing, '-')
                      for sing in path]) + suffix
    return result
