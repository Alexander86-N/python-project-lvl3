import tempfile
import os
import requests_mock
import requests
from page_loader.download import download


correct_name = 'en-wikipedia.html'
addres = 'https://en.wikipedia.org'


def test_download(make_request, read_file):
    with tempfile.TemporaryDirectory() as temp:
        random_path = os.path.join(temp, correct_name)
        result = download(addres, temp)
        assert random_path == result
        assert make_request == read_file
