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
    

def create_tag(tagname, env):
    prettyllog("netbox", "create", "tag", tagname, "000" , "creating tag", severity="INFO")
    url = env['KALM_NETBOX_URL'] + "/api/extras/tags/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
               'Content-Type': 'application/json'
            }
    data = {
        "name": tagname,
        "slug": tagname.lower().replace(" ", "-"),
        "color": "ff0000",
        "comments": "Created by KALM"
        }
    r = requests.post(url, headers=headers, json=data, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 201:
        data = r.json()
        prettyllog("netbox", "create", "tag", tagname, r.status_code , "tag created", severity="CHANGE")
        return data['id']
    else:
        if r.status_code == 400:
            prettyllog("netbox", "create", "tag", tagname, r.status_code , "tag exists", severity="INFO")
            return True
        prettyllog("netbox", "create", "tag", tagname, r.status_code , "unable to create tag", severity="ERROR")
        return False
    
def get_virtual_server_tags(serverid, env):
    prettyllog("netbox", "get", "virtual server tags", serverid, "000" , "getting virtual server tags", severity="INFO")
    url = env['KALM_NETBOX_URL'] + "/api/virtualization/virtual-machines/" + str(serverid) + "/tags/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
               'Content-Type': 'application/json'
            }
    mytags = []
    r = requests.get(url, headers=headers, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 200:
        data = r.json()
        for tag in data['results']:
            mytags.append(tag['name'])
        prettyllog("netbox", "get", "virtual server tags", serverid, r.status_code , "virtual server tags found", severity="INFO")
        return mytags
    else:
        prettyllog("netbox", "get", "virtual server tags", serverid, r.status_code , "unable to get virtual server tags", severity="ERROR")
        return mytags
    
def get_all_tags(env):
    prettyllog("netbox", "get", "all tags", "000", "000" , "getting all tags", severity="INFO")
    url = env['KALM_NETBOX_URL'] + "/api/extras/tags/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
               'Content-Type': 'application/json'
            }
    r = requests.get(url, headers=headers, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 200:
        data = r.json()
        alltags = {}
        for tag in data['results']:
            alltags[tag['name']] = tag['id']
        prettyllog("netbox", "get", "all tags", "000", r.status_code , "all tags found", severity="INFO")
        return alltags
    else:
        prettyllog("netbox", "get", "all tags", "000", r.status_code , "unable to get all tags", severity="ERROR")
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
    clusterid = get_cluster_id(clustername, env)
    alltags = get_all_tags(env)
    mytags = get_virtual_server_tags(serverid, env)
    found = False
    try:
        myvmwareid = alltags["vmware"]
    except:
        myvmwareid = False
    if not myvmwareid:
        myvmwareid = create_tag("vmware", env)
        alltags = get_all_tags(env)
    for mytag in mytags:
        if alltags[mytag] == "vmware":
            found = True
    if found == False:
        mytags.append(alltags["vmware"])

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
        "cluster": clusterid,
        "comments": str(serverdetails),
        "tags": mytags
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
    
def create_interface(serverdetails, env, netboxdata):
    prettyllog("netbox", "create", "interface", serverdetails['hostName'], "000" , "creating interface", severity="INFO")
    if not serverdetails['hostName']:
        prettyllog("netbox", "create", "interface", "unknown", "000" , "no hostname", severity="ERROR")
        return False
    serverid = get_virtual_server_id(serverdetails['hostName'], env)
    if not serverid:
        prettyllog("netbox", "create", "interface", serverdetails['hostName'], "000" , "server not found", severity="ERROR")
        return False
    url = env['KALM_NETBOX_URL'] + "/api/virtualization/interfaces/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
    data = {
        "virtual_machine": serverid,
        "name": "primary",
        "enabled": True,
        "mac_address": "00:00:00:00:00:00",
        "mtu": 1500,
        "mode": "access",
        "description": "Created by KALM"
        }
    r = requests.post(url, headers=headers, json=data, verify=env['KALM_NETBOX_SSL'])
    my_interface = get_interface_id(serverid, env)
    prettyllog("netbox", "create", "interface", serverdetails['hostName'], "000" , "interface id: " + str(my_interface), severity="INFO")
    if not my_interface:
        prettyllog("netbox", "create", "interface", serverdetails['hostName'], "000" , "interface not found", severity="ERROR")
        create_interface(serverdetails, env, netboxdata)    
        my_interface = get_interface_id(serverid, env)
    
    assign_ip_address(serverdetails['ipAddress'], serverdetails, env, netboxdata)

    


    if r.status_code == 201:
        
        data = r.json()
        prettyllog("netbox", "create", "interface", serverdetails['hostName'], r.status_code , "interface created", severity="CHANGE")
        return data['id']
    else:
        if r.status_code == 400:
            prettyllog("netbox", "create", "interface", serverdetails['hostName'], r.status_code , "interface exists", severity="INFO")
            return True
        prettyllog("netbox", "create", "interface", serverdetails['hostName'], r.status_code , "unable to create interface", severity="ERROR")
        return False
    
def get_interface_id(serverid, env):
    prettyllog("netbox", "get", "interface id", serverid, "000" , "getting interface id", severity="INFO")
    url = env['KALM_NETBOX_URL'] + "/api/virtualization/interfaces/?virtual_machine_id=" + str(serverid)
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
    r = requests.get(url, headers=headers, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 200:
        data = r.json()
        if len(data['results']) == 1:
            prettyllog("netbox", "get", "interface id", serverid, r.status_code , "interface id found", severity="INFO")
            return data['results'][0]['id']
        else:
            prettyllog("netbox", "get", "interface id", serverid, r.status_code , "interface id not found", severity="INFO")
            return False
    else:
        prettyllog("netbox", "get", "interface id", serverid, r.status_code , "unable to get interface id", severity="ERROR")
        return False
    
def assign_ip_address(ipaddress, serverdetails, env, netboxdata):
    #http://exrhel0494.it.rm.dk:8080/ipam/ip-addresses/add/?virtual_machine=846&vminterface=6&return_url=/virtualization/interfaces/6/

    prettyllog("netbox", "assign", "ip address", ipaddress, "000" , "assigning ip address", severity="INFO")
    ipaddressid = get_ip_address_id(ipaddress, env)
    if not ipaddressid:
        prettyllog("netbox", "assign", "ip address", "unknown", "000" , "no ip address", severity="ERROR")
        return False
    server_id = get_virtual_server_id(serverdetails['hostName'], env)
    if not server_id:
        prettyllog("netbox", "assign", "ip address", ipaddress, "000" , "server not found", severity="ERROR")
        return False
    interface_id = get_interface_id(server_id, env)
    if not interface_id:
        create_interface(serverdetails, env, netboxdata)
        interface_id = get_interface_id(server_id, env)
        prettyllog("netbox", "assign", "ip address", ipaddress, "000" , "interface not found", severity="ERROR")
        return False

    url = env['KALM_NETBOX_URL'] + "/api/ipam/ip-addresses/" + str(ipaddressid) + "/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
    data = {
            "assigned_object_type": "virtualization.vminterface",
            "assigned_object_id": interface_id,
        }
    r = requests.patch(url, headers=headers, json=data, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 201:
        data = r.json()
        prettyllog("netbox", "assign", "ip address", ipaddress, r.status_code , "ip address assigned", severity="CHANGE")
        return data['id']
    else:

        if r.status_code == 400:
            prettyllog("netbox", "assign", "ip address", ipaddress, r.status_code , "ip address exists", severity="INFO")
            return True
        prettyllog("netbox", "assign", "ip address", ipaddress, r.status_code , "unable to assign ip address", severity="ERROR")
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
#{'guestFullName': 'Red Hat Enterprise Linux 8 (64-bit)',
# 'guestId': 'rhel8_64Guest',
#'hostName': 'exrhel0537.it.rm.dk',
# 'hwVersion': 'vmx-19',
# 'ipAddress': '10.141.32.157',
# 'memory': 16384,
# 'numCpu': 4,
# 'numEthernetCards': 1,
#'numVirtualDisks': 3,
# 'overallStatus': 'green',
# 'toolsRunningStatus': 'guestToolsRunning',
# 'toolsStatus': 'toolsOk',
# 'toolsVersionStatus': 'guestToolsUnmanaged',
# 'toolsVersionStatus2': 'guestToolsUnmanaged',
# 'uuid': '420b9c5d-cc12-7b1b-62f0-2d3a85d0a9e8',
# 'vmPathName': '[GODSYD-SAN040_SYD-PROD-02_001] EXRHEL0537/EXRHEL0537.vmx'}



    pprint.pprint(serverdetails)
    guestFullName = serverdetails['guestFullName']
    guestId = serverdetails['guestId']
    hostName = serverdetails['hostName']
    hwVersion = serverdetails['hwVersion']
    ipAddress = serverdetails['ipAddress']
    memory = serverdetails['memory']
    numCpu = serverdetails['numCpu']
    numEthernetCards = serverdetails['numEthernetCards']
    numVirtualDisks = serverdetails['numVirtualDisks']
    overallStatus = serverdetails['overallStatus']
    toolsRunningStatus = serverdetails['toolsRunningStatus']
    toolsStatus = serverdetails['toolsStatus']
    toolsVersionStatus = serverdetails['toolsVersionStatus']
    toolsVersionStatus2 = serverdetails['toolsVersionStatus2']
    uuid = serverdetails['uuid']
    vmPathName = serverdetails['vmPathName']

    prettyllog("netbox", "create", "virtual server", serverdetails['hostName'], "000" , "creating cluster", severity="INFO")
    create_cluster(clustername, clustergroup, env, netboxdata)
    create_ip_address(ipAddress, env, netboxdata)
    
    
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
        'memory': memory,
        'vcpus': numCpu,



        "site":  get_site_id("Aarhus Universitetshospital", env),
        "cluster": clusterid
    }
    r = requests.post(url, headers=headers, json=data, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 201:
        data = r.json()
        prettyllog("netbox", "create", "virtual server", serverdetails['hostName'], r.status_code , "virtual server created", severity="CHANGE")
        prettyllog("netbox", "create", "virtual server", serverdetails['hostName'], "000" , "creating interface", severity="INFO")
        create_interface(serverdetails, env, netboxdata)
        prettyllog("netbox", "create", "virtual server", serverdetails['hostName'], "000" , "assigning ip address", severity="INFO")
        assign_ip_address(serverdetails['ipAddress'], serverdetails, env, netboxdata)
        return data['id']
    else:
        if r.status_code == 400:
            prettyllog("netbox", "create", "virtual server", serverdetails['hostName'], r.status_code , "virtual server exists", severity="INFO")
            update_virtual_server(serverdetails, env, netboxdata)
            return True
        prettyllog("netbox", "create", "virtual server", serverdetails['hostName'], r.status_code , "unable to create tenant_group", severity="ERROR")
        return False
    