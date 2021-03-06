#!/usr/bin/env python

import argparse
import os
import sys
import logging
from page_loader.download import download
from page_loader.logging import init_logger


def main():
    init_logger()
    logger = logging.getLogger(__name__)
    parser = argparse.ArgumentParser(prog='page-loader',
                                     description='Page loader')
    parser.add_argument('-o', '--output', action="store",
                        dest='path', metavar='OUTPUT',
                        default=os.getcwd(),
                        help='sets the program launch directory')
    parser.add_argument('url')
    args = parser.parse_args()
    try:
        result = download(args.url, args.path)
    except Exception as err:
        logger.error(err)
        sys.exit(1)
    print(f'Page was downloaded as {result}')
    sys.exit(0)


if __name__ == '__main__':
    main()
