import requests
import json
import os
import time
import base64
import xml.etree.ElementTree as ET
from ..common import prettyllog
import hvac


bauilout = False




def get_netbox_data(api):

    headers = {
    'Authorization': 'Token ' + os.getenv("KALM_NETBOX_TOKEN"),
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    }
    url = os.getenv("KALM_NETBOX_URL") + "/api/" + api + "/"
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except:
        prettyllog("netbox", "check", "001", "Could not get data from %s" % url)
        return False
    

def read_file(file):
    with open(file, 'r') as myfile:
        data = myfile.read()
    return data

def refresh_netbox():
    config = read_file('/etc/kalm/netbox.json')
    config = json.loads(config)
    for key in config:
        print(key)

def check_netbox_environment_variables():
    environmentvariables = ["KALM_NETBOX_URL", "KALM_NETBOX_TOKEN"]
    for environmentvariable in environmentvariables:
        if os.getenv(environmentvariable) == "":
            prettyllog("netbox", "check", "001", "%s needs to be defined" % environmentvariable)
            return True
    return False


def check_netbox_connectivity():
        status = get_netbox_data("status")
        return status
def create_netbox_config(organiaztion):
    config = {}
    config["netbox"] = {}
    config["netbox"]["organization"] = organiaztion
    prettyllog("netbox", "check", "config", "-", "001", "Creating /etc/kalm/netbox.json")
    open('/etc/kalm/netbox.json', 'w').close()
    with open('/etc/kalm/netbox.json', 'w') as outfile:
        json.dump(config, outfile)



def read_kalm_netbox_config(organization):
    if os.path.isfile('/etc/kalm/netbox.json') == False:
        prettyllog("netbox", "check", "config", "-", "001", "Could not find /etc/kalm/netbox.json")
        create_netbox_config(organization)
    config = read_file('/etc/kalm/netbox.json')
    config = json.loads(config)
    return config

def read_kalm_config():
    if os.path.isfile('/etc/kalm/kalm.json') == False:
        prettyllog("netbox", "check", "config", "-", "001", "Could not find /etc/kalm/kalm.json")
        return False
    config = read_file('/etc/kalm/kalm.json')
    config = json.loads(config)
    return config

def service(args):
    while not bauilout:
        prettyllog("netbox", "check", "access", "-", "000", "Read the kalm netbox config")
        kalmconfig = read_kalm_config()
        if kalmconfig is not False:
            prettyllog("netbox", "check", "access", "-", "000", "We have access to /etc/kalm/kalm.json")
            prettyllog("netbox", "check", "access", "-", "000", "Out organization is %s" % kalmconfig["organization"])
            netboxconfig = read_kalm_netbox_config(kalmconfig["organization"])
        else:
            prettyllog("netbox", "check", "access", "-", "000", "We have no access to /etc/kalm/kalm.json")

        if kalmconfig['organization']['secrets'] == "filesystem":
            prettyllog("netbox", "check", "access", "-", "000", "We are using filesystem for secrets")
            read_secret = read_file('/etc/kalm/secrets.json')
            print(read_secret)
        else:
            prettyllog("netbox", "check", "access", "-", "000", "We are using vault for secrets")
            if os.getenv("VAULT_TOKEN") is None or os.getenv("KALM_VAULT_URL") is None:
                prettyllog("netbox", "check", "access", "-", "000", "We have no access to vault")
                return False
            else:
                prettyllog("netbox", "check", "access", "-", "000", "We have access to vault")
                client = hvac.Client(url=os.getenv("KALM_VAULT_URL"))
                client.token = os.getenv("VAULT_TOKEN")
                read_secret = client.read('secret/kalm')['data']['secrets']
                prettyllog("netbox", "check", "access", "-", "000", "Read the secrets from vault")


        time.sleep(10)



        


        



   