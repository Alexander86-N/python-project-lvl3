import pytest


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
