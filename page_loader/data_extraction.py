from bs4 import BeautifulSoup


TAG = {'tag': 'img', 'url': 'scr'}

def data_extraction(file_path, tags):
    soup = BeautifulSoup(file_path, 'html.parser')
