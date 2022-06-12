import argparse
import os


def make_cli():
    parser = argparse.ArgumentParser(prog='page-loader',
                                     description='Page loader')
    parser.add_argument('url')
    parser.add_argument('path')
    parser.add_argument('-o', '--output', action="store_true",
                        help='sets the program launch directory')
    args = parser.parse_args()
    if args.output:
        path = os.getcwd()
        return args.url, path
    else:
        return args.url, args.path
