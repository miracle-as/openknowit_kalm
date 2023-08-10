import os
from ..common import prettyllog
from .awx_common import awx_get_id
from .awx_common import getawxdata
import json
import requests


VERIFY_SSL = os.getenv("VERIFY_SSL", "false")
if VERIFY_SSL.lower() == "false" or VERIFY_SSL == "no":
    VERIFY_SSL = False
else:
    VERIFY_SSL = True

############################################################################################################################
# Create organization
############################################################################################################################



def awx_create_organization(name, description, max_hosts, DEE, realm, mytoken, r):
  prettyllog("manage", "organization", name, "update", "000", "Start")
  try:  
    orgid = (awx_get_id("organizations", name,r ))
  except:
    print("Unexcpetede error")

  if (orgid == ""):
    headers = {"User-agent": "python-awx-client", "Content-Type": "application/json","Authorization": "Bearer {}".format(mytoken)}
    data = {
          "name": name,
          "description": description,
          "max_hosts": max_hosts
         }
    url = os.getenv("TOWER_HOST") + "/api/v2/organizations/"
    resp = requests.post(url,headers=headers, json=data, verify=VERIFY_SSL)
    response = json.loads(resp.content)
    try:
      orgid=response['id']
      prettyllog("manage", "organization", name, "exist", resp.status_code, "organization %s created with id %s" % (orgid))
    except:
      prettyllog("manage", "organization", name, "new", resp.status_code, "organization not created")
      print(response)
  else:    
    prettyllog("manage", "organization", name, "exist", "000", "organization already exist")
    headers = {"User-agent": "python-awx-client", "Content-Type": "application/json","Authorization": "Bearer {}".format(mytoken)}
    data = {
          "name": name,
          "description": description,
          "max_hosts": max_hosts
         }
    url = os.getenv("TOWER_HOST") + "/api/v2/organizations/%s" % orgid
    resp = requests.put(url,headers=headers, json=data, verify=VERIFY_SSL)
    response = json.loads(resp.content)
    prettyllog("manage", "organization", name, "update", resp.status_code, response)
  getawxdata("organizations", mytoken, r)
  prettyllog("manage", "organization", name, "end of organization", "000", "End")
