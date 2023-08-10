from .awx_common import awx_get_id
from .awx_common import getawxdata

from ..common import prettyllog

import requests
import os
import json



VERIFY_SSL = os.getenv("VERIFY_SSL", "false")
if VERIFY_SSL == "false" or VERIFY_SSL == "False" or VERIFY_SSL == "FALSE" or VERIFY_SSL == "no" or VERIFY_SSL == "NO" or VERIFY_SSL == "No":
  VERIFY_SSL = False
else:
  VERIFY_SSL = True




def awx_create_executionenvironment(ee , organization, mytoken, r):
  try:
    eeid = (awx_get_id("execution_environments", ee['name'], r))
  except:
    print("Unexcpeted credential error")
  orgid = (awx_get_id("organizations", organization, r))
  headers = {"User-agent": "python-awx-client", "Content-Type": "application/json","Authorization": "Bearer {}".format(mytoken)}

  data = {
      "name": ee['name'],
      "image": ee['image'],
      "description": ee['description'],
      "pull": ee['pull'],
      "registry_credential": ee['registry_credential'],
      "organization": orgid
    }
  if ( eeid == ""):
    url = os.getenv("TOWER_HOST") + "/api/v2/execution_environments/"
    resp = requests.post(url,headers=headers, json=data, verify=VERIFY_SSL)
    response = json.loads(resp.content)
    try:
      credid=response['id']
      prettyllog("manage", "execution_environments", ee['name'], organization, resp.status_code, credid, "INFO")
    except:
      prettyllog("manage", "execution_environments", ee['name'], organization, resp.status_code, response, "ERROR")
  else:
    url = os.getenv("TOWER_HOST") + "/api/v2/execution_environments/%s/" % eeid
    resp = requests.put(url,headers=headers, json=data, verify=VERIFY_SSL)
    response = json.loads(resp.content)
    try:
      eeid=response['id']
      prettyllog("manage", "execution_environments", ee['name'], organization, resp.status_code, eeid, "INFO")
    except:
      prettyllog("manage", "execution_environments", ee['name'], organization, resp.status_code, response, "ERROR")
  getawxdata("execution_environments", mytoken, r)


