import requests
import json
import os
import base64
import xml.etree.ElementTree as ET
import pprint
from ..common import prettyllog


import base64


def getenv():
  myenv = {}
  myenv["KALM_GIT_URL"] = os.getenv("KALM_GIT_URL")
  myenv["KALM_GIT_USER"] = os.getenv("KALM_GIT_USER")
  myenv["KALM_GIT_PASSWORD"] = os.getenv("KALM_GIT_PASSWORD")
  myenv["KALM_GIT_TYPE"] = os.getenv("KALM_GIT_TYPE")
  username = os.getenv("KALM_GIT_USER")
  password = os.getenv("KALM_GIT_PASSWORD")
  myenv["verifyssl"] = os.getenv("KALM_GIT_VERIFY_SSL", "False")

  credentials = f"{username}:{password}"
  base64_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
  myenv["base64_credentials"] = base64_credentials
  return myenv

def init():
  prettyllog("state", "Init", "git", "start", "000", "login initiated", severity="DEBUG")
  myenv = getenv()
  session = requests.Session()
  url = os.getenv("KALM_GIT_URL") + "/api/v1/user"
  headers = {
    "Content-Type": "application/json",
    "Authorization": "Basic " + myenv['base64_credentials']
    }
  resp = session.get(url,headers=headers)
  if resp.status_code == 200:
    prettyllog("state", "Init", "git", "ok", resp.status_code, "login successful", severity="INFO")
    return session
  else:
    prettyllog("state", "Init", "git", "error", resp.status_code, "login failed", severity="ERROR")
    return None




def get_git_token():
  session = init()
  myenv = getenv()
  url = myenv['KALM_GIT_URL'] + "/api/v1/users/" + myenv['KALM_GIT_USER'] + "/tokens"
  headers = {
    "Content-Type": "application/json"
    }
  data = {
    "username": "knowit"
    }
  resp = session.get(url,headers=headers, json=data)
  pprint.pprint(resp.status_code)
  pprint.pprint(url)



 
