import tempfile
import os
import pytest
import requests
import subprocess
from page_loader.download import download, get_data
from page_loader.url import to_directory, to_filename
from page_loader.html import get_resources
from page_loader.storage import save


correct_name = 'ru-hexlet-io-courses.html'
addres = 'https://ru.hexlet.io/courses'
name_dir = 'ru-hexlet-io-courses_files'
file_name = 'ru-hexlet-io-assets-application.css'
IMG = 'https://ru.hexlet.io/assets/professions/nodejs.png'
CSS = 'https://ru.hexlet.io/assets/application.css'
JS = 'https://ru.hexlet.io/packs/js/runtime.js'


def test_download_result(requests_mock,
                         read_file,
                         read_file_css,
                         read_file_js,
                         read_file_img):
    requests_mock.get(addres, text=read_file)
    requests_mock.get(IMG, content=read_file_img)
    requests_mock.get(CSS, content=read_file_css)
    requests_mock.get(JS, content=read_file_js)
    with tempfile.TemporaryDirectory() as temp:
        random_path = os.path.join(temp, correct_name)
        result = download(addres, temp)
        assert random_path == result
        assert os.path.exists(os.path.join(temp, name_dir))


def test_download_file_contents(requests_mock,
                                read_file,
                                read_correct_file,
                                read_file_css,
                                read_file_js,
                                read_file_img):
    requests_mock.get(addres, text=read_file)
    requests_mock.get(IMG, content=read_file_img)
    requests_mock.get(CSS, content=read_file_css)
    requests_mock.get(JS, content=read_file_js)
    with tempfile.TemporaryDirectory() as temp:
        result = download(addres, temp)
        filename = os.path.join(os.path.join(temp, name_dir), file_name)
        with open(result) as f:
            html = f.read()
        with open(filename, 'rb') as f:
            css = f.read()
        assert read_correct_file == html
        assert read_file_css == css
        assert os.path.exists(filename)


def test_download_number_of_files(requests_mock,
                                  read_file,
                                  read_file_css,
                                  read_file_js,
                                  read_file_img):
    requests_mock.get(addres, text=read_file)
    requests_mock.get(IMG, content=read_file_img)
    requests_mock.get(CSS, content=read_file_css)
    requests_mock.get(JS, content=read_file_js)
    with tempfile.TemporaryDirectory() as temp:
        download(addres, temp)
        assert len(os.listdir(temp)) == 2
        assert len(os.listdir(os.path.join(temp, name_dir))) == 4


def test_download_exceptions():
    with tempfile.TemporaryDirectory() as temp:
        with pytest.raises(ConnectionError):
            download('', temp)


def test_download_exceptions_status_code(requests_mock, read_file):
    requests_mock.get(addres, text=read_file, status_code=404)
    with tempfile.TemporaryDirectory() as temp:
        with pytest.raises(ConnectionError):
            download(addres, temp)


def test_download_exception_dir():
    with tempfile.TemporaryDirectory() as temp:
        os.mkdir(os.path.join(temp, name_dir))
        with pytest.raises(FileExistsError):
            download(addres, temp)


def test_connection_error(requests_mock):
    requests_mock.get(addres, exc=requests.exceptions.ConnectionError)
    with tempfile.TemporaryDirectory() as tmpdirname:
        assert not os.listdir(tmpdirname)
        with pytest.raises(Exception):
            assert download(addres, tmpdirname)
        assert not os.listdir(tmpdirname)


def test_page_loader():
    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run(['page-loader', '-o', tmp, addres],
                                encoding='utf-8',
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        assert result.returncode == 0


@pytest.mark.parametrize('link, expected', [
    ('https://ru.hexlet.io/courses',
     'ru-hexlet-io-courses.html'),
    ('https://ru.hexlet.io/assets/professions/nodejs.png',
     'ru-hexlet-io-assets-professions-nodejs.png'),
    ('https://ru.hexlet.io/assets/application.css.js',
     'ru-hexlet-io-assets-application-css.js')])
def test_to_filename(link, expected):
    result = to_filename(link)
    assert result == expected


@pytest.mark.parametrize('link, expected', [
    ('https://ru.hexlet.io/courses',
     'ru-hexlet-io-courses_files'),
    ('https://ru.hexlet.io/assets/professions/nodejs.png',
     'ru-hexlet-io-assets-professions-nodejs_files'),
    ('https://ru.hexlet.io/assets/application.css.js',
     'ru-hexlet-io-assets-application-css_files')])
def test_to_directory(link, expected):
    result = to_directory(link)
    assert result == expected


def test_get_resours(requests_mock,
                     read_file,
                     read_correct_file):
    requests_mock.get(addres, text=read_file)
    response = get_data(addres)
    resources, html = get_resources(addres, response, name_dir)
    result = [{'name': 'ru-hexlet-io-assets-professions-nodejs.png',
               'url': 'https://ru.hexlet.io/assets/professions/nodejs.png'},
              {'name': 'ru-hexlet-io-assets-application.css',
               'url': 'https://ru.hexlet.io/assets/application.css'},
              {'name': 'ru-hexlet-io-courses.html',
               'url': 'https://ru.hexlet.io/courses'},
              {'name': 'ru-hexlet-io-packs-js-runtime.js',
               'url': 'https://ru.hexlet.io/packs/js/runtime.js'}]
    assert html == read_correct_file
    assert resources == result


def test_save(read_correct_file, read_file_img):
    with tempfile.TemporaryDirectory() as temp:
        path_html = os.path.join(temp, 'one.html')
        path_img = os.path.join(temp, 'image.png')
        save(read_correct_file, path_html)
        save(read_file_img, path_img)
        with open(path_html) as f:
            html = f.read()
        with open(path_img, 'rb') as f:
            img = f.read()
        assert read_correct_file == html
        assert read_file_img == img
        assert os.path.exists(path_html)
        assert os.path.exists(path_img)
