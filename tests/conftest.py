import pytest
import requests
import requests_mock



@pytest.fixture
def read_file():
    result = ''
    file_name = 'tests/fixtures/loaded.txt'
    with open(file_name) as f:
        result = f.read()
    return result


@pytest.fixture
def make_request(read_file):
    with requests_mock.Mocker() as mock:
        mock.get('https://en.wikipedia.org',text=read_file)
        return requests.get('https://en.wikipedia.org').text
