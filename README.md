### Hexlet tests and linter status:
[![Actions Status](https://github.com/Alexander86-N/python-project-lvl3/workflows/hexlet-check/badge.svg)](https://github.com/Alexander86-N/python-project-lvl3/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/bcd48b207ab114cb2978/maintainability)](https://codeclimate.com/github/Alexander86-N/python-project-lvl3/maintainability)
[![example workflows](https://github.com/Alexander86-N/python-project-lvl3/actions/workflows/check-file.yml/badge.svg)](https://github.com/Alexander86-N/python-project-lvl3/actions)
[![Test Coverage](https://api.codeclimate.com/v1/badges/bcd48b207ab114cb2978/test_coverage)](https://codeclimate.com/github/Alexander86-N/python-project-lvl3/test_coverage)

# PAGE LOADER

 The utility downloads the page from the network and puts it in the specified directory.
 About the utility:
 - the page is loaded in formatted html format,
 - downloads the content located in the same domain,
 - at the end gives the full address of the downloaded page.

## How to install and use

### Install
`python3 -m pip install git+https://github.com/Alexander86-N/python-project-lvl3.git`

### Use as a library
```
from page_loader import download

file_path = download(url, filepath=os.getcwd())
print(file_path)
```

### CLI
```
usage: page-loader [-h] [-o OUTPUT] url

Page loader

positional arguments:
  url

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        sets the program launch directory
```

## Demonstration of all the steps to implement the program

[![asciicast](https://asciinema.org/a/rmwchODDQcMV3nAA7g8pRuaRT.svg)](https://asciinema.org/a/rmwchODDQcMV3nAA7g8pRuaRT)
[![asciicast](https://asciinema.org/a/4PoAFBFKiLwsFeIkk4NRMMcjw.svg)](https://asciinema.org/a/4PoAFBFKiLwsFeIkk4NRMMcjw)
[![asciicast](https://asciinema.org/a/dl0kf052zA95BVcOKi4A1i2fV.svg)](https://asciinema.org/a/dl0kf052zA95BVcOKi4A1i2fV)
### The final version.
[![asciicast](https://asciinema.org/a/uttwJkxtwYHKlRfKIiBnLvCcp.svg)](https://asciinema.org/a/uttwJkxtwYHKlRfKIiBnLvCcp)
