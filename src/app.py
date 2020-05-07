import logging
import math
import os
from concurrent.futures.thread import ThreadPoolExecutor

import flask
from flask import request, Response
from whitenoise import WhiteNoise

from src import decorators, utils

app = flask.Flask(__name__)
app.wsgi_app = WhiteNoise(app.wsgi_app, root="static/")


thread_pool = ThreadPoolExecutor()


@app.route("/")
@decorators.cache_without_request_args()
def home():
    return flask.render_template("home.html")


@app.route("/healthcheck")
def healthcheck():
    response = flask.Response(
        """\
<pingdom_http_custom_check>
    <status>OK</status>
    <response_time>1</response_time>
</pingdom_http_custom_check>"""
    )
    response.headers["Content-Type"] = "text/xml"
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"

    return response


@app.route("/tariff")
@decorators.cache_without_request_args(
    q=utils.DEFAULT_FILTER, p=utils.DEFAULT_PAGE, n=utils.DEFAULT_SAMPLE_SIZE
)
@decorators.compress_response
def tariff():
    data, total = utils.get_data_from_request()
    page = utils.get_positive_int_request_arg("p", utils.DEFAULT_PAGE)
    sample_size = utils.get_positive_int_request_arg("n", utils.DEFAULT_SAMPLE_SIZE)
    max_page = math.ceil(total / sample_size)

    return flask.render_template(
        "tariff.html",
        all_data=utils.get_data(get_all=True)[0],
        data=data,
        total=total,
        pages=utils.get_pages(page, max_page),
        page=page,
        max_page=total / sample_size,
        sample_size=sample_size,
        start_index=(sample_size * (page - 1)) + 1 if len(data) != 0 else 0,
        stop_index=sample_size * page if sample_size * page < total else total,
    )


@app.route("/api/global-uk-tariff.csv")
@decorators.cache_without_request_args(
    q=utils.DEFAULT_FILTER, p=utils.DEFAULT_PAGE, n=utils.DEFAULT_SAMPLE_SIZE
)
@decorators.compress_response
def tariff_csv():
    filter_arg = request.args.get(utils.FILTER_ARG)
    data = utils.get_data_as_list(filter_arg)
    output = utils.format_data_as_csv(data)
    return flask.send_file(output, mimetype="text/csv",)


@app.route("/api/global-uk-tariff.xlsx")
@decorators.cache_without_request_args(
    q=utils.DEFAULT_FILTER, p=utils.DEFAULT_PAGE, n=utils.DEFAULT_SAMPLE_SIZE
)
@decorators.compress_response
def tariff_xlsx():
    filter_arg = request.args.get(utils.FILTER_ARG)
    data = utils.get_data_as_list(filter_arg)
    output = utils.format_data_as_xlsx(data)
    return flask.send_file(
        output,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@app.route("/api/global-uk-tariff")
@decorators.cache_without_request_args(
    q=utils.DEFAULT_FILTER, p=utils.DEFAULT_PAGE, n=utils.DEFAULT_SAMPLE_SIZE
)
@decorators.compress_response
def tariff_api():
    data = utils.get_data_from_request(get_all=True)[0]
    return flask.jsonify(data)


@app.route("/tariff/metadata.json")
@decorators.cache_without_request_args()
@decorators.compress_response
def tariff_metadata():
    return flask.Response(
        flask.render_template("metadata.json"), mimetype="application/json",
    )


@app.after_request
def add_no_robots_header(response: Response):
    response.headers["X-Robots-Tag"] = "noindex, nofollow"
    return response


@app.after_request
def google_analytics(response: Response):
    kwargs = {}
    if request.accept_languages:
        kwargs["ul"] = request.accept_languages[0]

    thread_pool.submit(
        utils.send_analytics,
        path=request.path,
        host=request.host,
        remote_addr=request.remote_addr,
        user_agent=request.headers["User-Agent"],
        **kwargs,
    )
    return response
