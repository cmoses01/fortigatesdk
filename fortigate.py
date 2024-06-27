from fortigate_requests import FortigateRequests
from urllib.parse import quote
import requests

class FortigateAPI(FortigateRequests):
    
    def __init__(self):
        super().__init__()
    
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

        uri = '/api/v2/cmdb/firewall/address'

        resp = self._get_req(uri)


        return resp.json()['results']

if __name__ == "__main__":
    from getpass import getpass
    fw = FortigateAPI()
    fw.Username = ""
    fw.Password = getpass()
    fw.IP = ""

    login = fw.login()

    resp = fw.get_addresses()





