import requests
import json
import os
import base64
import xml.etree.ElementTree as ET


mytoken=os.getenv("JENKINSTOKEN")
VERIFY_SSL=os.getenv("VERIFY_SSL", False)
URL=os.getenv("JENKINS_API", "https://jenkins.openknowit.com")
username=os.getenv("JENKINS_USER")
password=os.getenv("JENKINS_PASSWORD")  
credentials = f"{username}:{password}"
credentials_base64 = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

def parse_jobs_xml(xml_string):
    root = ET.fromstring(xml_string)
    data = []
    
    for job in root.findall(".//job"):
        name = job.find("name").text
        url = job.find("url").text
        color = job.find("color").text if job.find("color") is not None else None
        data.append({"name": name, "url": url, "color": color})
    
    return data

def listjobs():   
  headers = {
    "User-agent": "python-awx-client",
    "Content-Type": "application/json",
    "Authorization": "Basic {}".format(credentials_base64)
  }  
  url = URL + '/crumbIssuer/api/json'
  resp = requests.get(url,headers=headers, verify=VERIFY_SSL)        
  jobs = parse_jobs_xml(resp.text)
  for job in jobs:
    print(job)
  return resp.status_code

def get_plugins():
  headers = { 
    "User-agent": "python-jenkins-client",
    "Content-Type": "application/json",
    "Authorization": "Basic {}".format(credentials_base64)
  }
   
  url = URL + '/pluginManager/api/json?depth=1'
  resp = requests.get(url,headers=headers, verify=VERIFY_SSL)
  plugins = resp.json()["plugins"]  
  print("-------------------------------------------------")
  print(resp.json())

  print("-------------------------------------------------")
  for plugin in plugins:
    print("%-40s, %-40s, %-40s" % (plugin["shortName"], plugin["version"], plugin["url"]))
  return resp.status_code

#  plugins = parse_xml(resp.text)
#  for plugin in plugins:
#    print(plugin)

   
