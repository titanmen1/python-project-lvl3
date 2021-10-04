import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser(description='Web page downloader')
    parser.add_argument('url')
    parser.add_argument(
        '-o',
        '--output',
        default='',
        help=f"output directory (default: '{os.getcwd()}')"
    )

    return parser.parse_args()
