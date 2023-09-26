#!/usr/bin/env python

import requests
import json

ZABBIX_API_URL = "https://zabbix.openknowit.com/api_jsonrpc.php"
AUTHTOKEN = "9e39c4605ff25083f230b22ccaf1c18128fb8123a502abddeaad73e0b6cff0b8"
#  --data '{"jsonrpc":"2.0","method":"item.create","params":{"name":"Free disk space on /home/joe/","key_":"vfs.fs.size[/home/joe/,free]","hostid":"10084","type":0,"value_type":3,"interfaceid":"1","delay":30},"id":3}'

def get_host_groups():
    r = requests.post(ZABBIX_API_URL,
    json= {     
          "jsonrpc": "2.0",     
          "method": "hostgroup.get",     
          "params": {         
          "output": "extend",
             "filter": {
             "name": [
                 "Zabbix servers",
                 "Linux servers"
                     ]         
             }
          },     
        "id": 1 ,
        "auth": AUTHTOKEN
    })
    print(json.dumps(r.json(), indent=4, sort_keys=True))

get_host_groups()

print("\nHost group create : Linux")
r = requests.post(ZABBIX_API_URL,
        json={
    "jsonrpc": "2.0",
    "method": "hostgroup.create",
    "params": {
        "name": "Linux servers"
    },
    "id": 1,
    "auth": AUTHTOKEN
})




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

