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
def create_git_project(project):
  prettyllog("state", "Init", "git", "start", "000", "create project initiated", severity="DEBUG")
  myenv = getenv()
  session = init()
  url = myenv['KALM_GIT_URL'] + "/api/v1/user/repos"
  headers = {
    "Content-Type": "application/json",
    "Authorization": "Basic " + myenv['base64_credentials']
    }
  data = {
    "name": project['name'],
    "description": project['description'],
    "private": project['private'],
    "auto_init": project['auto_init']
    }
  resp = session.post(url,headers=headers, json=data)
  if resp.status_code == 201:
    prettyllog("state", "Init", "git", "ok", resp.status_code, "create project successful", severity="INFO")
    return resp.json()
  else:
    prettyllog("state", "Init", "git", "error", resp.status_code, "create project failed", severity="ERROR")
    return None
  
  
def get_git_projects():
  myenv = getenv() 
  session = init()
  url = myenv['KALM_GIT_URL'] + "/api/v1/user/repos"
  headers = {
    "Content-Type": "application/json",
    "Authorization": "Basic " + myenv['base64_credentials']
    }
  resp = session.get(url,headers=headers)
  if resp.status_code == 200:
    prettyllog("state", "Init", "git", "ok", resp.status_code, "get projects successful", severity="INFO")
    return resp.json()
  else:
    prettyllog("state", "Init", "git", "error", resp.status_code, "get projects failed", severity="ERROR")
    return None
  

  
def create_git_token():
  session = init()
  myenv = getenv()
  url = myenv['KALM_GIT_URL'] + "/api/v1/users/" + myenv['KALM_GIT_USER'] + "/tokens?sudo=" + myenv['KALM_GIT_USER']
  headers = {
    "Content-Type": "application/json",
    "Authorization": "Basic " + myenv['base64_credentials']
    }
  data = {
    "name": myenv['KALM_GIT_USER']
    }
  resp = session.post(url,headers=headers, json=data)
  if (resp.status_code == 201):
    prettyllog("state", "Init", "git", "ok", resp.status_code, "create token successful", severity="INFO")
    return resp.json()
  else:
    prettyllog("state", "Init", "git", "error", resp.status_code, "create token failed", severity="INFO")
    return None



def refresh_git_token(git_token):
  create = True
  if (len (git_token) == 0):
    prettyllog("state", "Init", "git", "error", "000", "no tokens found", severity="INFO")
    create = Truesyst
    mytoken = create_git_token()
    pprint.pprint(mytoken)
  else:
    prettyllog("state", "Init", "git", "ok", "000", "tokens found", severity="INFO")
    mytoken = create_git_token()
    pprint.pprint(mytoken)
  if create == True:
    mytoken = create_git_token()



def delete_token():
  prettyllog("state", "Init", "git", "ok", "000", "token found", severity="INFO")
  session = init()
  myenv = getenv()
  url = myenv['KALM_GIT_URL'] + "/api/v1/users/" + myenv['KALM_GIT_USER'] + "/tokens/"
  headers = {
    "Content-Type": "application/json",
    "Authorization": "Basic " + myenv['base64_credentials']
    }
  data = {
    "username": myenv['KALM_GIT_USER']
    }
  resp = session.delete(url,headers=headers)
  if (resp.status_code == 204):
    prettyllog("state", "Init", "git", "ok", resp.status_code, "delete token successful", severity="INFO")
  else:
    prettyllog("state", "Init", "git", "error", resp.status_code, "delete token failed", severity="INFO")
  return None


def get_git_tokens():

  session = init()
  myenv = getenv()
  url = myenv['KALM_GIT_URL'] + "/api/v1/users/" + myenv['KALM_GIT_USER'] + "/tokens?sudo=" + myenv['KALM_GIT_USER']
  headers = {
    "Content-Type": "application/json",
    "Authorization": "Basic " + myenv['base64_credentials']
    }
  data = {
    "username": myenv['KALM_GIT_USER']
    }
  resp = session.get(url,headers=headers, json=data)
  if (resp.status_code == 200):
    prettyllog("state", "Init", "git", "ok", resp.status_code, "get token successful", severity="INFO")
    return resp.json()
  else:
    prettyllog("state", "Init", "git", "error", resp.status_code, "get token failed", severity="INFO")
    return None
  


 
