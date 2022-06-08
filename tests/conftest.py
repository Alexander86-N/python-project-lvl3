import pytest
import requests


@pytest.fixture(params=['tests/fixtures/test_html.html'])
def read_file(request):
    file_name = request.param
    with open(file_name) as f:
        result = f.read()
    return result


@pytest.fixture
def make_request(requests_mock, read_file):
    requests_mock.get('https://en.wikipedia.org', text=read_file,
                      headers={'content-type': 'text/html'})
    yield
