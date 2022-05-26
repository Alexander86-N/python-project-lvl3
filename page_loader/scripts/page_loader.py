#!/usr/bin/env python

import argparse
import os
from page_loader.download import download


def main():
    parser = argparse.ArgumentParser(prog='page-loader',
                                     description='Page loader')
    parser.add_argument('url')
    parser.add_argument('-o', '--output', default=os.getcwd(),
                        help='sets the program launch directory')
    args = parser.parse_args()
    print(download(args.url, args.output))


if __name__ == '__main__':
    main()
