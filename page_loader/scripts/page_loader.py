#!/usr/bin/env python

import logging
import sys

from page_loader.cli import parse_args
from page_loader import download


def main():
    args = parse_args()

    logging.basicConfig(level=logging.INFO)

    try:
        filepath = download(args.url, args.output)
        print(f"Page was downloaded as '{filepath}'")
    except Exception as e:
        logging.error(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
