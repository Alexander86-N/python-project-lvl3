import os
import requests


def loading(url, file_name, mode='w'):
    response = requests.get(url)
    if mode == 'wb':
        with open(file_name, 'wb') as fp:
            fp.write(response.content)
    if mode == 'w':
        with open(file_name, 'w') as fp:
            fp.write(response.text)


def name_formation(addres, suffix='.html'):
    path = os.path.splitext(addres.split('//')[1])[0]
    new_path = ''
    for sing in path:
        new_path += sing if sing.isalnum() else sing.replace(sing, '-')
    return new_path + suffix
    
