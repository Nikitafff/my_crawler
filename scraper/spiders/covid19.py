import requests
from parsel import Selector
import json
import sys
import typing
from collections import deque

BASE_URL = 'https://fortnitestats.net'


def list_delimeter(list_to_delim, chunk_size):
    return [list_to_delim[x:x + chunk_size] for x in range(0, len(list_to_delim), chunk_size)]


def parse_headers(resp):
    sel = Selector(resp.text)
    header_css = 'th::text'
    return sel.css(header_css).getall()


def parse_top(resp):
    sel = Selector(resp.text)
    table_rows_xpath = '//tr//td//text()[normalize-space() and not(contains(.,"#"))]'
    return list_delimeter(sel.xpath(table_rows_xpath).getall(), len(parse_headers(resp)))


def making_dicts(resp):
    return [dict(zip(parse_headers(resp), rows)) for rows in parse_top(resp)]


def parse_fortnite(resp: requests.Response):
    sel = Selector(resp.text)
    tasks = making_dicts(resp)
    next_xpath = '//a[text()="Next Page"]/@href'
    next_page = sel.xpath(next_xpath).get()
    if next_page:
        tasks.append((BASE_URL + next_page, parse_fortnite))
    return tasks


def start(start_url: str, callback: typing.Callable, max_page, output_file):
    out_file = open(output_file, 'w', buffering=1)
    page = 0
    start_task = (start_url, callback)
    tasks = deque([start_task])
    try:
        while tasks and page < max_page:
            url, callback = tasks.pop()
            resp = requests.get(url)
            for result in callback(resp):
                if isinstance(result, dict):
                    _write_jl(result, out_file)
                else:
                    tasks.append(result)
            page += 1
    finally:
        out_file.close()
        print('done')


def _write_jl(row, out_file):
    json.dump(row, out_file)
    out_file.write('\n')


start(BASE_URL, parse_fortnite, max_page = 10, output_file = 'fortnite.csv')