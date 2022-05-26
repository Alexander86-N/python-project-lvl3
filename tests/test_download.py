import tempfile
import os
import requests_mock
import requests
from page_loader.download import download


correct_name = 'en-wikipedia-org-wiki-Main-Page.html'
addres = 'https://en.wikipedia.org/wiki/Main_Page'


def test_download():
    with tempfile.TemporaryDirectory() as temp:
        random_path = os.path.join(temp, correct_name)
        with requests_mock.Mocker() as mock:
            mock.get(addres, text='hello')
            responce = requests.get(addres)
            result = download(addres, temp)
    assert random_path == result
    assert responce.text == 'hello'
