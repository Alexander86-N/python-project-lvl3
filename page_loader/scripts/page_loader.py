#!/usr/bin/env python

from page_loader.cli import make_cli
from page_loader.download import download


def main():
    arg_one, arg_two = make_cli()
    print(download(arg_one, arg_two))


if __name__ == '__main__':
    main()
