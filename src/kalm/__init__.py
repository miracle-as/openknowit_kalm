from kalm import kalm
import os
import sys
import redis
import time
import subprocess
import json
import argparse
import requests




def runme(command):
  commandlist = command.split(" ")
  result = subprocess.run(commandlist, capture_output=True)
  payload = {"returncode": result.returncode, "stdout": result.stdout.decode(), "stderr": result.stderr }
  return payload


def setupkalm(force):
    if not force:
        print("We need to setup kalm - Do you with to continue (y/N)? ")
        answer = input()
        if answer == "Y" or answer == "y" or answer == "Yes" or answer == "yes":
            force = True
    if force:
        print("Initializing")
        runme("sudo mkdir /etc/kalm >/dev/null 2>&1")

def connectiontest():
    checks=[]
    errors=[]
    
    TOWERCLI = { 
        "installed": False, 
        "version": "unknown",
        "status": "unknown", 
        "env_password": os.getenv("TOWER_PASSWORD"), 
        "env_host": os.getenv("TOWER_HOST"),
        "env_username": os.getenv("TOWER_USERNAME") 
        }

    ANSIBLE_TOKEN = { "set": False, "value": "", "status": "unknown"} 
    if os.getenv("ANSIBLE_TOKEN") != None:
        ANSIBLE_TOKEN = { "set": True, "value": os.getenv("ANSIBLE_TOKEN")   , "status": "unknown"} 

    NETBOX_TOKEN = { "set": False, "value": "", "status": "unknown"} 
    if os.getenv("NETBOX_TOKEN") != None:
        NETBOX_TOKEN = { "set": True, "value": os.getenv("NETBOX_TOKEN")   , "status": "unknown"} 

    # We need to check if the config is there and a  valid  json    
    KALM_CONFIG = { "set": False, "value": "", "status": "unknown"} 
    if os.getenv("KALM_CONFIG") != None:
        KALM_CONFIG = { "set": True, "value": os.getenv("KALM_CONFIG")  , "status": "unknown"} 
    else:
        # fall back to default if not set
        KALM_CONFIG = { "set": False, "value": "/etc/kalm/kalm.json"  , "status": "unknown"} 

    KALM_SECRET = { "set": False, "value": "", "status": "unknown"} 
    if os.getenv("KALM_SECRET") != None:
        KALM_SECRET = { "set": True, "value": os.getenv("KALM_SECRET")  , "status": "unknown"} 
    else:
        # fall back to default if not set
        KALM_SECRET = { "set": False, "value": "/etc/kalm/secret.json"  , "status": "unknown"} 



    if os.path.isfile(KALM_CONFIG['value']):
      with open(KALM_CONFIG['value']) as user_file:
        try:
          parsed_json = json.load(user_file)
        except:
          errors.append("003: error in json format")
          print("003: error in json file")
          # BAIL OUT WHEN config is not json
          return False
    else:
        errors.append("004: File not found")
        # BAIL OUT WHEN config is not existing
        return False

    if os.path.isfile(KALM_SECRET['value']):
      with open(KALM_SECRET['value']) as user_file:
        try:
          parsed_json = json.load(user_file)
        except:
          errors.append("003: error in json format")
          print("003: error in json file")
          # BAIL OUT WHEN config is not json
          return False
    else:
        errors.append("004: File not found")
        # BAIL OUT WHEN config is not existing
        return False


    result = runme("awx --version")
    if result['returncode'] == 0:
        checks.append("004: awx is installed")
        TOWERCLI["installed"] =True
        TOWERCLI["version"] =  result['stdout']
        

    result = runme("awx me | jq .results[].is_superuser |grep true")
    if result['returncode'] == 0:
        checks.append("006: we are superuser on awx")
        TOWERCLI["status"] =  "ready"
    else:
        errors.append("006: we need admin access")
        return False
    
    # We neek to know if the api is accesable with our TOKEN and/or we can or shall create a new TOKEN
    if TOWERCLI["env_host"] == None:
       #We need to know where to go
        errors.append("100: We have no target defined in TOWER_HOST environment")
        return False
       
    if ANSIBLE_TOKEN['set']:
      headers = {"User-agent": "python-awx-client", "Content-Type": "application/json","Authorization": "Bearer {}".format(ANSIBLE_TOKEN['value'])}
      url = TOWERCLI['env_host'] + "/api/v2/ping/"
      resp = requests.get(url,headers=headers)
      if resp.status_code == 200:
        ANSIBLE_TOKEN['status']  = "ready"
      else:
        ANSIBLE_TOKEN['status']  = "failed"

    if ANSIBLE_TOKEN["status"] != "ready" and  TOWERCLI["status"] == "ready":
        result = runme("awx --conf.color False tokens create |jq '{'id': .id, 'token': .token }")
        parsed_json = json.loads(result["stdout"])
        newtoken = parsed_json['token']
        if result['returncode'] == 0:
          checks.append("004: awx token created")
          headers = {"User-agent": "python-awx-client", "Content-Type": "application/json","Authorization": "Bearer {}".format(newtoken)}
          url = TOWERCLI['env_host'] + "/api/v2/ping/"
          resp = requests.get(url,headers=headers)
          if resp.status_code == 200:
            ANSIBLE_TOKEN['status']  = "ready"
            os.environ["ANSIBLE_TOKEN"] = newtoken
            ANSIBLE_TOKEN = { "set": True, "value": os.getenv("ANSIBLE_TOKEN")   , "status": "ready"} 
          else:
            ANSIBLE_TOKEN['status']  = "failed"
            return False


    if len(errors) > 0:
        return False
    else:
        return True





def main():
    parser = argparse.ArgumentParser(description="Keep kalm and automate", usage="kalm <action> \n\n \
                                     options:\n  \
                                     main      Run kalm using the main/initial process to ensure the basic environment in /etc/kalm/kalm.json\n  \
                                     check     check access to services defined\n  \
                                     setup     setup access to services defined\n  \
                                     netbox    Run kalm to update netbox configured in /etc/kalm/netbox.json \n  \
                                     git       Run kalm using /etc/kalm.json and /etc/kalm.d/ \n \
                                     ")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup netbox')
    args = parser.parse_args()
    ready = False
    ready  = connectiontest()

    if args.action[0] == "check":
        if ready:
            print("We have the access we need")
            exit(0)
        else:
            exit(1)

    if args.action[0] == "setup":
        force = False
        try: 
            arg1 = args.action[1]
            if arg1 == "-y":
                force = True
            else: 
                force = False
        except:
            force = False
        setupkalm(force)



    if ready and args.action[0] == "main":
        r = redis.Redis()
        r.flushdb()
        ansibletoken = os.getenv("ANSIBLE_TOKEN")
        loop = False
        sleep = 0
        first = True
        for arg in args.action:
            if arg == "loop":
                loop = True
            if arg == "sleep=60":
                sleep = arg.split("=")[1]



        while first == True or loop == True:
            print("-----------------------------Running ansible automation daemon-------------------------------")
            kalm.kalm(ansibletoken, r)
            first = False
            if loop:
               print("-----------------------------Sleeeping half a minute----------------------------") 
               time.sleep(sleep)
               print("-----------------------------Finished sleeping----------------------------") 

    





