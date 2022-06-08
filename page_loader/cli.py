import argparse
import os


def make_cli():
    parser = argparse.ArgumentParser(prog='page-loader',
                                     description='Page loader')
    parser.add_argument('url')
    parser.add_argument('-o', '--output', default=os.getcwd(),
                        help='sets the program launch directory')
    args = parser.parse_args()
    return args.url, args.output
