import requests
import json
import os
import base64
import xml.etree.ElementTree as ET
import platform
import yaml
from ..common import prettyllog
from .common import get_env
from ..netbox import netbox

import pprint


myenv = get_env()
ZABBIX_API_URL = myenv['KALM_ZABBIX_URL'] + "/api_jsonrpc.php"
AUTHTOKEN =  myenv['KALM_ZABBIX_TOKEN']


def list_host_group(hostgroup):
    prettyllog("zabbix", "list_host_group", "zabbix", "000", "list_host_group for %s " % hostgroup, "info")
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
        "id": 1,
        "auth": AUTHTOKEN
    })
    try:
        return(r.json())
    except: 
        return False
    
def get_host_groups():
    prettyllog("zabbix", "get_host_groups", "zabbix", "000", "get_host_groups", "info")
    r = requests.post(ZABBIX_API_URL,
        json= {     
          "jsonrpc": "2.0",     
          "method": "hostgroup.get",     
          "params": {         
            "output": "extend"
           },
          "id": 1,
          "auth": AUTHTOKEN
        }, verify=False)

    try:
        return r.json()
    except: 
        return False
    
def get_hosts():
    r = requests.post(ZABBIX_API_URL,
    json= {     
          "jsonrpc": "2.0",     
          "method": "host.get",     
          "params": {         
            "output": "extend"
          },         
          "id": 1,
          "auth": AUTHTOKEN
    }, verify=False)
    try:
        return r.json()
    except: 
        return False
    
        
def list_host_groups():
    r = requests.post(ZABBIX_API_URL,
    json= {     
          "jsonrpc": "2.0",     
          "method": "hostgroup.get",     
          "params": {         
          "output": "extend",
        },
        "id": 1,
        "auth": AUTHTOKEN
    }, verify=False)
    try:
        return(r.json())
    except:
        return False

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
        }, verify=False)
    try:
        return r.json()['result'][0]['hostid']
    except:
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
        }, verify=False)
    try:
        return r.json()['result'][0]['groupid']
    except:
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
    }, verify=False)
    try:
        return r.json()['result']['hostids'][0]
    except:
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
    }, verify=False)
    try:
        return r.json()['result']['hostids'][0]
    except:
        return None

def create_host_group(hostgroup = "Linux servers"):
    r = requests.post(ZABBIX_API_URL,
    json= {     
          "jsonrpc": "2.0",     
          "method": "hostgroup.create",     
          "params": {         
          "name": hostgroup
          },
        "id": 1,       
        "auth": AUTHTOKEN
    }, verify=False)
    try:
        return r.json()['result']['groupids'][0]
    except:
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
        }, verify=False)
    try:
        return r.json()['result'][0]
    except:
        print("no host found")
        return None
    
def serve():
    myenv = get_env()
    prettyllog("zabbix", "init", "main", "Kalm", "000", "Serving zabbix api", "info")
    hostgroups = get_host_groups()
    hostgroupsnames = {}
    hostgroupids = {}
    for hostgroup in hostgroups['result']:
        hostgroupids[hostgroup['name']] = hostgroup['groupid']
        hostgroupsnames[hostgroup['groupid']] = hostgroup['name']

    prettyllog("zabbix", "init", "main", "Kalm", "000", "hostgroups: %d" % len(hostgroupids), "info")
    for group in myenv['zabbix']['hostGroups']:
        for subgroup in group['subgroups']:
            try:    
                hostgroupid = hostgroupids[subgroup]
                prettyllog("zabbix", "init", "main", "Kalm", "000", "hostgroup %s found" % subgroup, "info")
            except:
                prettyllog("zabbix", "init", "main", "Kalm", "000", "hostgroup %s not found" % subgroup, "info")
                hostgroupid = create_host_group(subgroup)
                hostgroupids[subgroup] = hostgroupid
                hostgroupsnames[hostgroupid] = subgroup
    prettyllog("zabbix", "init", "main", "Kalm", "000", "hostgroups: %d" % len(hostgroupids), "info")

    hosts = get_hosts()
    hostsnames = {}
    hostsids = {}
    if hosts == False:
        prettyllog("zabbix", "init", "main", "Kalm", "000", "no hosts found", "info")
    else:
        for host in hosts['result']:
            hostsnames[host['host']] = host['hostid']
            hostsids[host['hostid']] = host['host']
            hostdata = get_host_data(host['hostid'])
            netboxdata = netbox.get_host(host['host'])
            if netboxdata == None:
                prettyllog("zabbix", "init", "main", "Kalm", "000", "no netbox data found for %s" % host['host'], "info")
            else:
                prettyllog("zabbix", "init", "main", "Kalm", "000", "netbox data found for %s" % host['host'], "info")
                pprint.pprint(netboxdata)

            pprint.pprint(hostdata)
        prettyllog("zabbix", "init", "main", "Kalm", "000", "hosts: %d" % len(hostsnames), "info")
    
    pprint.pprint(hostsids)


    return 0



    

