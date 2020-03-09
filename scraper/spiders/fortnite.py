import requests
from parsel import Selector


BASE_URL = 'https://fortnitestats.net'
XPATH_TABLE = '//tr//td//text()[normalize-space() and not(contains(.,"#"))]'


def list_delimeter(list_to_delim: list, chunk_size: int, next_page: str) -> list:
    link = [BASE_URL + next_page]
    return [list_to_delim[x:x + chunk_size] + link for x in range(0, len(list_to_delim), chunk_size)]


def parse_headers(resp: requests.Response) -> list:
    sel = Selector(resp.text)
    header_css = 'th::text'
    return sel.css(header_css).getall()


def parse_top(resp: requests.Response, next_page: str) -> list:
    sel = Selector(resp.text)
    return list_delimeter(sel.xpath(XPATH_TABLE).getall(), len(parse_headers(resp)), next_page)


def making_dicts(resp: requests.Response, next_page: str) -> list:
    header = parse_headers(resp) + ['Link']
    table_data = parse_top(resp, next_page)
    return [dict(zip(header, rows)) for rows in table_data]


def parse_fortnite(resp: requests.Response) -> list:
    sel = Selector(resp.text)
    next_xpath = '//a[text()="Next Page"]/@href'
    next_page = sel.xpath(next_xpath).get()
    tasks = making_dicts(resp, next_page)
    if next_page:
        tasks.append((BASE_URL + next_page, parse_fortnite))
    return tasks

