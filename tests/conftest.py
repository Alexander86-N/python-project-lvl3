import pytest
import tempfile


@pytest.fixture
def read_file():
    with open('tests/fixtures/test_html.html', 'r') as f:
        result = f.read()
    return result


@pytest.fixture
def read_correct_file():
    with open('tests/fixtures/correct_html.html', 'r') as f:
        result = f.read()
    return result


@pytest.fixture
def read_file_css():
    with open('tests/fixtures/test_file.css', 'rb') as f:
        result = f.read()
    return result


@pytest.fixture
def read_file_js():
    with open('tests/fixtures/test_file.js', 'rb') as f:
        result = f.read()
    return result


@pytest.fixture
def read_file_img():
    with open('tests/fixtures/test_image/test_file_img.png', 'rb') as f:
        result = f.read()
    return result


@pytest.fixture
def make_request(requests_mock,
                 read_file,
                 read_file_css,
                 read_file_js,
                 read_file_img):
    requests_mock.get('https://ru.hexlet.io/courses', text=read_file,
                      headers={'content-type': 'all'})
    requests_mock.get('https://ru.hexlet.io/assets/professions/nodejs.png',
                      content=read_file_img, headers={'content-type': 'all'})
    requests_mock.get('https://ru.hexlet.io/assets/application.css',
                      content=read_file_css, headers={'content-type': 'all'})
    requests_mock.get('https://ru.hexlet.io/packs/js/runtime.js',
                      content=read_file_js, headers={'content-type': 'all'})
    requests_mock.get('https://ru.hexlet.io/courses', text=read_file,
                      headers={'content-type': 'all'})
    yield

    assert requests_mock.call_count == 5


@pytest.fixture
def make_request_exceptions(requests_mock,
                            read_file):
    requests_mock.get('https://ru.hexlet.io/courses', text=read_file,
                      headers={'content-type': 'all'}, status_code=404)
