import tempfile
import os
import pathlib
from page_loader.download import download


correct_name = 'ru-hexlet-io-courses.html'
addres = 'https://ru.hexlet.io/courses'
img_addres = 'https://ru.hexlet.io/assets/professions/nodejs.png'
correct_name_dir = 'ru-hexlet-io-courses_files'


def test_download(read_file,
                  read_file_css,
                  read_file_js,
                  read_file_img,
                  requests_mock):
    with tempfile.TemporaryDirectory() as temp:
        random_path = os.path.join(temp, correct_name)
        requests_mock.get('https://ru.hexlet.io/courses', text=read_file, 
                          headers={'Content-Type': 'text/html'})
        requests_mock.get('https://ru.hexlet.io/assets/professions/nodejs.png',
                          content=read_file_img, headers={'Content-Type': 'all'})
        requests_mock.get('https://ru.hexlet.io/assets/application.css',
                          content=read_file_css, headers={'content-type': 'all'})
        requests_mock.get('https://ru.hexlet.io/courses', content=read_file_css,
                          headers={'content-type': 'all'})
        requests_mock.get('https://ru.hexlet.io/packs/js/runtime.js',
                          content=read_file_js, headers={'content-type': 'all'})
        result = download('https://ru.hexlet.io/courses', temp)
        assert random_path == result
        assert os.path.isdir(os.path.abspath(correct_name_dir))
        assert os.path.isfile('ru-hexlet-io-assets-professions-nodejs.png')
