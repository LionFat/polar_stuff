import requests

class BearAPIWrapper:
    
    def __init__(self, base_url='http://127.0.0.1:8091'):
        self.base_url = base_url
        
    def get(self, path = None):
        return requests.get(self.base_url + path)
        
    def post(self, path = None, data = None):
        return requests.post(self.base_url + path, data=data)
        
    def put(self, path = None, data = None):
        return requests.put(self.base_url + path, data=data)
        
    def delete(self, path = None):
        return requests.delete(self.base_url + path)
        
    