# The UK Global Tariff [![CircleCI](https://circleci.com/gh/uktrade/global-uk-tariff.svg?style=svg)](https://circleci.com/gh/uktrade/global-uk-tariff)

## Background

The UK Global Tariff Tool, also to be known by its GOV.UK service name of “Check the future UK global tariff”, is a web service for traders and other interested parties to look up how the import duty on goods will change once the Transition Period has ended and the UK sets its own tariff policy.

Goods are segmented mostly by the CN8 commodity code taxonomy with some segmented at the CN10 commodity code taxonomy where appropriate, and are displayed in a table with a human-readable code description, the current duty under the EU tariff, the new duty under the UK tariff and a label specifying the type of change. A search box can be used for searching within any of these fields. Results are spread over multiple pages where necessary. Downloads of the data in the table are available in CSV or Excel spreadsheet formats, as well as via a JSON API.

The service is aimed at importers and will be publicly accessible. It is due for release alongside the announcement of the tariff. There will be an associated GOV.UK start page that provides more background to the tariff.

## Components

The service is implemented using a JavaScript React frontend and Python backend. The backend can also replicate the frontend for those who don't have JavaScript enabled.

The repo currently holds both the compiled JavaScript and the complete data in JSON form, these are both due to a limited build and deploy process.

### Backend

The backend reads a static data file containing tariff data and provides this to a Jinja template both in a filtered format (for non-javascript users) and in it's complete form for everyone else. It also provides an API for filtering and downloading the data in JSON, CSV and XLSX formats.

### Frontend

The JavaScript frontend provides a simple data table built in React. This filters and displays the data as required. 

### External Services

The UK Global Tariff does not use ay external services such as databases to run. However it is integrated with 3 monitoring services to keep track of how the tool is used and any bugs that arise. These are Google Analytics, ELK (via an Elastic APM) and Sentry for bugs. All of these services have credentials which are provided through environmental variables. These environmental variables are detailed below.

## Data.gov.uk

The data in the service is automatically published to Data.gov.uk. There is a metadata file hosted at /metadata.json that is read by Data.gov.uk and used to populate the data catalogue entry. This file is publicly readable.

## Zendesk

There is a feedback link in the service which directs requests to ukglobaltariff@uktrade.zendesk.com.

## Quickstart

This app is tested with Python 3.8.x and Node 12.16.x

Create a Python virtualenv and install the dependencies:

```bash
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

In another terminal fetch the node dependencies and start a webpack server:

```bash
npm install
npm run watch
```

Run the app:

```bash
python main.py
```

This will make the app viewable at [http://localhost:5000]().

### Environmental Variables

No environmental variables are necessary - although it is likely some errors will be logged if they are not added. The different variables used in the app are detailed below:

| Variable Name  | Purpose                                                            |
|----------------|--------------------------------------------------------------------|
| APM_TOKEN      | Token to authenticate the Elastic APM                              |
| ENV_NAME       | Environment name, e.g. STAGING/PRODUCTION, used by the Elastic APM |
| GA_TRACKING_ID | The tracking ID for Google Analytics                               |
| SENTRY_HOST    | The Sentry host to send Error information to.                      |
| SENTRY_KEY     | The key to authenticate against the Sentry server                  |
| SENTRY_PROJECT | The Sentry project the error information relates to.               |

## Testing

Tests can be run with the following command:

```bash
python -m pytest .
```

To run them with coverage use the following command:

```bash
python -m pytest . --cov
```

## Updating Data

If the need arises to update the static JSON file from a spreadsheet, this can be done on a local machine using:

```shell script
./src/data.py <your-new-data.xlsx> data.json
```

Watch for any warnings about data errors that may be emitted.

Then update the dates in `./src/templates/metadata.json`, commit the changes, and deploy the service.
