from fortinet.forti_requests import FortiRequests
from urllib.parse import quote
import requests

class Fortigate(FortiRequests):
    
    def __init__(self, vdom="root"):
        super().__init__()
        self.vdom = vdom
    
    def login(self):

        uri = f'/logincheck?username={self.Username}&secretkey={quote(self.Password)}'

        resp = self._post_req(uri)

        
        #print(resp.cookies)
        # for cookie in resp.cookies:

        #     if cookie.name == "ccsrftoken":
                
        #         self.headers['X-CSRFTOKEN'] = cookie.value.strip('"')

        #         break

        cookies_dict = requests.utils.dict_from_cookiejar(resp.cookies)
        cookies_header = '; '.join([f"{key}={value}" for key, value in cookies_dict.items()])
        self.headers['Cookie'] = cookies_header
        return resp
    
    def get_addresses(self):

        uri = f'/api/v2/cmdb/firewall/address'
        if self.vdom != "root":
            uri += f'?vdom={self.vdom}'
        
        resp = self._get_req(uri)

        return resp.json()['results']
    
    def get_routing_table(self):

        uri = f'/api/v2/monitor/router/ipv4'

        if self.vdom != "root":
            uri += f'?vdom={self.vdom}'

        resp = self._get_req(uri)

        return resp.json()['results']
    
    def get_ha_status(self):

        return True
        







