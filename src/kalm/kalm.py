import redis
from pprint import pprint
import json
import requests
import hvac
import os
import sys
import datetime
import tempfile
import pynetbox
import urllib3
import datetime
from .awx.awx_common import awx_get_id
from .awx.awx_common import getawxdata
from .awx.awx_credential import awx_create_credential
from .common import prettyllog
from .awx.awx_organisation import awx_create_organization
from .awx.awx_project import awx_create_project
from .awx.awx_project import awx_get_project

#from .awx_project import awx_get_project
#from .awx_project import awx_create_subproject
#from .awx_common import awx_create_label

def git_create_repo(name, description, private, organization, mytoken, r):
  prettyllog("manage", "repo", name, organization, "000", "-")

def git_create_org(name, description, private, mytoken, r):
  prettyllog("manage", "org", name, "000", "000", "-")

def git_create_team(name, description, private, mytoken, r):
  prettyllog("manage", "team", name, "000", "000", "-")

def git_create_user(name, description, private, mytoken, r):
  prettyllog("manage", "user", name, "000", "000", "-")





class suppress_stdout_stderr(object):
    '''
    A context manager for doing a "deep suppression" of stdout and stderr in 
    Python, i.e. will suppress all print, even if the print originates in a 
    compiled C/Fortran sub-function.
       This will not suppress raised exceptions, since exceptions are printed
    to stderr just before a script exits, and after the context manager has
    exited (at least, I think that is why it lets exceptions through).      

    '''
    def __init__(self):
        # Open a pair of null files
        self.null_fds =  [os.open(os.devnull,os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = [os.dup(1), os.dup(2)]

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0],1)
        os.dup2(self.null_fds[1],2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0],1)
        os.dup2(self.save_fds[1],2)
        # Close all file descriptors
        for fd in self.null_fds + self.save_fds:
            os.close(fd)


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

VERIFY_SSL = os.getenv("VERIFY_SSL", "false")
if VERIFY_SSL.lower() == "false" or VERIFY_SSL == "no":
    VERIFY_SSL = False
else:
    VERIFY_SSL = True


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
def checkout_git_repo(url, branch, path):
    #create a temporary directory
    tmpdir = tempfile.mkdtemp()
    #clone the repo
    command = "cd %s && git clone -b %s %s %s" % (tmpdir, branch, url, path)
    os.system(command)




def vault_get_secret(path, vault):
  secret = vault.read_secret(engine_name="secret", secret=path)['data']['data']
  return secret



  

def awx_delete(item, name, mytoken, r):
  headers = {"User-agent": "python-awx-client", "Content-Type": "application/json","Authorization": "Bearer {}".format(mytoken)}
  itemid = (awx_get_id(item, name, r))
  url = os.getenv("TOWER_HOST") + "/api/v2/" + item + "/" + itemid
  resp = requests.delete(url,headers=headers, verify=VERIFY_SSL)

def awx_purge_orphans(token, r):
  orphans = r.keys("*:orphan:*")
  for orphan in orphans:
    mykey = orphan.decode().split(":")
    awx_delete(mykey[1],mykey[3])

def verify_gitkey(project):
  if os.path.exists("/etc/kalm/keys/%s.json" % project):
    with open("/etc/kalm/keys/%s" % project) as f:
      #check if keys us a valid ssh key
      return True
  else:
    if create_gitkey(project):
      return True
    else:
      return False
  
def create_gitkey(project):
  if os.path.exists("/etc/kalm/keys/%s.json" % project):
    print("Key exists")
  else:
    print("Key does not exist")
    command = "ssh-keygen -t rsa -b 4096 -C \""
    myrun = os.comm#x(command)
    if myrun == 0:
      print("Key created")  
      return True
    else:
      print("Key creation failed")
      return False
    

    #save key



    return data['scm_key']
def awx_create_subproject(org, project, subproject, mytoken, r):
  verify_gitkey(subproject)
  orgid = (awx_get_id("organizations", org, r))
  projid = (awx_get_id("projects", project, r))

  data = {
    "name": subproject,
    "description": "subproject of " + project,
    "organization": orgid,
    "scm_type": "git",
    "scm_url": "",
    "scm_branch": "",
    "scm_clean": "false",
    "scm_delete_on_update": "false",
    "credential": "deploykey_%s" % subproject,
    "scm_update_on_launch": "false",
    "scm_update_cache_timeout": 0
  }
  # check if subproject etc file exists in /etc/kalm/kalm.d/subproject.json
  # if it exists, read it and update data
  # if it does not exist, create it
  # if it exists, but is not the same as the one in /etc/kalm/kalm.d/subproject.json, update it
  
  


  if os.path.exists("/etc/kalm/kalm.d/%s.json" % subproject):
    with open("/etc/kalm.d/subproject.json") as f:
      data = json.load(f)

  else:
      open("/etc/kalm/kalm.d/%s.json" % subproject, 'w').close()
      with open("/etc/kalm/kalm.d/%s.json" % subproject, 'w') as f:
        json.dump(data, f)

    

  


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
        getawxdata("inventories", mytoken, r)
        try:
            invid = (awx_get_id("inventories", name, r))
        except:
            print("Unexpected error")
        if (invid != "" ):
          loop = False
  headers = {"User-agent": "python-awx-client", "Content-Type": "application/json","Authorization": "Bearer {}".format(mytoken)}
  url = os.getenv("TOWER_HOST") + "/api/v2/inventories/%s/" % invid
  resp = requests.put(url,headers=headers, json=variables, verify=VERIFY_SSL)
  response = json.loads(resp.content)


  ##########################################################################################
  ##################### NETBOX #############################################################
  ##########################################################################################

  if (inventorytype == "netbox"):
    print("Create hosts in netbox")
    nbtoken = os.getenv("NBTOKEN")
    nburl = os.getenv("NBURL")
    try:
      nb = pynetbox.api(nburl, token=nbtoken)
    except:
      print("Unexpected error:", sys.exc_info()[0])
      
    ipaddresses = nb.ipam.ip_addresses.all()
    vms = nb.virtualization.virtual_machines.all()
    for vm in vms:
      if ( vm.primary_ip != None ):
        pri_ip = str(vm.primary_ip).split('/')[0]
        awx_create_host(pri_ip, str(vm.name), name,organization, mytoken, r)
        prettyllog("manage", "inventories", name, organization, resp.status_code, response)
        


def awx_create_host(name, description, inventory, organization, mytoken, r):
  prettyllog("manage", "host", name, organization, "0", "Creating host %s" % name)
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
  try:
    vaults = ansiblevault[organization]['vault']
  except: 
    vaults = []

  for vault in vaults:
    credential = { 
      "name": vault['name'], 
      "description": vault['description'], 
      "type": "Vault", 
      "vault_id": vault['vault_id'], 
      "vault_password": vault['vault_password'], 
      "kind": "vault" }
    awx_create_credential(credential, organization, mytoken, r)

# Create server access
  try: 
    sshs = ansiblevault[organization]['ssh']
  except:
    sshs = []

  for ssh in sshs:
    try:
      sshkeyval = readthefile(ssh['ssh_private_key'])
    except:
      sshkeyval = ""
    try:
      sshsingval = readthefile(ssh['ssh_signed_key'])
    except:
      sshsingval = ""
    try:
      test = ssh['name']
    except:
      ssh['name'] = "default"
    try:
      sshusername = ssh['username']
    except:
      sshusername = "root"
    try:
      sshpassword = ssh['password']
    except:
      sshpassword = ""
    try:
      sshdescription = ssh['description']
    except:
      sshdescription = "No data provided"


    credential = { 
      "name": ssh['name'], 
      "username": ssh['username'], 
      "password": ssh['password'],
      "description": ssh['description'], 
      "type": "Machine", 
      "ssh_key_data": sshkeyval,
      "ssh_public_key_data": sshsingval,
      "privilege_escalation_username": ssh['privilege_escalation_username'],
      "privilege_escalation_password": ssh['privilege_escalation_password'],
      "kind": "ssh" 
      }
    awx_create_credential(credential, organization, mytoken, r)

# Create access to git 
  try:
    scms = ansiblevault[organization]['scm']
  except:
    scms = []

  for scm in scms:
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

def awx_create_template(name, description, job_type, inventory,project,eename, credential, playbook, organization, mytoken, r):
  prettyllog("Info", "template", name, organization, "666", "Creating template %s" % name, "INFO")
  orgid = (awx_get_id("organizations", organization,r))
  invid = (awx_get_id("inventories", inventory,r ))
  projid = (awx_get_id("projects", project,r ))
  credid = (awx_get_id("credentials", credential, r))
  eeid = (awx_get_id("execution_environments", eename, r))
  prettyllog("Info", "template", name, organization, "666", "Organization %s has the id %s" % (organization, orgid))
  if eeid == "":
    eeid = 1
    errormessage = "Execution environment %s is not valid" % eename
    prettyllog("Warning", "template", name, organization, "666", errormessage)
  else:
    infomessage = "Execution environment %s has the id %s" % (eename, eeid)
    prettyllog("Info", "template", name, organization, "666", infomessage)

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
  prettyllog("Info", "template", name, organization, resp.status_code, response, "DEBUG")  
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
      prettyllog("update", "template", name, organization, resp.status_code, response, "ERROR")
  getawxdata("job_templates", mytoken, r)
  tmplid = awx_get_id("job_templates", name ,r )
  getawxdata("credentials", mytoken, r)
  credid = (awx_get_id("credentials", credential, r))
  if VERIFY_SSL == False:
    ####################### AWX VERSION IS CHANGING THIS
    #associatecommand = "awx job_template associate %s --credential %s --insecure  >/dev/null 2>/dev/null " % ( tmplid, credid)  
    associatecommand = "awx job_template associate_credential --job-template %s --credential %s --insecure >/dev/null 2>&1" % ( tmplid, credid)
    prettyllog("manage", "template", name, organization, "000", associatecommand)
    try:           
      with suppress_stdout_stderr():
        os.system(associatecommand)
        prettyllog("manage", "template", name, organization, "666", "associate credential %s to template %s" % (credid, tmplid))
    except:
      associatecommand = "awx job_template associate %s --credential %s --insecure  >/dev/null 2>/dev/null " % ( tmplid, credid)  
      try:
        with suppress_stdout_stderr():
          os.system(associatecommand)
        prettyllog("manage", "template", name, organization, "666", "associate credential %s to template %s" % (credid, tmplid))
      except:
        prettyllog("manage", "template", name, organization, "666", "Could not associate credential %s to template %s" % (credid, tmplid))


  
  else:
    #associatecommand = "awx job_template associate %s --credential %s >/dev/null 2>/dev/null " % ( tmplid, credid)
    associatecommand = "awx job_template associate_credential --job-template %s --credential %s" % ( tmplid, credid )

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
# function: get  organization
######################################
def awx_get_organization(orgid, mytoken=None, r=None):
  headers = {"User-agent": "python-awx-client", "Content-Type": "application/json","Authorization": "Bearer {}".format(mytoken)}
  url = os.getenv("TOWER_HOST") + "/api/v2/organizations/%s" % orgid
  resp = requests.get(url,headers=headers, verify=VERIFY_SSL)
  return   json.loads(resp.content)


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



######################################
# function: get subproject data 
######################################
def get_subproject(subproject, project, organisation, mytoken, r):
  print("get subproject data")

  #check if file exists in /etc/kalm/kalm.d/subproject.json
  # if it exists, read it and update data
  if os.path.exists("/etc/kalm/kalm.d/%s.json" % subproject):
    with open("/etc/kalm/kalm.d/%s.json" % subproject) as f:
      data = json.load(f)
  else:
    print("Subproject file does not exist")
    if create_subproject_file(subproject, project, organisation, mytoken, r):
      if os.path.exists("/etc/kalm/kalm.d/%s.json" % subproject):
        with open("/etc/kalm/kalm.d/%s.json" % subproject) as f:
          data = json.load(f)
      else:
        print("Subproject file does not exist")
        return False
    else:
      print("Subproject file does not exist")
      return False
  return data

def create_master_project_file(project, organisation, token, r):
  if os.path.exists("/etc/kalm.json"):
    with open("/etc/kalm.json") as f:
      data = json.load(f)
  else:
    data = {  }
    open("/etc/kalm.json", 'w').close()
    with open("/etc/kalm.json", 'w') as f:
      json.dump(data, f)
    return True
  

######################################
# function: create subproject file
######################################

def create_subproject_file(subproject, project, organisation, token, r):
  orgid = (awx_get_id("organizations", organisation, r))
  projid = (awx_get_id("projects", project, r))
  data = {
  "organization": [
    {
      "name": "{{ organization }}",
      "parentproject": "{{ project }}",
      "project": [
        {
           "name": "{{ subproject }}",
           "description": "subproject of {{ project }}",
           "scm_type": "git",
           "scm_url": "",
           "scm_branch": "",
           "scm_clean": "false",
           "scm_delete_on_update": "false",
           "credential": "deploykey_compliance",
           "scm_update_on_launch": "false",
           "scm_update_cache_timeout": 0
        }
      ],
      "inventories": [
        {
          "name": "compliance",
          "description": "Inventory containing all servers in netbox tagged compliance",
          "type": "netbox"
	}
      ],
      "templates": [
        {
          "name": "ansible_project_compliance_checkup",
          "description": "Checkup job for ensuring the ability to execute on servers",
          "job_type": "run",
          "inventory": "compliance",
          "project": "compliance",
          "EE": "Automation Hub Default execution environment",
          "credentials": "compliance",
          "playbook": "checkup.yml"
        },
        {
          "name": "ansible_project_compliance_runner",
          "description": "Apply the project compliance on servers tagged ",
          "job_type": "run",
          "inventory": "compliance",
          "project": "compliance",
          "EE": "Automation Hub Default execution environment",
          "credentials": "compliance",
          "playbook": "compliance.yml"
        }
      ],
      "schedules": [
        {
          "name": "ansible_project_compliance_checkup",
          "type": "job",
          "template": "ansible_project_compliance_checkup",
          "description": "ansible project compliance checkup shedule",
          "local_time_zone": "CET",
          "run_every_minute": "5",
          "start": "now",
          "end": "never"
        },
        {
          "name": "ansible_project_compliance_runner",
          "type": "job",
          "template": "ansible_project_compliance_runner",
          "description": "ansible project compliance runner shedule",
          "local_time_zone": "CET",
          "run_every_minute": "5",
          "start": "now",
          "end": "never"
        },
        {
          "name": "ansible_projecet_compliance",
          "type": "project",
          "project": "compliance",
          "description": "Master job for syncing project compliance",
          "local_time_zone": "CET",
          "run_every_minute": "10",
          "start": "now",
          "end": "never"
        }
      ],
      "labels":
      [
        {
          "name": "compliance"
        }
      ]
    }
  ]
}


   

  open("/etc/kalm/kalm.d/%s.json" % subproject, 'w').close()
  with open("/etc/kalm/kalm.d/%s.json" % subproject, 'w') as f:
    json.dump(data, f)
  return True




  # if it does not exist, create it







########################################################################################################################
# Main:  start
########################################################################################################################





def kalm(mytoken, r, realm="standalone", subproject=None):
  ########################################################################################################################
  # Load and set ansible secrets in ansible vault
  ########################################################################################################################
  prettyllog("init", "runtime", "config", "init", "001", "loadning secrets")
  ansiblevaultfile = "/etc/kalm/secret.json"
  f = open(ansiblevaultfile)
  ansiblevault = json.loads(f.read())
  f.close

  ###################################
  # check if git is accessible
  ###################################
  prettyllog("init", "runtime", "config", "init", "001", "checking git access")
  gitprovider=os.getenv("GITPROVIDER")
  if gitprovider == "github":
    giturl="https://github.com"
  if gitprovider == "gitlab":
    giturl="https://gitlab.com"
  if gitprovider == "bitbucket":
    giturl="https://bitbucket.org"
  if gitprovider == "gitea":
    giturl=os.getenv("GITURL")
  if gitprovider == "gogs":
    giturl=os.getenv("GITURL")

  gituser=os.getenv("GITUSER")
  gitpassword=os.getenv("GITPASSWORD")
  gitorg=os.getenv("GITORG")



    


  


  ########################################################################################################################
  # Load  and set ansible automation org
  ########################################################################################################################


  cfgfile = "/etc/kalm/kalm.json"
  # checkout git repo in kalm.json main project





  if (realm == "standalone" or realm == "main"):
          cfgfile = "/etc/kalm/kalm.json"
          realm="main"
          prettyllog("init", "runtime", "config", "master", "002",  "Running Running as daemon")
   
  if (realm == "subproject" ):
          prettyllog("init", "runtime", "config", subproject, "003" , "running cusom config file")
          cfgfile = "/etc/kalm/kalm.d/%s" % subproject + ".json"
  prettyllog("init", "runtime", "config", "master", "001", "loading config file %s" % cfgfile)
  

  f = open(cfgfile)
  config = json.loads(f.read())
  f.close

  prettyllog("init", "runtime", "config", "master", "001", "refreshing awx data")
  refresh_awx_data(mytoken, r)

  ########################################################################################################################
  # organizations
  ########################################################################################################################
  for org in (config['organization']):
    prettyllog("loop","org", "config", org['name'], "000", "organization")
    orgname = org['name']
    key = os.getenv("TOWER_HOST") + ":organizations:name:" + orgname
    r.delete(key)
    try:
      max_hosts = org['meta']['max_hosts']
    except:
      max_hosts = 100
    try: 
      default_environment = org['meta']['default_environment']
    except:
      default_environment = ""
    try:
      description = org['meta']['description']
    except:
      description = ""
    try: 
      autocreaterepositories = org['meta']['autocreaterepositories']
    except:
      autocreaterepositories = False


    prettyllog("loop","org", "config", org['name'], "000", "create or modify organization when needed")
    awx_create_organization(orgname, description, max_hosts, default_environment, realm, mytoken, r)
    getawxdata("organizations", mytoken, r)

    orgid = awx_get_id("organizations", orgname, r)
    loop = True
    while ( loop ):
      orgdata = awx_get_organization(orgid, mytoken, r)
      try:
        if ( orgdata['name'] == orgname ):
          loop = False
      except:
        loop = True

    awx_update_vault(ansiblevault, orgname, mytoken, r)
    refresh_awx_data(mytoken, r)


    ######################################
    # Projects
    ######################################
    masterproject = ""
    try:
      project = org['project']
      projectname = project['name']
      masterproject = projectname
      projectdesc = project['description']
      projecttype = project['scm_type']
      projecturl  = project['scm_url']
      projectbrnc = project['scm_branch']
      projectcred = project['credential']
      key = os.getenv("TOWER_HOST") +":projects:orphan:" + projectname
      r.delete(key)
      prettyllog("config", "initialize", "projects", orgname, "000",  "Creating project %s" % projectname)
      awx_create_project(projectname, projectdesc, projecttype, projecturl, projectbrnc, projectcred, orgname, mytoken, r)
      prettyllog("config", "initialize", "projects", orgname, "000",  "Getting project id for %s" % projectname)
      awx_get_id("projects", projectname, r)
      projid = (awx_get_id("projects", projectname, r))
      prettyllog("config", "initialize", "projects", orgname, "000",  "project id %s for %s" % (projid, projectname))
    except:
      prettyllog("config", "initialize", "projects", orgname, "000",  "No projects found")
    ######################################
    # Subprojects
    ######################################
    prettyllog("config", "initialize", "subprojects", orgname, "000",  "Checking for subprojects")
    try:
      subprojects = org['subprojects']
      print(subprojects)
      for subproject in subprojects:
        subprojectname = subproject['name']
        key = os.getenv("TOWER_HOST") +":projects:orphan:" + subprojectname
        r.delete(key)
        subproject =  get_subproject(subprojectname, masterproject, orgname, mytoken, r)
        projectname = subproject['name']
        projectdesc = subproject['description']
        projecttype = subproject['scm_type']
        projecturl  = subproject['scm_url']
        projectbrnc = subproject['scm_branch']
        projectcred = subproject['credential']
        awx_create_project(projectname, projectdesc, projecttype, projecturl, projectbrnc, projectcred, orgname, mytoken, r)
        awx_get_id("projects", subprojectname, r)
        projid = (awx_get_id("projects", subprojectname, r))
        prettyllog("config", "initialize", "subprojects", orgname, org['name'],  "sub project %s created" % subprojectname)
    except:
      prettyllog("config", "initialize", "subprojects", orgname, "000",  "No subprojects found")

  ######################################
  # inventories
  ######################################
    prettyllog("config", "initialize", "inventories", orgname, "000",  "Checking for inventories")
    try: 
      inventories = org['inventories']
    except:
      prettyllog("config", "initialize", "inventories", orgname, "000",  "No inventories found")
      inventories = []

    for inventory in inventories:
      valid=True
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
      if valid:
        awx_create_inventory(inventoryname, inventorydesc, orgname, inventorytype, inventoryvariables, mytoken, r)
      else:
        prettyllog("config", "initialize", "inventories", inventory, "000",  "Inventory is invalid")



  ######################################
  # hosts
  ######################################
    prettyllog("config", "initialize", "hosts", orgname, "000",  "Checking for hosts")
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
    prettyllog("config", "initialize", "users", orgname, "000",  "Checking for users")
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
    prettyllog("config", "initialize", "templates", orgname, "000",  "Checking for templates")
    try:
      templates = org['templates']
      for template in templates:
        prettyllog("config", "initialize", "templates", orgname, "000",  "Creating template %s" % template['name'])
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

    ######################################
    # Schedules
    ######################################
    prettyllog("config", "initialize", "schedules", orgname, "000",  "Checking for schedules")
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
