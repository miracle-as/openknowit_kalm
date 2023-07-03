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


######################################
# function: get Project 
######################################
def awx_get_project(projid, organization=None, mytoken=None, r=None):
  headers = {"User-agent": "python-awx-client", "Content-Type": "application/json","Authorization": "Bearer {}".format(mytoken)}
  orgid = (awx_get_id("organizations", organization, r))
  url = os.getenv("TOWER_HOST") + "/api/v2/projects/%s" % projid
  resp = requests.get(url,headers=headers,  verify=VERIFY_SSL)
  return   json.loads(resp.content)



######################################
# function: Create Project 
######################################
def awx_create_project(name, description, scm_type, scm_url, scm_branch, credential, organization, mytoken, r):
  getawxdata("projects", mytoken, r)
  try:  
    projid = (awx_get_id("projects", name, r))
  except:
    print("Unexpected error")
  headers = {"User-agent": "python-awx-client", "Content-Type": "application/json","Authorization": "Bearer {}".format(mytoken)}
  orgid = (awx_get_id("organizations", organization, r))
  credid = (awx_get_id("credentials", credential, r))
  data = {
        "name": name,
        "description": description,
        "scm_type": scm_type,
        "scm_url": scm_url,
        "organization": orgid,
        "scm_branch": scm_branch,
        "credential": credid
       }
  if (projid == ""):
    url = os.getenv("TOWER_HOST") + "/api/v2/projects/"
    resp = requests.post(url,headers=headers, json=data, verify=VERIFY_SSL)
    response = json.loads(resp.content)
    try:
      projid=response['id']
      prettyllog("manage", "project", name, organization, resp.status_code, projid)
    except:
      prettyllog("manage", "project", name, organization, resp.status_code, response)
    #loop until project is synced
    loop = True
    while ( loop ):
        getawxdata("projects", mytoken, r)
        try:  
            projid = (awx_get_id("projects", name, r))
        except:
            print("Unexpected error")
        projectinfo = awx_get_project(projid, organization, mytoken , r)
        try:
          if( projectinfo['status'] == "successful"):
              loop = False
        except:
          print("Project status unknown")

  else:
    url = os.getenv("TOWER_HOST") + "/api/v2/projects/%s/" % projid
    resp = requests.put(url,headers=headers, json=data, verify=VERIFY_SSL)
    response = json.loads(resp.content)
    try:  
      projid = (awx_get_id("projects", name,r ))
      prettyllog("manage", "project", name, organization, resp.status_code, projid)
    except:
      prettyllog("manage", "project", name, organization, resp.status_code, response)
    getawxdata("projects", mytoken, r)
    try:
        projid = (awx_get_id("projects", name, r ))
    except:
        print("Unexpected error")
    projectinfo = awx_get_project(projid, organization, mytoken, r)
    if( projectinfo['status'] == "successful"):
      prettyllog("manage", "project", name, organization, "000", "Project is ready")
    else:    
      prettyllog("manage", "project", name, organization, "666", "Project is not ready")
  refresh_awx_data(mytoken, r)
