import tempfile
import sys
import os
import pytest
from page_loader.download import download


correct_name = 'ru-hexlet-io-courses.html'
addres = 'https://ru.hexlet.io/courses'
name_dir = 'ru-hexlet-io-courses_file'
file_name = 'ru-hexlet-io-assets-application.css'


def test_download_result(make_request):
    with tempfile.TemporaryDirectory() as temp:
        random_path = os.path.join(temp, correct_name)
        result = download(addres, temp)
        assert random_path == result
        assert os.path.exists(os.path.join(temp, name_dir))


def test_download_file_contents(make_request,
                                read_file_css,
                                read_correct_file):
    with tempfile.TemporaryDirectory() as temp:
        result = download(addres, temp)
        filename = os.path.join(os.path.join(temp, name_dir), file_name)
        with open(result) as f:
            html = f.read()
        with open(filename, 'rb') as f:
            css = f.read()
        assert read_correct_file == html
        assert read_file_css == css


def test_download_number_of_files(make_request):
    with tempfile.TemporaryDirectory() as temp:
        download(addres, temp)
        list_file = ['ru-hexlet-io-assets-application.css',
                     'ru-hexlet-io-assets-professions-nodejs.png',
                     'ru-hexlet-io-packs-js-runtime.js']
        assert os.listdir(os.path.join(temp, name_dir)) == list_file


def test_download_exceptions():
    with tempfile.TemporaryDirectory() as temp:
        with pytest.raises(ConnectionError):
            download('', temp)


def test_download_exceptions_status_code(make_request_exceptions):
    with tempfile.TemporaryDirectory() as temp:
        with pytest.raises(Warning):
            download(addres, temp)
