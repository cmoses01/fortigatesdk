import requests
import warnings


warnings.filterwarnings("ignore")

class FortiRequests:

    def __init__(self, logging_format='%(message)s'):
        self.Username = ''
        self.Password = ''
        self.IP = ""
        self.APIPort = 443
        self.headers = {"Content-Type": "application/json"}
    
    def _post_req(self, uri, payload=None):

        response = requests.post(f"https://{self.IP}:{self.APIPort}/{uri}", headers=self.headers,json=payload,
                                 verify=False)
        
        return response
    
    def _get_req(self, uri):

        response = requests.get(f"https://{self.IP}:{self.APIPort}/{uri}", headers=self.headers,
                                 
                                 verify=False)

        return response