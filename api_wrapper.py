import requests, json

class BearAPIWrapper:

    """ Wrapper for the bears REST API:
    POST      /bear - create
    GET       /bear - read all bears
    GET       /bear/:id - read specific bear
    PUT       /bear/:id - update specific bear
    DELETE    /bear - delete all bears
    DELETE    /bear/:id - delete specific bear
    """

    DEFAULT_HOST = '127.0.0.1'
    DEFAULT_PORT = 8091
    
    GET='GET'
    POST='POST'
    PUT='PUT'
    DELETE='DELETE'

    def __init__(self, host=None, port=None):
        
        self.host = self.DEFAULT_HOST if host is None else host
        self.port = self.DEFAULT_PORT if port is None else port
        
        self.base_url = f'http://{self.host}:{str(self.port)}'
        
    def __common_http_handler__(self, url_path, method=GET, data=None, parse_json=False):
        """Common method for HTTP requests to bears REST API.
        
        Parameters
        ----------
        url_path   : str, URL path to specified API resource 
        method     : str, HTTP method (default - GET), allowed values: GET, POST, PUT, DELETE
        data       : dict, bear data to pass (default - None)
        parse_json : bool, parse retrieved data as JSON (default - False)
        """
        if data is not None:
            data = json.dumps(data)
        
        if method == self.GET:
            res = requests.get(url_path)
        elif method == self.POST:
            res = requests.post(url_path,data=data)
        elif method == self.PUT:
            res = requests.put(url_path,data=data)
        elif method == self.DELETE:
            res = requests.delete(url_path)
            
        self.last_status_code = res.status_code
        
        if not res.ok:
            raise Exception(f'bad {method} request {url_path} status code: {res.status_code}')
            
        if parse_json:
            try:
                return res.json()
            except Exception:
                raise Exception(f'{method} request {url_path} result string is not a JSON: "{res.text}"')
            
        return res.text
        
    def get_info(self):
        """Retrieves info about REST API endpoints"""
        return self.__common_http_handler__(f'{self.base_url}/info')
        
    def get_all_bears(self):
        """Retrieves list of all existing bears"""
        return self.__common_http_handler__(f'{self.base_url}/bear', parse_json=True)
        
    def get_bear(self, id):
        """Retrieves the bear dict specified by id
        
        Args:
            id (int): specified bear id
            
        Returns:
            dict: id-specified bear data
        """
        return self.__common_http_handler__(f'{self.base_url}/bear/{str(id)}', parse_json=True)
        
    def create_bear(self, data):
        """Creates data-specified bear and retrieves its id
        
        Args:
            data (dict): specified bear data
            
        Returns:
            int: created bear id
        """
        return int(self.__common_http_handler__(f'{self.base_url}/bear', method=self.POST, data=data))
        
    def update_bear(self, id, data):
        """Updates id-specified bear with data
        
        Args:
            id (int): specified bear id
            data (dict): specified bear data
        """
        return self.__common_http_handler__(f'{self.base_url}/bear/{str(id)}', method=self.PUT, data=data)
        
    def delete_all_bears(self):
        """Removes all existing bears"""
        return self.__common_http_handler__(f'{self.base_url}/bear', method=self.DELETE)
        
    def delete_bear(self, id):
        """Removes id-specified bear
        
        Args:
            id (int): bear id to delete
        """
        return self.__common_http_handler__(f'{self.base_url}/bear/{str(id)}', method=self.DELETE)
