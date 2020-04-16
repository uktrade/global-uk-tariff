import json
import os

from bs4 import BeautifulSoup
from flask.testing import FlaskClient
import pytest

from main import app
from src import utils


@pytest.fixture
def client() -> FlaskClient:
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


@pytest.fixture
def data_file(tmp_path):
    data = [
        {
            "commodity": "01012100",
            "description": "Pure-bred breeding horses",
            "cet_duty_rate": "0.00%",
            "ukgt_duty_rate": "0.00%",
            "change": "No change",
        },
        {
            "commodity": "01022130",
            "description": "Pure-bred breeding cows (excl. heifers)	",
            "cet_duty_rate": "0.00%",
            "ukgt_duty_rate": "0.00%",
            "change": "Liberalised",
        },
        {
            "commodity": "01022190",
            "description": "Pure-bred cattle for breeding (excl. heifers and cows)	",
            "cet_duty_rate": "0.00%",
            "ukgt_duty_rate": "0.00%",
            "change": "Liberalised",
        },
        {
            "commodity": "84821010",
            "description": "Ball bearings with greatest external diameter <= 30 mm	",
            "cet_duty_rate": "8.00%",
            "ukgt_duty_rate": "8.00%",
            "change": "Liberalised",
        },
    ]

    filepath = os.path.join(tmp_path, "test-data.json")
    with open(filepath, "w") as data_file:
        json.dump(data, data_file)

    return filepath


def test_home(client: FlaskClient):
    response = client.get("/")

    assert response.status_code == 200
    assert b'<a href="/tariff">global tariff</a>' in response.data


@pytest.mark.parametrize(
    "filter,length", [("", 5), ("cow", 3), ("bearing", 2), ("notreal", 1)]
)
def test_tariff_with_filter(
    filter: str, length: int, client: FlaskClient, data_file: str
):
    utils.DATA_FILEPATH = data_file
    response = client.get(f"/tariff?filter={filter}")

    assert response.status_code == 200
    soup = BeautifulSoup(response.data, "html.parser")
    rows = soup.find_all("tr")
    assert len(rows) == length


@pytest.mark.parametrize("filter", ["horses", "Horses"])
def test_tariff_filter_case_insensitive(
    filter: str, client: FlaskClient, data_file: str
):
    utils.DATA_FILEPATH = data_file
    response = client.get(f"/tariff?filter={filter}")
    soup = BeautifulSoup(response.data, "html.parser")
    rows = soup.find_all("td", string="Pure-bred breeding horses")

    assert len(rows) == 1


@pytest.mark.parametrize("sample", range(1, 5))
def test_tariff_with_sample_size(sample: int, client: FlaskClient, data_file: str):
    utils.DATA_FILEPATH = data_file
    response = client.get(f"/tariff?n={sample}")

    assert response.status_code == 200
    soup = BeautifulSoup(response.data, "html.parser")
    rows = soup.find_all("tr")
    assert len(rows) == sample + 1


@pytest.mark.parametrize(
    "filter,length", [("", 4), ("cow", 2), ("bearing", 1), ("notreal", 0)]
)
def test_tariff_api_with_filter(
    filter: str, length: int, client: FlaskClient, data_file: str
):
    utils.DATA_FILEPATH = data_file
    response = client.get(f"/api/global-uk-tariff?filter={filter}")

    assert response.status_code == 200
    data = response.json
    assert len(data) == length
    for item in data:
        assert set(item.keys()) == {
            "commodity",
            "description",
            "cet_duty_rate",
            "ukgt_duty_rate",
            "change",
        }


@pytest.mark.parametrize(
    "filter,length", [("", 6), ("cow", 4), ("bearing", 3), ("notreal", 2)]
)
def test_tariff_csv(filter: str, length: int, client: FlaskClient, data_file: str):
    """
    Test /tariff/global-uk-tariff.csv returns the correct content for a CSV

    Length is always expected number of rows + 2 due to the header row and a newline at EOL.
    """
    utils.DATA_FILEPATH = data_file
    response = client.get(f"/api/global-uk-tariff.csv?filter={filter}")

    assert response.status_code == 200
    assert response.mimetype == "text/csv"
    data = response.data.split(b"\n")
    assert len(data) == length


def test_tariff_xlsx(client: FlaskClient, data_file: str):
    utils.DATA_FILEPATH = data_file
    response = client.get(f"/api/global-uk-tariff.xlsx")

    assert response.status_code == 200
    assert (
        response.mimetype
        == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
