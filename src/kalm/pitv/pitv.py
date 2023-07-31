import requests
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


pitvurl = os.getenv("pitv_URL", "https://pitvapi.openknowit.com")  

def status():
  print(pitvurl)

def service():
  print("service")
  
