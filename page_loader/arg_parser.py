import argparse


def parse():
    parser = argparse.ArgumentParser(description='Page loader')
    parser.add_argument('url', type=str)
    parser.add_argument(
        '-o',
        '--output',
        help='path of output',
        default='',
    )
    return parser.parse_args()
