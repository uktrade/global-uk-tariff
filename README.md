# The Global UK Tariff

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

## Testing

Tests can be run with the following command:

```bash
python -m pytest .
```

To run them with coverage use the following command:

```bash
python -m pytest . --cov
```
