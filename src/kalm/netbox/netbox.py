import requests
import json
import os
import time
import base64
import xml.etree.ElementTree as ET
from ..common import prettyllog

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


def read_kalm_netbox_config():
    if os.path.isfile('/etc/kalm/netbox.json') == False:
        prettyllog("netbox", "check", "001", "Could not find /etc/kalm/netbox.json")
        return False
    config = read_file('/etc/kalm/netbox.json')
    config = json.loads(config)
    return config



def service(args):
    while not bauilout:
        prettyllog("netbox", "check", "access", "-", "000", "Read the kalm netbox config")
        config = read_kalm_netbox_config()
        print(config)
        prettyllog("netbox", "check", "access", "-", "000", "Checking netbox environment variables")
        bailout = check_netbox_environment_variables()
        prettyllog("netbox", "check", "access", "-", "000", "Checking netbox connectivity")
        netboxaccess = check_netbox_connectivity()
        if netboxaccess:
            prettyllog("netbox", "check", "access", "-", "000", "We have access to %s " % os.getenv("KALM_NETBOX_URL"))
        else:
            prettyllog("netbox", "check", "access", "-", "000", "We have no access to %s " % os.getenv("KALM_NETBOX_URL"))
        time.sleep(10)



        


        



   