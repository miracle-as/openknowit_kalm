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



######################################
# function: create Credential
######################################
def awx_create_credential( credential , organization, mytoken, r):
  try:
    credid = (awx_get_id("credentials", credential['name'], r))
  except:
    print("Unexcpeted credential error")
  orgid = (awx_get_id("organizations", organization, r))
  headers = {"User-agent": "python-awx-client", "Content-Type": "application/json","Authorization": "Bearer {}".format(mytoken)}
  credentialtypeid = (awx_get_id("credential_types", credential['type'], r))

  ######################################
# type: vault
######################################
  if( credential['kind'] == "vault"):
    data = {
      "name": credential['name'],
      "description": credential['description'],
      "credential_type": credentialtypeid,
      "organization": orgid,
      "inputs":
        {
           "vault_id": "",
           "vault_password": credential['vault_password']
        },
      "kind": credential['kind']
    }

######################################
# type: hashicorp vault
######################################
  if( credential['kind'] == "hashivault_kv"):
    myurl = os.getenv(key="VAULT_URL")
    mytoken = os.getenv(key="VAULT_TOKEN")
    data = {
      "name": credential['name'],
      "description": credential['description'],
      "credential_type": credentialtypeid,
      "organization": orgid,
      "inputs":
        {
           "url": credential['url'],
           "token": credential['token']
        },
      "kind": credential['kind']
    }


######################################
# type: GIT source control
######################################
  if( credential['kind'] == "scm"):
    data = {
        "name": credential['name'],
        "description": credential['description'],
        "credential_type": credentialtypeid,
        "organization": orgid,
        "inputs":
          {
            "ssh_key_data": credential['ssh_key_data'],
            "username": credential['username'],
            "password": credential['password']
          },
        "kind": credential['kind']
        }

######################################
# type: machine 
######################################
  if( credential['kind'] == "ssh" ):
    try:
      credential_name = credential['name']
    except:
      credential_name = "credential"
    try:
      credential_description = credential['description']
    except:
      credential_description = ""
    try:
      credential_username = credential['username']
    except:
      credential_username = ""
    try:
      credential_password = credential['password']
    except:
      credential_password = ""
    try:
      credential_ssh_key_data = credential['ssh_key_data']
    except:
      credential_ssh_key_data = ""
    try:
      credential_privilege_escalation_method = credential['privilege_escalation_method']
    except:
      credential_privilege_escalation_method = ""
    try:
      credential_privilege_escalation_username = credential['privilege_escalation_username']
    except:
      credential_privilege_escalation_username = ""
    try:
      credential_privilege_escalation_password = credential['privilege_escalation_password']
    except:
      credential_privilege_escalation_password = ""
      
    data = {
        "name": credential_name,
        "description": credential_description,
        "credential_type": credentialtypeid,
        "organization": orgid,
        "inputs":
          {
            "ssh_key_data": credential_ssh_key_data, 
            "username": credential_username,
            "password": credential_password,
            "become_method": credential_privilege_escalation_method,
            "become_username": credential_privilege_escalation_username,
            "become_password": credential_privilege_escalation_password
          },
        "kind": credential['kind']
        }

  if ( credid == ""):
    url = os.getenv("TOWER_HOST") + "/api/v2/credentials/"
    resp = requests.post(url,headers=headers, json=data, verify=VERIFY_SSL)
    response = json.loads(resp.content)
    try:
      credid=response['id']
      prettyllog("manage", "credential", credential['name'], organization, resp.status_code, credid)
    except:
      prettyllog("manage", "credential", credential['name'], organization, resp.status_code, response)
  else:
    url = os.getenv("TOWER_HOST") + "/api/v2/credentials/%s/" % credid
    resp = requests.put(url,headers=headers, json=data, verify=VERIFY_SSL)
    response = json.loads(resp.content)
    try:
      credid=response['id']
      prettyllog("manage", "credential", credential['name'], organization, resp.status_code, credid)
    except:
      prettyllog("manage", "credential", credential['name'], organization, resp.status_code, response)
  getawxdata("credentials", mytoken, r)