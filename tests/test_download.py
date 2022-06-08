import tempfile
import os
from page_loader.download import download


correct_name = 'en-wikipedia.html'
addres = 'https://en.wikipedia.org'
img_addres = 'https://en.wikipedia.org/assets/professions/nodejs.png'
correct_name_dir = 'en-wikipedia_file'


def test_download(read_file, requests_mock):
    with tempfile.TemporaryDirectory() as temp:
        random_path = os.path.join(temp, correct_name)
        requests_mock.get('https://en.wikipedia.org', text=read_file, 
                          headers={'Content-Type': 'text/html'})
        requests_mock.get('https://en.wikipedia.org/assets/professions/nodejs.png', text=read_file,
                          headers={'Content-Type': 'all'})
        result = download('https://en.wikipedia.org', temp)
        assert random_path == result
        assert os.path.isdir(correct_name_dir)
        assert os.path.isfile('en-wikipedia_file/-assets-professions-nodejs.png')
