import os
from page_loader.loading import loading, name_formation

def download(url, filepath=os.getcwd()):
    file_name = name_formation(url)
    loading(url, file_name, 'w')
    filename = os.path.join(filepath, file_name)
    name_dir = name_formation(url, '_file')
    new_dir = os.mkdir(name_dir)
    return os.path.abspath(filename)
