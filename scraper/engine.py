import requests
import json
import typing
from collections import deque
import csv

FILEMAME = 'Fortnite_stats'
FORMAT_CSV = 'csv'
FORMAT_JL = 'jl'
PAGE_NUMBER = 10


def start(start_url: str, callback: typing.Callable, max_page: int, output_file: str, file_format: str):
    out_file = open(f'{output_file}.{file_format}', 'w', buffering=1, encoding="utf-8")
    page = 0
    start_task = (start_url, callback)
    tasks = deque([start_task])
    try:
        while tasks and page < max_page:
            url, callback = tasks.pop()
            resp = requests.get(url)
            for result in callback(resp):
                if isinstance(result, dict):
                    if file_format == FORMAT_JL:
                        _write_jl(result, out_file)
                    elif file_format == FORMAT_CSV:
                        _write_csv(result, out_file)
                else:
                    tasks.append(result)
            page += 1
    finally:
        out_file.close()
        print('Work Done, Master')


def _write_jl(row, out_file):
    json.dump(row, out_file)
    out_file.write('\n')


def _write_csv(row, out_file):
    writer = csv.DictWriter(out_file, fieldnames=row.keys())
    if out_file.tell() == 0:
        writer.writeheader()
    writer.writerow(row)
