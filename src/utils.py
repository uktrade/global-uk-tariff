import json
from io import BytesIO
from typing import Tuple, List

import flask
from xlsxwriter import Workbook

DATA_FILEPATH = "data.json"

DEFAULT_PAGE = 1
DEFAULT_SAMPLE_SIZE = 25


def get_positive_int_request_arg(
    name: str, default: int, request: flask.Request = flask.request
):
    value = request.args.get(name, default, type=int)

    # No int arguments should be below 1 - in some cases this can cause a ZeroDivisionError
    # Provide a reasonable alternative instead
    if value < 1:
        return default
    return value


def get_data(
    filter_param: str = None,
    offset: int = DEFAULT_PAGE - 1,
    sample_size: int = DEFAULT_SAMPLE_SIZE,
    get_all: bool = False,
    filepath: str = None,
) -> Tuple[List[dict], int]:
    with open(filepath or DATA_FILEPATH) as data_file:
        json_data = json.load(data_file)
    if filter_param is not None:
        json_data = [
            row
            for row in json_data
            if any(filter_param.lower() in str(value).lower() for value in row.values())
        ]
    start_node = offset * sample_size
    if get_all:
        return json_data, len(json_data)
    return json_data[start_node : start_node + sample_size], len(json_data)


def get_data_from_request(
    request: flask.Request = flask.request,
) -> Tuple[List[dict], int]:
    filter_arg = request.args.get("filter")
    offset = get_positive_int_request_arg("p", DEFAULT_PAGE) - 1
    sample_size = get_positive_int_request_arg("n", DEFAULT_SAMPLE_SIZE)

    return get_data(filter_arg, offset, sample_size)


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


def format_data_as_csv(data: List[List[str]]) -> str:
    formatted_data = ""
    for row in data:
        str_row = ",".join(row)
        formatted_data += str_row + "\n"
    return formatted_data


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
