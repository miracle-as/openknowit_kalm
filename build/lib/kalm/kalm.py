import redis
from pprint import pprint
import json
import requests
import hvac
import os
import sys
import datetime
import pynetbox
import urllib3
import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

VERIFY_SSL = os.getenv("VERIFY_SSL", "false")
if VERIFY_SSL == "false" or VERIFY_SSL == "False" or VERIFY_SSL == "FALSE" or VERIFY_SSL == "no" or VERIFY_SSL == "NO" or VERIFY_SSL == "No":
  VERIFY_SSL = False
else:
  VERIFY_SSL = True


def prettyllog(function, action, item, organization, statuscode, text):
  d_date = datetime.datetime.now()
  reg_format_date = d_date.strftime("%Y-%m-%d %I:%M:%S %p")
  print("%-20s: %-12s %20s %-50s %-20s %-4s %-50s " %( reg_format_date, function,action,item,organization,statuscode, text))

  


#def prettyllog(function, action, item, organization, statuscode, text):
 # d_date = datetime.datetime.now()
 # reg_format_date = d_date.strftime("%Y-%m-%d %I:%M:%S %p")
 # print("%-20s: %-12s %20s %-50s %-20s %-4s %-50s " %( reg_format_date, function,action,item,organization,statuscode, text))

class Hvac:
  def __init__(self):
    self.url = self._get_url()
    self.token = self._get_token()
    self.client = hvac.Client(url=self.url, token=self.token)

  @staticmethod
  def _get_url():
    return os.getenv(key="VAULT_URL")

  @staticmethod
  def _get_token():
    return os.getenv(key="VAULT_TOKEN")

  # Method to create a new KV pair
  def create_kv_engine(self, engine_name):
    self.client.sys.enable_secrets_engine(
      backend_type="kv",
      path=engine_name,
      options={"version": "2"}
    )

  # Method to create a password 
  def create_password(self, engine_name, username, password):
    self.client.secrets.kv.v2.create_or_update_secret(
      mount_point=engine_name,
      path=username,
      secret={"username": username, "password": password}
    )

  # Method to read an existing password 
  def read_password(self, engine_name, username):
    return self.client.secrets.kv.v2.read_secret_version(
      mount_point=engine_name,
      path=username
    )
  # Method to read an existing token
  def read_secret(self, engine_name, secret):
    return self.client.secrets.kv.v2.read_secret_version(
      mount_point=engine_name,
      path=secret
    )

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

def vault_get_secret(path, vault):
  secret = vault.read_secret(engine_name="secret", secret=path)['data']['data']
  return secret


def awx_get_id(item,name, r):
  key = os.getenv("TOWER_HOST") + item +":name:" + name
  myvalue =  r.get(key)
  mydevode = ""
  try: 
    mydecode = myvalue.decode()
  except:
    mydecode = ""
  return mydecode

  

def awx_delete(item, name, mytoken, r):
  headers = {"User-agent": "python-awx-client", "Content-Type": "application/json","Authorization": "Bearer {}".format(mytoken)}
  itemid = (awx_get_id(item, name, r))
  url = os.getenv("TOWER_HOST") + "/api/v2/" + item + "/" + itemid
  resp = requests.delete(url,headers=headers, verify=VERIFY_SSL)

def awx_purge_orphans():
  orphans = r.keys("*:orphan:*")
  for orphan in orphans:
    mykey = orphan.decode().split(":")
    awx_delete(mykey[1],mykey[3])

def awx_create_label(name, organization, mytoken, r):
  orgid = (awx_get_id("organizations", organization, r))
  if ( orgid != "" ):
    data = {
       "name": name,
       "organization": orgid
       }
    headers = {"User-agent": "python-awx-client", "Content-Type": "application/json","Authorization": "Bearer {}".format(mytoken)}
    url = os.getenv("TOWER_HOST") + "/api/v2/labels"
    resp = requests.post(url,headers=headers, json=data, verify=VERIFY_SSL)
      


def awx_create_inventory(name, description, organization, inventorytype, variables, mytoken, r):
  try:  
    invid = (awx_get_id("inventories", name, r))
  except:
    print("Unexpeted inventory error")
  if (invid == ""):
    orgid = (awx_get_id("organizations", organization, r))
    data = {
          "name": name,
          "description": description,
          "inventorytype": inventorytype,
          "organization": orgid
         }
    headers = {"User-agent": "python-awx-client", "Content-Type": "application/json","Authorization": "Bearer {}".format(mytoken)}
    url = os.getenv("TOWER_HOST") + "/api/v2/inventories/"
    resp = requests.post(url,headers=headers, json=data, verify=VERIFY_SSL)
    response = json.loads(resp.content)
    prettyllog("manage", "inventories", name, organization, resp.status_code, response)
    loop = True
    while ( loop ):
        print("looop")
        getawxdata("inventories", mytoken, r)
        try:
            invid = (awx_get_id("inventories", name, r))
        except:
            print("Unexpected error")
        if (invid != "" ):
          loop = False
  headers = {"User-agent": "python-awx-client", "Content-Type": "application/json","Authorization": "Bearer {}".format(mytoken)}
  u
  resp = requests.put(url,headers=headers, json=variables, verify=VERIFY_SSL)
  response = json.loads(resp.content)
  if (inventorytype == "netbox"):
    print("Create hosts in netbox")
    nbtoken = os.getenv("NBTOKEN")
    nburl = os.getenv("NBURL")
    nb = pynetbox.api(nburl, token=nbtoken)
    ipaddresses = nb.ipam.ip_addresses.all()
    vms = nb.virtualization.virtual_machines.all()
    for vm in vms:
      pri_ip = str(vm.primary_ip).split('/')[0]
      awx_create_host(pri_ip, str(vm.name), name,organization, mytoken, r)

  prettyllog("manage", "inventories", name, organization, resp.status_code, response)


def awx_create_host(name, description, inventory, organization, mytoken, r):
  try:  
    invid = (awx_get_id("inventories", inventory, r))
  except:
    print("Unexcpetede error")
  orgid = (awx_get_id("inventories", organization,r ))
  data = {
        "name": name,
        "description": description,
        "organization": orgid,
        "inventory": invid
       }
  headers = {"User-agent": "python-awx-client", "Content-Type": "application/json","Authorization": "Bearer {}".format(mytoken)}
  url = os.getenv("TOWER_HOST") + "/api/v2/hosts/"
  resp = requests.post(url,headers=headers, json=data, verify=VERIFY_SSL)
  response = json.loads(resp.content)
  try:
    hostid=response['id']
    prettyllog("manage", "host", name, organization, resp.status_code, "Host %s created with id: %s" % (name, hostid ))
  except:
    prettyllog("manage", "host", name, organization, resp.status_code, response)



def readthefile(filename):
  f = open(filename)
  fileval = f.read()
  f.close
  return fileval


############################################################################################################################
# update ansible vault
############################################################################################################################
def awx_update_vault(ansiblevault, organization, mytoken, r):
  for vault in ansiblevault[organization]['vault']:
    credential = { 
      "name": vault['name'], 
      "description": vault['description'], 
      "type": "Vault", 
      "vault_id": vault['vault_id'], 
      "vault_password": vault['vault_password'], 
      "kind": "vault" }
    awx_create_credential(credential, organization, mytoken, r)

  for ssh in ansiblevault[organization]['ssh']:
    sshkeyval = readthefile(ssh['ssh_private_key'])
    credential = { 
      "name": ssh['name'], 
      "username": ssh['username'], 
      "password": ssh['password'],
      "description": ssh['description'], 
      "type": "Machine", 
      "ssh_key_data": sshkeyval,
      "privilege_escalation_method": ssh['privilege_escalation_method'],
      "privilege_escalation_username": ssh['privilege_escalation_username'],
      "privilege_escalation_password": ssh['privilege_escalation_password'],
      "kind": "ssh" 
      }
    awx_create_credential(credential, organization, mytoken, r)

  for scm in ansiblevault[organization]['scm']:
    f = open(ssh['ssh_private_key'])
    sshkeyval = f.read()
    f.close
    credential = { 
      "name": scm['name'], 
      "username": scm['username'], 
      "password": scm['password'], 
      "description": scm['description'], 
      "type": "Source Control", 
      "ssh_key_data": sshkeyval,
      "kind": "scm" 
      }
    awx_create_credential(credential, organization, mytoken, r)



############################################################################################################################
# Create organization
############################################################################################################################

def awx_create_organization(name, description, max_hosts, DEE, realm, mytoken, r):
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
      prettyllog("manage", "organization", name, realm, resp.status_code, "organization %s created with id %s" % (orgid))
    except:
      prettyllog("manage", "organization", name, realm, resp.status_code, response)
  else:    
    headers = {"User-agent": "python-awx-client", "Content-Type": "application/json","Authorization": "Bearer {}".format(mytoken)}
    data = {
          "name": name,
          "description": description,
          "max_hosts": max_hosts
         }
    url = os.getenv("TOWER_HOST") + "/api/v2/organizations/%s" % orgid
    resp = requests.put(url,headers=headers, json=data, verify=VERIFY_SSL)
    response = json.loads(resp.content)
    prettyllog("manage", "organization", name, realm, resp.status_code, response)
  getawxdata("organizations", mytoken, r)


############################################################################################################################
# Create job schedule
############################################################################################################################
def awx_create_schedule(name, unified_job_template,  description, tz, start, run_frequency, run_every, end, scheduletype, organization, mytoken, r):
  headers = {"User-agent": "python-awx-client", "Content-Type": "application/json","Authorization": "Bearer {}".format(mytoken)}
  # The scheduling is tricky and must be refined
  if ( scheduletype == "Normal"):
     data = {
      "name": name,
      "unified_job_template": unified_job_template,
      "description": description,
      "local_time_zone": tz,
      "dtstart": start['year'] + "-" + start['month'] + "-" + start['day'] + "T" + start['hour'] + ":" + start['minute'] + ":" + start['second']  + "Z",
      "rrule": "DTSTART;TZID=" + tz + ":" + start['year'] + start['month'] + start['day'] + "T" + start['hour'] + start['minute'] + start['second'] +" RRULE:INTERVAL=" + run_frequency + ";FREQ=" + run_every
    }
  url = os.getenv("TOWER_HOST") + "/api/v2/schedules/"
  resp = requests.post(url,headers=headers, json=data, verify=VERIFY_SSL)
  response = json.loads(resp.content)
  try:
    schedid=response['id']
    prettyllog("manage", "schedule", name, organization, resp.status_code, schedid)
  except:
    prettyllog("manage", "schedule", name, organization, resp.status_code, response)

############################################################################################################################
# Create job template
############################################################################################################################
def awx_create_template(name, description, job_type, inventory,project,ee, credential, playbook, organization, mytoken, r):
  orgid = (awx_get_id("organizations", organization,r))
  invid = (awx_get_id("inventories", inventory,r ))
  projid = (awx_get_id("projects", project,r ))
  credid = (awx_get_id("credentials", credential, r))
  eeid = (awx_get_id("execution_environments", ee, r))

  data = {
    "name": name,
    "description": description,
    "job_type": "run",
    "inventory": invid,
    "project": projid,
    "playbook": playbook,
    "scm_branch": "",
    "credential": credid,
    "forks": 0,
    "limit": "",
    "verbosity": 0,
    "extra_vars": "",
    "job_tags": "",
    "force_handlers": "false",
    "skip_tags": "",
    "start_at_task": "",
    "timeout": 0,
    "use_fact_cache": "false",
    "execution_environment": eeid,
    "host_config_key": "",
    "ask_scm_branch_on_launch": "false",
    "ask_diff_mode_on_launch": "false",
    "ask_variables_on_launch": "false",
    "ask_limit_on_launch": "false",
    "ask_tags_on_launch": "false",
    "ask_skip_tags_on_launch": "false",
    "ask_job_type_on_launch": "false",
    "ask_verbosity_on_launch": "false",
    "ask_inventory_on_launch": "false",
    "ask_credential_on_launch": "false",
    "survey_enabled": "false",
    "become_enabled": "false",
    "diff_mode": "false",
    "allow_simultaneous": "false",
    "job_slice_count": 1
}
  headers = {"User-agent": "python-awx-client", "Content-Type": "application/json","Authorization": "Bearer {}".format(mytoken)}
  url = os.getenv("TOWER_HOST") + "/api/v2/job_templates/"
  resp = requests.post(url,headers=headers, json=data, verify=VERIFY_SSL)
  response = json.loads(resp.content)
  getawxdata("job_templates", mytoken, r)
  tmplid = awx_get_id("job_templates", name, r )
  if ( tmplid != "" ):
    url = os.getenv("TOWER_HOST") + "/api/v2/job_templates/%s/" % tmplid
    resp = requests.put(url,headers=headers, json=data, verify=VERIFY_SSL)
    response = json.loads(resp.content)
    try:
      tmplid=response['id']
      prettyllog("update", "template", name, organization, resp.status_code, tmplid)
    except:
      prettyllog("update", "template", name, organization, resp.status_code, response)
  getawxdata("job_templates", mytoken, r)
  tmplid = awx_get_id("job_templates", name ,r )
  getawxdata("credentials", mytoken, r)
  credid = (awx_get_id("credentials", credential, r))
  print('associatecommand = "awx job_template associate %s --credential %s >/dev/null 2>/dev/null " % ( tmplid, credid)')
  print("We should not use any awx cli commands, but the API is not consisten and sometimes fails to set the credentials")
  if VERIFY_SSL == False:
    associatecommand = "/usr/local/bin/awx job_template associate %s --credential %s -k >/dev/null 2>/dev/null " % ( tmplid, credid)  
  else:
    associatecommand = "/usr/local/bin/awx job_template associate %s --credential %s >/dev/null 2>/dev/null " % ( tmplid, credid)
    
  print(associatecommand)
  os.system(associatecommand)
  ############################################################################### end of create job template ##########################################


######################################
# function:  Create Team
######################################
def awx_create_team(name, description, organization , mytoken, r):
  prettyllog("manage", "team", name, organization, "000", "-")

######################################
# function: create user
######################################
def awx_create_user(name, description, organization, mytoken, r):
  prettyllog("manage", "user", name, organization, "000", "-")

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
    data = {
        "name": credential['name'],
        "description": credential['description'],
        "credential_type": credentialtypeid,
        "organization": orgid,
        "inputs":
          {
            "ssh_key_data": credential['ssh_key_data'], 
            "username": credential['username'],
            "password": credential['password'],
            "become_method": credential['privilege_escalation_method'],
            "become_username": credential['privilege_escalation_username'],
            "become_password": credential['privilege_escalation_password']
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


######################################
# function: get  organization
######################################
def awx_get_organization(orgid, mytoken, r):
  headers = {"User-agent": "python-awx-client", "Content-Type": "application/json","Authorization": "Bearer {}".format(mytoken)}
  url = os.getenv("TOWER_HOST") + "/api/v2/organizations/%s" % orgid
  resp = requests.get(url,headers=headers, verify=VERIFY_SSL)
  return   json.loads(resp.content)

######################################
# function: get Project 
######################################
def awx_get_project(projid, organization, mytoken, r):
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
        projectinfo = awx_get_project(projid, organization)
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

######################################
# function: Refresh AWX data
######################################
def refresh_awx_data(mytoken,r ):
  items = {"organizations", "projects", "credentials", "hosts", "inventories", "credential_types", "labels" , "instance_groups", "job_templates"}    
  for item in items:
    getawxdata(item, mytoken, r)


########################################################################################################################
# Main:  start
########################################################################################################################

def kalm(mytoken, r):

  ########################################################################################################################
  # Load and set ansible secrets in ansible vault
  ########################################################################################################################
  prettyllog("init", "runtime", "config", "init", "001", "loadning secrets")
  ansiblevaultfile = "/etc/kalm/secret.json"
  f = open(ansiblevaultfile)
  ansiblevault = json.loads(f.read())
  f.close


  ########################################################################################################################
  # Load  and set ansible automation org
  ########################################################################################################################
  cfgfile = "/etc/kalm/kalm.json"
  realm = "standalone"
  if (len(sys.argv) == 1):
    prettyllog("init", "runtime", "config", "master", "001", "Running standalone : using local master config")
    realm = "standalone"
  else:
      if (sys.argv[1] == "master" ):
          cfgfile = "/etc/kalm.json"
          realm="master"
          prettyllog("init", "runtime", "config", "master", "002",  "Running Running as daemon")
      if (sys.argv[1] == "custom" ):
          prettyllog("init", "runtime", "config", sys.argv[2], "003" , "running cusom config file")
          cfgfile = "/etc/kalm.d/%s" % sys.argv[2]

  f = open(cfgfile)
  config = json.loads(f.read())
  f.close

  prettyllog("init", "runtime", "config", "master", "001", "refreshing awx data")
  refresh_awx_data(mytoken, r)

  ########################################################################################################################
  # organizations
  ########################################################################################################################
  for org in (config['organization']):
    prettyllog("loop","org", "config", org['name'], "000", "create organization")
    orgname = org['name']
    key = os.getenv("TOWER_HOST") + ":organizations:name:" + orgname
    r.delete(key)
    max_hosts = org['meta']['max_hosts']
    default_environment = org['meta']['default_environment']
    description = org['meta']['description']
    awx_create_organization(orgname, description, max_hosts, default_environment, realm, mytoken, r)
    getawxdata("organizations", mytoken, r)
    orgid = awx_get_id("organizations", orgname, r)
    loop = True
    while ( loop ):
      orgdata = awx_get_organization(orgid, mytoken, r)
      if ( orgdata['name'] == orgname ):
        loop = False
    awx_update_vault(ansiblevault, orgname, mytoken, r)
    refresh_awx_data(mytoken, r)


    ######################################
    # Credentials   
    ######################################
    #try:
     # credentials = org['credentials']
     # for credential in credentials:
      #  key = os.getenv("TOWER_HOST") +":credentials:orphan:" + credential['name']
    #   r.delete(key)
      #awx_create_credential( credential, orgname)
      #loop = True
      #while (loop):
      #  credid = awx_get_id("credentials", credential['name'])
      #  if ( credid != "" ):
      #    loop = False
 # except:
 #   prettyllog("config", "initialize", "credentials", orgname, "000",  "No credentioals found")

    ######################################
    # Projects
    ######################################
    try:
      projects = org['projects']
      for project in projects:
        projectname = project['name']
        projectdesc = project['description']
        projecttype = project['scm_type']
        projecturl  = project['scm_url']
        projectbrnc = project['scm_branch']
        projectcred = project['credential']
        key = os.getenv("TOWER_HOST") +":projects:orphan:" + projectname
        r.delete(key)
        awx_create_project(projectname, projectdesc, projecttype, projecturl, projectbrnc, projectcred, orgname, mytoken, r)
        awx_get_id("projects", projectname, r)
        projid = (awx_get_id("projects", projectname, r))
    except:
      prettyllog("config", "initialize", "projects", orgname, "000",  "No projects found")

  ######################################
  # inventories
  ######################################
    try: 
      inventories = org['inventories']
    except:
      prettyllog("config", "initialize", "inventories", orgname, "000",  "No inventories found")

    for inventory in inventories:
      valid=True
      print(inventory)
      try:
        inventoryname = inventory['name']
      except:
        inventoryname = "Missing"
        valid = False
      try: 
        inventorydesc = inventory['description']
      except:
        inventorydesc = ""
      try: 
        inventorytype = inventory['type']
      except:
        inventorytype = "static"
      try:
        inventoryvariables = inventory['variables']
      except:
        inventoryvariables = {}
      print(inventoryvariables)
      if valid:
        awx_create_inventory(inventoryname, inventorydesc, orgname, inventorytype, inventoryvariables, mytoken, r)
      else:
        prettyllog("config", "initialize", "inventories", inventory, "000",  "Inventory is invalid")



  ######################################
  # hosts
  ######################################
    try:
      hosts = org['hosts']
      for host in hosts:
        hostname = host['name']
        hostdesc = host['description']
        hostinventories = host['inventories']
        for hostinventory in hostinventories: 
          awx_create_host(hostname, hostdesc, hostinventory, orgname, mytoken, r)
    except:
      prettyllog("config", "initialize", "hosts", orgname, "000",  "No hosts found")

    ######################################
    # users
    ######################################
    try:
      users = org['users']
    except:
      prettyllog("config", "initialize", "users", orgname, "000",  "No users found")

    ######################################
    # label
    ######################################
    try:
      labels = org['labels']
      for label in labels:
        labelname = label['name']
        awx_create_label(labelname, orgname, mytoken, r)
    except:
      prettyllog("config", "initialize", "labels", orgname, "000",  "No labels found")

    ######################################
    # Templates
    ######################################
    print("Templates")
    print("============================DEBUG==============================YY")
    try:
      templates = org['templates']
      for template in templates:
        templatename = template['name']
        templatedescription = template['description']
        templatejob_type = template['job_type']
        templateinventory =  template['inventory']
        templateproject = template['project']
        templateEE = template['EE']
        templatecredential = template['credentials']  
        templateplaybook = template['playbook']
        awx_create_template(templatename, templatedescription, templatejob_type, templateinventory, templateproject, templateEE, templatecredential, templateplaybook, orgname, mytoken, r)
    except:
      prettyllog("config", "initialize", "templates", orgname, "000",  "No templates found")
    print("============================DEBUG==============================YY")

    ######################################
    # Schedules
    ######################################
    try:
      schedules = org['schedules']
      for schedule in schedules:
        schedulename = schedule['name']
        if ( schedule['type'] == "job"):
          templatename = schedule['template']
          unified_job_template_id = awx_get_id("job_templates", templatename, r)
        if ( schedule['type'] == "project"):
          projectname = schedule['project']
          unified_job_template_id = awx_get_id("projects", projectname, r)
        tz = schedule['local_time_zone']
        if ( schedule ['start'] == "now" ):
          dtstart = { 
            "year": "2012",
            "month": "12",
            "day": "01",
            "hour": "12",
            "minute": "00",
            "second": "00"
            }
        if ( int(schedule['run_every_minute']) ):
          scheduletype="Normal"
          run_frequency =  schedule['run_every_minute']
          run_every = "MINUTELY"
        if ( schedule ['end'] == "never" ):
          dtend = "null"
        awx_create_schedule(schedulename, unified_job_template_id, description,tz, dtstart, run_frequency, run_every, dtend, scheduletype, orgname, mytoken, r)
    except:
      prettyllog("config", "initialize", "schedules", orgname, "000",  "No schedules found")
### The end
