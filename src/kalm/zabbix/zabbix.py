import requests
import json
import os
import base64
import xml.etree.ElementTree as ET
import platform
import yaml
from ..common import prettyllog
import pprint


ZABBIX_API_URL = os.environ.get('ZABBIX_URL') + "/api_jsonrpc.php"
AUTHTOKEN = os.environ.get('ZABBIX_TOKEN')

#ZABBIX_API_URL = "https://zabbix.openknowit.com/api_jsonrpc.php"
#AUTHTOKEN = "9e39c4605ff25083f230b22ccaf1c18128fb8123a502abddeaad73e0b6cff0b8"
#  --data '{"jsonrpc":"2.0","method":"item.create","params":{"name":"Free disk space on /home/joe/","key_":"vfs.fs.size[/home/joe/,free]","hostid":"10084","type":0,"value_type":3,"interfaceid":"1","delay":30},"id":3}'

def list_host_group():
    HOSTGROUP= os.environ.get('ZABBIX_HOSTGROUP')
    r = requests.post(ZABBIX_API_URL,
    json= {     
          "jsonrpc": "2.0",     
          "method": "hostgroup.get",     
          "params": {         
          "output": "extend",
                "filter": {
                "name": [
                    HOSTGROUP
                        ]         
                }

          },         
        "auth": AUTHTOKEN
    })
    print(json.dumps(r.json(), indent=4, sort_keys=True))

def list_host_groups():
    r = requests.post(ZABBIX_API_URL,
    json= {     
          "jsonrpc": "2.0",     
          "method": "hostgroup.get",     
          "params": {         
          "output": "extend"},
        "auth": AUTHTOKEN
    })
    pprint.pprint(r.result)
    
    print(json.dumps(r.json(), indent=4, sort_keys=True))

def create_host_group():
    r = requests.post(ZABBIX_API_URL,
    json= {     
          "jsonrpc": "2.0",     
          "method": "hostgroup.create",     
          "params": {         
          "name": "Linux servers"
          },     
        "auth": AUTHTOKEN
    })
    print(json.dumps(r.json(), indent=4, sort_keys=True))

def create_host():
  print("\nCreate host")
  r = requests.post(ZABBIX_API_URL,
                  json={
    "jsonrpc": "2.0",
    "method": "host.create",
    "params": {
        "host": "Linux server",
        "interfaces": [
            {
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": "192.168.3.1",
                "dns": "",
                "port": "10050"
            }
        ],
        "groups": [
            {
                "groupid": "4"
            }
        ],
        "tags": [
            {
                "tag": "Host name",
                "value": "Linux server"
            }
        ],
        "inventory_mode": 0,
        "inventory": {
            "macaddress_a": "01234",
            "macaddress_b": "56768"
        }
    },
    "id": 2,
    "auth": AUTHTOKEN
  })
  print(json.dumps(r.json(), indent=4, sort_keys=True))
