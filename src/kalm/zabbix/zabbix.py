import requests
import json
import os
import base64
import xml.etree.ElementTree as ET
import platform
import yaml
from ..common import prettyllog
from .common import get_env
import pprint

myenv = get_env()
ZABBIX_API_URL = myenv['KALM_ZABBIX_URL'] + "/api_jsonrpc.php"
AUTHTOKEN =  myenv['KALM_ZABBIX_TOKEN']


def list_host_group(hostgroup):
    r = requests.post(ZABBIX_API_URL,
    json= {     
          "jsonrpc": "2.0",     
          "method": "hostgroup.get",     
          "params": {         
          "output": "extend",
                "filter": {
                "name": [
                           hostgroup
                        ]         
                }

          },         
        "auth": AUTHTOKEN
    })
    print(json.dumps(r.json(), indent=4, sort_keys=True))

def list_host_groups():
    prettyllog("List host groups","info",   "zabbix", "list_host_groups", "zabbix.py", "kalm")
    r = requests.post(ZABBIX_API_URL,
    json= {     
          "jsonrpc": "2.0",     
          "method": "hostgroup.get",     
          "params": {         
          "output": "extend",
                 "filter": {
                 "name": [
            ] 
            }
        },
        "id": 1,
        "auth": AUTHTOKEN
    })
    pprint.pprint(r.content)
    
    print(json.dumps(r.json(), indent=4, sort_keys=True))

def get_host_id(hostname):
    r = requests.post(ZABBIX_API_URL,
    json= {

            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": "extend",
                "filter": {
                    "host": [
                        hostname
                    ]
                }
            },
            "auth": AUTHTOKEN,
            "id": 1
        })
    try:
        return r.json()['result'][0]['hostid']
    except:
        print("no host found")
        return None
    
def get_host_group_id(hostgroup):
    r = requests.post(ZABBIX_API_URL,
    json= {

            "jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params": {
                "output": "extend",
                "filter": {
                    "name": [
                        hostgroup
                    ]
                }
            },
            "auth": AUTHTOKEN,
            "id": 1
        })
    try:
        return r.json()['result'][0]['groupid']
    except:
        print("no hostgroup found")
        return None
    
def create_host(hostname , hostgroup_id, ipadress):    
    r = requests.post(ZABBIX_API_URL,
    json= {     
          "jsonrpc": "2.0",     
          "method": "host.create",     
          "params": {         
          "host": hostname,
          "interfaces": [
            {
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": ipadress,
                "dns": "",
                "port": "10050"
            }
        ],
        "groups": [
            {
                "groupid": hostgroup_id
            }
        ],
        "tags": [
            {
                "tag": "Host name",
                "value": hostname
            }
        ],
        "inventory_mode": 0,
        "inventory": {
            "macaddress_a": "01234",
            "macaddress_b": "56768"
        }
          },
        "id": 1,
        "auth": AUTHTOKEN
    })
    try:
        return r.json()['result']['hostids'][0]
    except:
        print(r.status_code)
        print(r.content)
        print("no host created")
        return None
    
def  host_update(hostname, host_id, hostgroup_id, ipadress):
    r = requests.post(ZABBIX_API_URL,
    json= {     
          "jsonrpc": "2.0",     
          "method": "host.update",     
          "params": {         
          "hostid": host_id,
          "interfaces": [
            {
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": ipadress,
                "dns": "",
                "port": "10050"
            }
        ],
        "groups": [
            {
                "groupid": hostgroup_id
            }
        ],
        "tags": [
            {
                "tag": "Host name",
                "value": hostname
            }
        ],
        "inventory_mode": 0,
        "inventory": {
            "macaddress_a": "01234",
            "macaddress_b": "56768"
        }
          },
        "id": 1,
        "auth": AUTHTOKEN
    })
    try:
        return r.json()['result']['hostids'][0]
    except:
        print(r.status_code)
        print(r.content)
        print("host not updated")
        return None

def create_host_group(hostgroup = "Linux servers"):
    r = requests.post(ZABBIX_API_URL,
    json= {     
          "jsonrpc": "2.0",     
          "method": "hostgroup.create",     
          "params": {         
          "name": hostgroup
          },     
        "auth": AUTHTOKEN
    })
    try:
        return r.json()['result']['groupids'][0]
    except:
        print("no hostgroup created")
        return None
    
def status():
    print("status")
    return 0


def register():
    print("register")
    try:
        hostname = os.environ.get('KALM_ZABBIX_HOSTNAME')
    except:
        pass
    if hostname == None:
        print("no hostname defined in env KALM_ZABBIX_HOSTNAME")
        return 1
    print("hostname: " + hostname)
    try:
        ipadress = os.environ.get('KALM_ZABBIX_HOSTIP')
    except:
        pass
    if ipadress == None:
        print("no ipadress defined in env KALM_ZABBIX_HOSTIP")
        return 1
    print("ipadress: " + ipadress)


    try:
        hostgroup = os.environ.get('KALM_ZABBIX_HOSTGROUP')
    except:
        pass
    if hostgroup == None:
        print("no hostgroup defined in env KALM_ZABBIX_HOSTGROUP")
        return 1
    
    print("hostgroup: " + hostgroup)
    hostgroup_id = get_host_group_id(hostgroup)
    if hostgroup_id == None:
        print("no hostgroup found")
        hostgroup_id = create_host_group(hostgroup)
        if hostgroup_id == None:
            print("no hostgroup created")
            return 1
        else:
            print("hostgroup created")
    else:
        print("hostgroup found")

    print("hostgroup_id: " + hostgroup_id)
    host_id = get_host_id(hostname)
    if host_id == None:
        print("no host found")
        host_id = create_host(hostname, hostgroup_id, ipadress)
        if host_id == None:
            print("no host created")
            return 1
        else:
            print("host created")
    else:
        print("host found")
        host_id = host_update(hostname, host_id, hostgroup_id, ipadress)
        if host_id == None:
            print("no host updated")
            return 1
        else:
            print("host updated")
    print("host_id: " + host_id)
    hostdate = get_host_data(host_id)
    open("hostdata.yaml", "w").write(yaml.dump(hostdate))
    return 0

def get_host_data(host_id):
    r = requests.post(ZABBIX_API_URL,
    json= {

            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": "extend",
                "filter": {
                    "hostid": [
                        host_id
                    ]
                }
            },
            "auth": AUTHTOKEN,
            "id": 1
        })
    try:
        return r.json()['result'][0]
    except:
        print("no host found")
        return None
    
def serve():
    myenv = get_env()
    prettyllog("zabbix", "init", "main", "Kalm", "000", "Serving zabbix api", "info")
    print(myenv['zabbix']['hostgroups'])
    list_host_groups()
    print(myenv['zabbix'])
    return 0



    

