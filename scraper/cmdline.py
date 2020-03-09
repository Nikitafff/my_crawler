import argparse

from scraper.commands import crawl
from scraper.engine import FILEMAME, FORMAT_CSV, FORMAT_JL, PAGE_NUMBER


def parse():
    parser = argparse.ArgumentParser(prog='scraper')
    subparsers = parser.add_subparsers()

    parser_crawl = subparsers.add_parser('crawl')
    parser_crawl.add_argument('-p', '--pages', default=PAGE_NUMBER)
    parser_crawl.add_argument('-o', '--outfile', metavar='FILE', default=FILEMAME)
    parser_crawl.add_argument('-f', '--format', default=FORMAT_CSV, choices=[FORMAT_CSV, FORMAT_JL])
    parser_crawl.set_defaults(func=crawl.execute)

    args = parser.parse_args()
    args.func(args)
