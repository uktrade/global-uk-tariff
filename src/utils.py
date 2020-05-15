import csv
import json
import os
from io import BytesIO, StringIO
from typing import Tuple, List
from uuid import uuid4

import flask
import requests
from xlsxwriter import Workbook

GA_TRACKING_ID = os.getenv("GA_TRACKING_ID")
GA_TRACKING_URL = "https://www.google-analytics.com/collect"

DATA_FILEPATH = "data.json"

FILTER_ARG = "q"

DEFAULT_FILTER = ""
DEFAULT_PAGE = 1
DEFAULT_SAMPLE_SIZE = 25
with open(DATA_FILEPATH) as _data_file:
    DEFAULT_DATA = json.load(_data_file)


def get_positive_int_request_arg(
    name: str, default: int, request: flask.Request = flask.request
):
    value = request.args.get(name, default, type=int)

    # No int arguments should be below 1 - in some cases this can cause a ZeroDivisionError
    # Provide a reasonable alternative instead
    if value < 1:
        return default
    return value


def get_filtered_data(data: List[dict], filters: List[str]) -> List[dict]:
    """
    Filters the data on a set of given keywords.

    If multiple filters are give these should operate on an AND basis.

    i.e. the row must contain all given filters for it to be returned.
    """
    if not filters:
        return data

    new_data = []
    for row in data:
        str_row = [str(item).lower() for item in row.values()]
        for sub_filter in filters:
            if not any(sub_filter in item for item in str_row):
                break
        else:
            new_data.append(row)

    return new_data


def get_data(
    filter_param: str = DEFAULT_FILTER,
    offset: int = DEFAULT_PAGE - 1,
    sample_size: int = DEFAULT_SAMPLE_SIZE,
    get_all: bool = False,
    filepath: str = None,
) -> Tuple[List[dict], int]:
    if not filepath:
        json_data = DEFAULT_DATA
    else:
        with open(filepath) as data_file:
            json_data = json.load(data_file)

    filters = (
        [sub_filter.lower() for sub_filter in filter_param.split(" ")]
        if filter_param
        else []
    )

    json_data = get_filtered_data(json_data, filters)

    start_node = offset * sample_size
    if get_all:
        return json_data, len(json_data)
    return json_data[start_node : start_node + sample_size], len(json_data)


def get_data_from_request(
    request: flask.Request = flask.request, **kwargs
) -> Tuple[List[dict], int]:
    filter_arg = request.args.get(FILTER_ARG, DEFAULT_FILTER)
    offset = get_positive_int_request_arg("p", DEFAULT_PAGE) - 1
    sample_size = get_positive_int_request_arg("n", DEFAULT_SAMPLE_SIZE)

    return get_data(filter_arg, offset, sample_size, **kwargs)


def get_data_as_list(filter_param: str) -> List[List[str]]:
    raw_data = get_data(filter_param, get_all=True)[0]
    if raw_data:
        headers = list(raw_data[0].keys())
    else:
        headers = [
            "commodity",
            "description",
            "cet_duty_rate",
            "ukgt_duty_rate",
            "change",
        ]

    data = [[row[header] for header in headers] for row in raw_data]

    return [headers] + data


def format_data_as_csv(data: List[List[str]]) -> StringIO:
    output = StringIO()
    writer = csv.writer(output)
    writer.writerows(data)
    output.seek(0)
    return output


def format_data_as_xlsx(data: List[List[str]]) -> BytesIO:
    output = BytesIO()
    with Workbook(output) as workbook:
        worksheet = workbook.add_worksheet()
        for row_num, row in enumerate(data):
            for col_num, col in enumerate(row):
                worksheet.write(row_num, col_num, col)

    output.seek(0)
    return output


def get_pages(start_page: int, max_page: int, page_range: int = 2) -> List[int]:
    min_page = 1
    pages = [
        page
        for page in range(start_page - page_range, start_page + page_range + 1)
        if 0 < page <= max_page
    ]

    if not pages:  # edge case where there are no results.
        return [1]

    if min_page not in pages:
        pages = [min_page, "..."] + pages
    if max_page not in pages:
        pages = pages + ["...", max_page]

    return pages


def send_analytics(path: str, host: str, remote_addr: str, user_agent: str, **kwargs):
    if not path.startswith("/static") and GA_TRACKING_ID:
        remote_addr = ".".join(remote_addr.split(".")[:3]) + ".0"
        data = {
            "v": "1",
            "tid": GA_TRACKING_ID,
            "cid": str(uuid4()),
            "uip": remote_addr,
            "aip": 1,  # Ensure IPs are anonymised
            "t": "pageview",
            "dp": path,
            "dh": host,
            "ua": user_agent,
            **kwargs,
        }
        requests.post(
            GA_TRACKING_URL, data=data,
        )
