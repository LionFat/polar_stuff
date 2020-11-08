First install all you need: `pip install -r requirements.txt`.

Then run tests: `pytest` (if an API server is on localhost:8091).
Or specify the API host and/or port you need using parameters: `--api-host` and `--api-port`:  
- `pytest --api-host=<your service ip>`
- `pytest --api-host=<your service ip> --api-port=<your service port>`
