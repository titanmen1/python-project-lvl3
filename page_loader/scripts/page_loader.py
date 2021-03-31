#!/usr/bin/env python
from page_loader import download, arg_parser


def main():
    args = arg_parser.parse()
    print(download(args.url, args.output))


if __name__ == '__main__':
    main()
