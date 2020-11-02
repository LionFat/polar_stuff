import pytest
import api_wrapper

def pytest_configure(config):
    pytest.api_url = config.getoption('--api-url')
    
    print(pytest.api_url)
    
def pytest_addoption(parser):
    parser.addoption('--api-url', action='store', default='http://127.0.0.1:8091', help='specify the api url, default value: http://127.0.0.1:8091')
    
@pytest.fixture
def api():
    return api_wrapper.BearAPIWrapper(pytest.api_url)
    
@pytest.fixture
def delete_all_bears(api):
    return api.delete('/bear')
    