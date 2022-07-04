#!/usr/bin/env python

import logging
from page_loader.cli import make_cli
from page_loader.download import download
from page_loader.init_logger import init_logger


def main():
    init_logger('page_loader')
    logger = logging.getLogger('page_loader.page_loader')
    arg_one, arg_two = make_cli()
    try:
        path = download(arg_one, arg_two)
    except Exception as err:
        logger.error(err)
        exit(1)
    else:
        print(path)
        exit(0)


if __name__ == '__main__':
    main()
