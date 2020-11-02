first install all you need: `pip install -r requirements.txt`

then run tests: `pytest -sv --tb=short` (if API server on localhost) or `pytest -sv --api-url=http://<your server ip>:8091 --tb=short` (if server on other machine)
