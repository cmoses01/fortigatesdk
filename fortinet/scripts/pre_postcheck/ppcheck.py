from fortinet import FortiManager

from fortinet.scripts.pre_postcheck.tmp import x, y, z
import json
from getpass import getpass
from pprint import pprint


fm = FortiManager()
fm.Username = ""
fm.Password = ""
fm.IP = "fortimgrstations.alaskaair.com"

fm.login()
route_table = fm.get_route_table(device_name="seajn-lab-fw-1", vdom='ALL_VDOMS')
with open('routes.json', 'w') as file:
    json.dump(route_table, file, indent=2 )
