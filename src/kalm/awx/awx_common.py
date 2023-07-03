import os
import requests
import json

VERIFY_SSL = os.getenv("VERIFY_SSL", "false")
if VERIFY_SSL == "false" or VERIFY_SSL == "False" or VERIFY_SSL == "FALSE" or VERIFY_SSL == "no" or VERIFY_SSL == "NO" or VERIFY_SSL == "No":
  VERIFY_SSL = False
else:
  VERIFY_SSL = True


######################################
# function: Refresh AWX data
######################################
def refresh_awx_data(mytoken,r ):
  items = { 
    "ad_hoc_commands",
    "analytics,applications",
    "credential_input_sources",
    "credentials",
    "credential_types",
    "execution_environments",
    "groups",
    "hosts",
    "inventory_sources",
    "inventory_updates",
    "jobs",
    "job_templates",
    "labels",
    "metrics",
    "notifications",
    "notification_templates",
    "organizations",
    "projects",
    "project_updates",
    "roles",
    "schedules",
    "system_jobs",
    "system_job_templates",
    "teams",
    "unified_jobs",
    "unified_job_templates",
    "workflow_approvals",
    "workflow_job_nodes",
    "workflow_jobs",
    "workflow_job_template_nodes",
    "workflow_job_templates"
  }
  #items = {"organizations", "projects", "credentials", "hosts", "inventories", "credential_types", "labels" , "instance_groups", "job_templates", "execution_environments"}    
  for item in items:
    getawxdata(item, mytoken, r)





def awx_get_id(item,name, r):
  key = os.getenv("TOWER_HOST") + item +":name:" + name
  myvalue =  r.get(key)
  mydevode = ""
  try: 
    mydecode = myvalue.decode()
  except:
    mydecode = ""
  return mydecode

def getawxdata(item, mytoken, r):
  headers = {"User-agent": "python-awx-client", "Content-Type": "application/json","Authorization": "Bearer {}".format(mytoken)}
  url = os.getenv("TOWER_HOST") + "/api/v2/" + item
  intheloop = "first"
  while ( intheloop == "first" or intheloop != "out" ):
    try:
      resp = requests.get(url,headers=headers, verify=VERIFY_SSL)
    except:
      intheloop = "out"
    try:
      mydata = json.loads(resp.content)
    except:
      intheloop = "out"
    try:
      url = os.getenv("TOWER_HOST") + "/api/v2/" + (mydata['next'])
    except: 
      intheloop = "out"
    savedata = True
    try:
      myresults = mydata['results'] 
    except:
      savedata = False
    if ( savedata == True ):
      for result in mydata['results']:
        key = os.getenv("TOWER_HOST") + item +":id:" + str(result['id'])
        r.set(key, str(result), 600)
        key = os.getenv("TOWER_HOST") + item +":name:" + result['name']
        r.set(key, str(result['id']), 600 )
        key = os.getenv("TOWER_HOST") + item +":orphan:" + result['name']
        r.set(key, str(result), 600)
