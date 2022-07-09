#!/usr/bin/env python

import argparse
import os
import sys
from page_loader.download import download
from page_loader.init_logger import logger


def main():
    parser = argparse.ArgumentParser(prog='page-loader',
                                     description='Page loader')
    parser.add_argument('url')
    parser.add_argument('path')
    parser.add_argument('-o', '--output', action="store_true",
                        help='sets the program launch directory')
    args = parser.parse_args()
    if args.output:
        url = args.url
        path = os.getcwd()
    else:
        url = args.url
        path = args.path
    try:
        result = download(url, path)
    except Exception as err:
        logger.error(err)
        sys.exit(1)
    print(f'Page was downloaded as {result}')
    sys.exit(0)


if __name__ == '__main__':
    main()
