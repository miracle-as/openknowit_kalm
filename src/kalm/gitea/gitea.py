import requests
import json
import os
import base64
import xml.etree.ElementTree as ET


import base64

username = os.getenv("KALM_GITEA_USERNAME")
password = os.getenv("KALM_GITEA_PASSWORD")
credentials = f"{username}:{password}"
base64_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")



VERIFY_SSL = os.getenv("VERIFY_SSL", "false")
if VERIFY_SSL == "false" or VERIFY_SSL == "False" or VERIFY_SSL == "FALSE" or VERIFY_SSL == "no" or VERIFY_SSL == "NO" or VERIFY_SSL == "No":
  VERIFY_SSL = False
else:
  VERIFY_SSL = True

def list_gitea():
  print("list gitea")
  print(get_gitea_token())
  


def get_gitea_token():
  print("get gitea token")
  url = os.getenv("KALM_GITEA_URL") + "/api/v1/users/token"
  headers = {
    "Content-Type": "application/json",
    "Authorization": "Basic " + base64_credentials
    }
  data = '{"name":"kalm"}' 
  resp = requests.put(url,headers=headers, json=data, verify=VERIFY_SSL)
  print(resp.content)
  print(resp.status_code)
 
