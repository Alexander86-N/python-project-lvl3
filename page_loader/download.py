import os
import requests


def download(url, filepath=os.getcwd()):
    new_path = name_formation(url)
    filename = os.path.join(filepath, new_path)
    with open(new_path, 'w') as f:
        r = requests.get(url)
        f.write(r.text)
    name_dir = name_formation(url, '_file')
    new_dir = os.mkdir(name_dir)
    return os.path.abspath(filename)


def name_formation(addres, suffix='.html'):
    path = os.path.splitext(addres.split('//')[1])[0]
    new_path = ''
    for sing in path:
        new_path += sing if sing.isalnum() else sing.replace(sing, '-')
    return new_path + suffix
