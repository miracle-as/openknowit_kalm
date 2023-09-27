#!/usr/bin/env python

import requests
import json
import os

ZABBIX_API_URL = os.getenv("ZABBIX_URL") + "/api_jsonrpc.php"
AUTHTOKEN = os.getenv("ZABBIX_TOKEN")



#  --data '{"jsonrpc":"2.0","method":"item.create","params":{"name":"Free disk space on /home/joe/","key_":"vfs.fs.size[/home/joe/,free]","hostid":"10084","type":0,"value_type":3,"interfaceid":"1","delay":30},"id":3}'

def get_host_groups():
    print("-----------------------------------")
    print(ZABBIX_API_URL)

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
