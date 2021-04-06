import argparse
import os


def parse():
    parser = argparse.ArgumentParser(description='Page loader')
    parser.add_argument('url', type=str)
    parser.add_argument(
        '-o',
        '--output',
        help='Path of output. Default: {0}'.format(os.getcwd()),
        default='',
    )
    return parser.parse_args()
