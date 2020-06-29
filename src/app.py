import logging
import math
import os
from concurrent.futures.thread import ThreadPoolExecutor

from elasticapm.contrib.flask import ElasticAPM
import flask
from flask import request, Response
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from whitenoise import WhiteNoise

from src import decorators, utils


logger = logging.getLogger(__name__)

if os.getenv("SENTRY_KEY") and os.getenv("SENTRY_PROJECT") and os.getenv("SENTRY_HOST"):
    sentry_sdk.init(
        dsn=f"https://{os.getenv('SENTRY_KEY')}@{os.getenv('SENTRY_HOST')}/{os.getenv('SENTRY_PROJECT')}",
        integrations=[FlaskIntegration()],
    )


app = flask.Flask(__name__)
app.config["ELASTIC_APM"] = {
    "SERVICE_NAME": "global-uk-tariff",
    "SECRET_TOKEN": os.getenv("APM_TOKEN"),
    "SERVER_URL": "https://apm.elk.uktrade.digital",
    "ENVIRONMENT": os.getenv("ENV_NAME"),
}

app.wsgi_app = WhiteNoise(app.wsgi_app, root="static/")
apm = ElasticAPM(app)


thread_pool = ThreadPoolExecutor()


@app.route("/")
def home():
    return flask.redirect("/tariff")


@app.route("/accessibility", strict_slashes=False)
def accessibility():
    return flask.render_template("accessibility.html")


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


@app.route("/tariff/metadata.xml")
@decorators.cache_without_request_args()
@decorators.compress_response
def dcat_metadata():
    return flask.Response(
        flask.render_template("metadata.xml"), mimetype="application/rdf+xml",
    )


@app.after_request
def add_no_robots_header(response: Response):
    response.headers["X-Robots-Tag"] = "noindex, nofollow"
    return response


@app.after_request
def google_analytics(response: Response):
    try:
        kwargs = {}
        if request.accept_languages:
            try:
                kwargs["ul"] = request.accept_languages[0][0]
            except IndexError:
                pass

        if request.referrer:
            kwargs["dr"] = request.referrer

        path = request.path
        if request.query_string:
            path = path + f"?{request.query_string.decode()}"

        thread_pool.submit(
            utils.send_analytics,
            path=path,
            host=request.host,
            remote_addr=request.remote_addr,
            user_agent=request.headers["User-Agent"],
            **kwargs,
        )
    except Exception:  # We don't want to kill the response if GA fails.
        logger.exception("Google Analytics failed")
        pass
    return response
