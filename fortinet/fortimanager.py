from urllib.parse import quote
import requests

from fortinet.forti_requests import FortiRequests

class FortiManager(FortiRequests):

    jsonrpc_uri = '/jsonrpc'
    proxy_uri   = '/sys/proxy/json'
    

    def __init__(self):
        super().__init__()
        self.token = None
        
        
    def jsonrpc_call(self, uri, method, data=None):
        '''
        since all api calls are post request to /jsonrpc endpoint call, this is the wrapper for the post request
        '''

        payload = {
            "method": method,
            "params":  [{"data": data,
                        "url": uri}]
            }
        if self.token:
            payload['session'] = self.token
        
        return super()._post_req(uri=self.jsonrpc_uri, payload=payload)
    
    # METHODS TO USE AGAINST FORTIMANAGER
    
    def login(self):

        uri = "/sys/login/user"

        data = {                
                "user": self.Username,
                "passwd": self.Password
                }

        resp = self.jsonrpc_call(data=data, method='exec', uri=uri)

        if resp.ok:
            self.token = resp.json()['session']
        else:
            resp.raise_for_status()
        return resp.json()

    def get_route_table(self, device_name, vdom):


        if vdom == "ALL_VDOMS":
            all_vdom_routes = []
            vdoms = self.get_vdoms(device_name=device_name)
            for vdom in vdoms:
                routes = self.get_route_table(device_name=device_name, vdom=vdom)
                all_vdom_routes.append({"vdom": vdom, "route_table": routes})
            return all_vdom_routes
        
        
       
        
        fortigate_uri = f'/api/v2/monitor/router/ipv4?vdom={vdom}'
        
        data = {
                
                'action': 'get',
                'target': [f'device/{device_name}'],
                'resource': fortigate_uri,
            }
        
        resp = self.jsonrpc_call(data=data, method='exec', uri=self.proxy_uri)
        
        return resp.json()['result'][0]['data'][0]['response']['results']
        
    def get_vdoms(self, device_name):

        fortigate_uri = '/api/v2/cmdb/system/vdom'

        data = {
                
                'action': 'get',
                'target': [f'device/{device_name}'],
                'resource': fortigate_uri,
            }
        
        resp = self.jsonrpc_call(data=data, method='exec', uri=self.proxy_uri)
        
        return [vdom['name'] for vdom in resp.json()['result'][0]['data'][0]['response']['results']]
    
    def get_ha_status(self, device_name, serial=None):

        # fortigate_uri = '/api/v2/monitor/system/ha-peer'

        # if isinstance(serial, str):
        #     fortigate_uri += f'?serial_no={serial}'

        
       
        pass
        # resp = self.jsonrpc_call(data=data, uri=self.proxy_uri)

        # return resp.json()['result'][0]['data'][0]['response']['results']
    
if '__main__' == __name__:
    from pprint import pprint
    import json
    fm = FortiManager()
    fm.Username = ""
    fm.Password = ""
    fm.IP = "fortimgrstations.alaskaair.com"

    fm.login()
    resp = fm.get_ha_status(device_name='seajn-lab-fw-1', serial='FGT80FTK21042005')
    pprint(resp)
