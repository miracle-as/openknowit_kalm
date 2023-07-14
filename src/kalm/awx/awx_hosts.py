import os
import json
import requests
from ..common import prettyllog

from .awx_common import refresh_awx_data
from .awx_common import awx_get_id
from .awx_common import getawxdata

VERIFY_SSL = os.getenv("VERIFY_SSL", "false")
if VERIFY_SSL.lower() == "false" or VERIFY_SSL == "no":
    VERIFY_SSL = False
else:
    VERIFY_SSL = True
    


def awx_create_host(name, description, inventory, organization, mytoken, r):
  try:  
    invid = (awx_get_id("inventories", inventory, r))
  except:
    print("Unexcpetede error")
  orgid = (awx_get_id("inventories", organization,r ))
  data = {
        "name": name,
        "description": description,
        "organization": orgid,
        "inventory": invid
       }
  headers = {"User-agent": "python-awx-client", "Content-Type": "application/json","Authorization": "Bearer {}".format(mytoken)}
  url = os.getenv("TOWER_HOST") + "/api/v2/hosts/"
  resp = requests.post(url,headers=headers, json=data, verify=VERIFY_SSL)
  response = json.loads(resp.content)
  try:
    hostid=response['id']
    prettyllog("manage", "host", name, organization, resp.status_code, "Host %s created with id: %s" % (name, hostid ))
  except:
    prettyllog("manage", "host", name, organization, resp.status_code, response)
