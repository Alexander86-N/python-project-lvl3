import os
import requests


def loading(url, file_path):
    file_name = name_formation(url)
    new_path = os.path.join(file_path, file_name)
    with open(file_name, 'w') as fp:
        request = requests.get(url)
        fp.write(request.text)
    return filename
