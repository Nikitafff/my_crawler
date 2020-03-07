import requests
from parsel import Selector
import pandas as pd

BASE_URL = 'https://www.worldometers.info/coronavirus/'

resp = requests.get(BASE_URL)
assert resp.status_code == 200, f'bad status code: {resp.status_code}'  # тело ответа содержит HTML
assert resp.text, f'response body is empty: resp.content'


def clean_data(list_to_clean):
    return list(map(str.strip, list_to_clean))


def list_delimeter(list_to_delim, chunk_size):
    return [tuple(list_to_delim[x:x+chunk_size], BASE_URL) for x in range(0, len(list_to_delim), chunk_size)]


def delete_blocker(block_word, data):
    del data[data.index(block_word) + 1]
    del data[data.index(block_word) - 1]


def parse(resp: requests.Response):
    sel = Selector(resp.text)
    header_css = 'th::text'
    table_rows_xpath = "//tr//td//text()"
    table_header = [url for url in sel.css(header_css).getall()][::2].append('link')
    table_data = clean_data(sel.xpath(table_rows_xpath).getall())
    delete_blocker('Diamond Princess', table_data)
    data = list_delimeter(table_data, len(table_header))
    df = pd.DataFrame(data, columns=table_header)
    return df.to_csv("covid19_statistics.csv", sep=';')
