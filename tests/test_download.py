import tempfile
import sys
import os
import pytest
import requests
import subprocess
import requests_mock
from page_loader.download import download
from page_loader.scripts.page_loader import main


correct_name = 'ru-hexlet-io-courses.html'
addres = 'https://ru.hexlet.io/courses'
name_dir = 'ru-hexlet-io-courses_files'
file_name = 'ru-hexlet-io-assets-application.css'


def test_download_result(make_request):
    with tempfile.TemporaryDirectory() as temp:
        random_path = os.path.join(temp, correct_name)
        result = download(temp, addres)
        assert random_path == result
        assert os.path.exists(os.path.join(temp, name_dir))


def test_download_file_contents(make_request,
                                read_file_css,
                                read_correct_file):
    with tempfile.TemporaryDirectory() as temp:
        result = download(temp, addres)
        filename = os.path.join(os.path.join(temp, name_dir), file_name)
        with open(result) as f:
            html = f.read()
        with open(filename, 'rb') as f:
            css = f.read()
        assert read_correct_file == html
        assert read_file_css == css
        assert os.path.exists(filename)


def test_download_number_of_files(make_request):
    with tempfile.TemporaryDirectory() as temp:
        download(temp, addres)
        assert len(os.listdir(temp)) == 2
        assert len(os.listdir(os.path.join(temp, name_dir))) == 4


def test_download_exceptions():
    with tempfile.TemporaryDirectory() as temp:
        with pytest.raises(ConnectionError):
            download(temp, '')


def test_download_exceptions_status_code(make_request_exceptions):
    with tempfile.TemporaryDirectory() as temp:
        with pytest.raises(Warning):
            download(temp, addres)

def test_download_exception_dir():
    with tempfile.TemporaryDirectory() as temp:
        os.mkdir(os.path.join(temp, name_dir))
        with pytest.raises(FileExistsError):
            download(temp, addres)


def test_connection_error(requests_mock):
    requests_mock.get(addres, exc=requests.exceptions.ConnectionError)
    with tempfile.TemporaryDirectory() as tmpdirname:
        assert not os.listdir(tmpdirname)
        with pytest.raises(Exception):
            assert download(tmpdirname, addres)
        assert not os.listdir(tmpdirname)


def test_page_loader():
    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run(['page-loader', '-o', tmp, addres],
                                encoding='utf-8',
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        assert result.returncode == 0
#        assert '' == result.stdout
