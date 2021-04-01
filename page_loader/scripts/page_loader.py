#!/usr/bin/env python
import sys

from page_loader import download, arg_parser
import logging


def main():
    args = arg_parser.parse()
    try:
        logging.basicConfig(level=logging.INFO)
        logging.info('Start download')
        print('Path webpage: ', download(args.url, args.output))
    except Exception as e:
        logging.critical(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
