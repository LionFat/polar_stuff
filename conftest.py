import pytest
import api_wrapper

def pytest_configure(config):
    
    pytest.api_host = config.getoption('--api-host')
    
    pytest.api_port = config.getoption('--api-port')
    
def pytest_addoption(parser):
    
    parser.addoption('--api-host', action='store', default=None, help='specify the API host')
    
    parser.addoption('--api-port', action='store', default=None, help='specify the API port')
    
@pytest.fixture(scope='session')
def api():
    
    return api_wrapper.BearAPIWrapper(host=pytest.api_host, port=pytest.api_port)
    
@pytest.fixture(scope='session', autouse=True)
def bears_teardown(api):
    
    yield
    
    api.delete_all_bears()

@pytest.fixture(scope='function', autouse=True)
def cleanup_before_test(api):
    
    api.delete_all_bears()
