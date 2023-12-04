import requests
import json
import os
import base64
import xml.etree.ElementTree as ET
import platform
import pprint
import yaml
from ..common import prettyllog
from .organization import get_site_id
from .clusters import create_cluster,  get_cluster_id
from .netbox_ipaddress import create_ip_address 
from .netbox_ipaddress import get_ip_address_id



def get_virtual_server(servername, env):
    prettyllog("netbox", "get", "virtual server", servername, "000" , "getting virtual server", severity="INFO")
    url = env['KALM_NETBOX_URL'] + "/api/virtualization/virtual-machines/?name=" + servername
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
    r = requests.get(url, headers=headers, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 200:
        data = r.json()
        if len(data['results']) == 1:
            prettyllog("netbox", "get", "virtual server", servername, r.status_code , "virtual server found", severity="INFO")
            return data['results'][0]['id']
        else:
            prettyllog("netbox", "get", "virtual server", servername, r.status_code , "virtual server not found", severity="INFO")
            return False
    else:
        prettyllog("netbox", "get", "virtual server", servername, r.status_code , "unable to get virtual server", severity="ERROR")
        return False
    
def get_virtual_server_by_id(serverid, env):
    prettyllog("netbox", "get", "virtual server", serverid, "000" , "getting virtual server", severity="INFO")
    url = env['KALM_NETBOX_URL'] + "/api/virtualization/virtual-machines/" + str(serverid) + "/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
    r = requests.get(url, headers=headers, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 200:
        data = r.json()
        prettyllog("netbox", "get", "virtual server", serverid, r.status_code , "virtual server found", severity="INFO")
        return data
    else:
        prettyllog("netbox", "get", "virtual server", serverid, r.status_code , "unable to get virtual server", severity="ERROR")
        return False

def get_virtual_server_id(servername, env):
    prettyllog("netbox", "get", "virtual server id", servername, "000" , "getting virtual server", severity="INFO")
    url = env['KALM_NETBOX_URL'] + "/api/virtualization/virtual-machines/?name=" + servername
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
    r = requests.get(url, headers=headers, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 200:
        data = r.json()
        if len(data['results']) == 1:
            prettyllog("netbox", "get", "virtual server", servername, r.status_code , "virtual server found", severity="INFO")
            return data['results'][0]['id']
        else:
            prettyllog("netbox", "get", "virtual server", servername, r.status_code , "virtual server not found", severity="INFO")
            return False
    else:
        prettyllog("netbox", "get", "virtual server", servername, r.status_code , "unable to get virtual server", severity="ERROR")
        return False
    

def update_virtual_server(serverdetails, env , netboxdata):
    prettyllog("netbox", "update", "virtual server", serverdetails['hostName'], "000" , "updating virtual server", severity="INFO")
    if not serverdetails['hostName']:
        prettyllog("netbox", "update", "virtual server", "unknown", "000" , "no hostname", severity="ERROR")
        return False
    serverid = get_virtual_server_id(serverdetails['hostName'], env)
    if not serverid:
        prettyllog("netbox", "update", "virtual server", serverdetails['hostName'], "000" , "server not found", severity="ERROR")
        return False
    ipaddressid = get_ip_address_id(serverdetails['ipAddress'], env)
    if not ipaddressid:
        create_ip_address(serverdetails['ipAddress'], env, netboxdata)  
        ipaddressid = get_ip_address_id(serverdetails['ipAddress'], env)
    url = env['KALM_NETBOX_URL'] + "/api/virtualization/virtual-machines/" + str(serverid) + "/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
    data = {
        "name": serverdetails['hostName'],
        #strip all wovel characters and replace spaces with -
        "slug": serverdetails['hostName'].lower().replace(" ", "-"),
        "description": "Created by KALM",
        "primary_ip4": ipaddressid,
        "memory": serverdetails['memory'],
        "vcpus": serverdetails['numCpu'],
        "site":  get_site_id("Aarhus Universitetshospital", env),
        "cluster": 41,
        "comments": str(serverdetails)
        }
    r = requests.patch(url, headers=headers, json=data, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 201:
        data = r.json()
        prettyllog("netbox", "update", "virtual server", serverdetails['hostName'], r.status_code , "virtual server created", severity="CHANGE")
        return data['id']
    else:
        if r.status_code == 400:
            prettyllog("netbox", "update", "virtual server", serverdetails['hostName'], r.status_code , "virtual server exists", severity="INFO")
            return True
        prettyllog("netbox", "update", "virtual server", serverdetails['hostName'], r.status_code , "unable to create tenant_group", severity="ERROR")
        return False


def create_virtual_server(serverdetails, env, netboxdata):
    if not serverdetails['hostName']:
        prettyllog("netbox", "create", "virtual server", "unknown", "000" , "no hostname", severity="ERROR")
        return False
    virtual_server_id = get_virtual_server(serverdetails['hostName'], env)
    if virtual_server_id:
        prettyllog("netbox", "create", "virtual server", serverdetails['hostName'], "000" , "virtual server exists", severity="INFO")
        update_virtual_server(serverdetails, env, netboxdata)
        return True
    prettyllog("netbox", "create", "virtual server", serverdetails['hostName'], "000" , "creating virtual server", severity="INFO") 

    vmpathname = serverdetails['vmPathName']
    if "GODNOR" in vmpathname:
        clustergroup = "GOD"
        clustername = "GODNOR" 
    elif "GODSYD" in vmpathname:
        clustergroup = "GOD"
        clustername = "GODSYD"
    elif "SKS" in vmpathname:
        clustergroup = "SKS"
        clustername = "SKS"
    else:
        clustergroup = "OTHER"
        clustername = "OTHER"
    prettyllog("netbox", "create", "virtual server", serverdetails['hostName'], "000" , "creating cluster", severity="INFO")
    create_cluster(clustername, clustergroup, env, netboxdata)
    clusterid = get_cluster_id(clustername, env)
    url = env['KALM_NETBOX_URL'] + "/api/virtualization/virtual-machines/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
    data = {
        "name": serverdetails['hostName'],
        #strip all wovel characters and replace spaces with -
        "slug": serverdetails['hostName'].lower().replace(" ", "-"),
        "description": "Created by KALM",
        "site":  get_site_id("Aarhus Universitetshospital", env),
        "cluster": clusterid
    }
    r = requests.post(url, headers=headers, json=data, verify=env['KALM_NETBOX_SSL'])
    pprint.pprint(r.content)
    print("----------------------------------------------- " + str(r.status_code))
    if r.status_code == 201:
        data = r.json()
        prettyllog("netbox", "create", "virtual server", serverdetails['hostName'], r.status_code , "virtual server created", severity="CHANGE")
        return data['id']
    else:
        if r.status_code == 400:
            prettyllog("netbox", "create", "virtual server", serverdetails['hostName'], r.status_code , "virtual server exists", severity="INFO")
            update_virtual_server(serverdetails, env, netboxdata)
            return True
        prettyllog("netbox", "create", "virtual server", serverdetails['hostName'], r.status_code , "unable to create tenant_group", severity="ERROR")
        return False
    